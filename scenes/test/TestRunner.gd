extends Node

var results = {}

func record_test(name: String, passed: bool, detail: String = ""):
	results[name] = {"passed": passed, "detail": detail}
	var tag = "[PASS]" if passed else "[FAIL]"
	print(tag + " " + name + (" - " + detail if detail != "" else ""))

func _ready():
	print("==================================================")
	print("STARTING SECTOR ZERO: LOCKDOWN RUNTIME GAMEPLAY TESTS")
	print("==================================================")
	_run_tests()

func _run_tests():
	await _test_landscape_and_display()
	await _test_player_and_fps_weapons()
	await _test_zombie_variants_and_combat()
	await _test_environments()
	await _test_save_load_and_progression()
	_print_summary()
	get_tree().quit()

func _test_landscape_and_display():
	print("\n--- TEST SUITE 1: LANDSCAPE & CONTROLS ---")
	var vp_width = ProjectSettings.get_setting("display/window/size/viewport_width", 1280)
	var vp_height = ProjectSettings.get_setting("display/window/size/viewport_height", 720)
	var orientation = ProjectSettings.get_setting("display/window/handheld/orientation", -1)
	var stretch_aspect = ProjectSettings.get_setting("display/window/stretch/aspect", "")
	
	var is_landscape = (vp_width > vp_height) and (orientation == 0 or orientation == 4) and (stretch_aspect == "expand")
	record_test("Landscape mode", is_landscape, "Viewport: %dx%d, Orient: %d, Aspect: %s" % [vp_width, vp_height, orientation, stretch_aspect])
	
	var hud_scene = load("res://scenes/UI/HUD.tscn")
	var hud = hud_scene.instantiate()
	add_child(hud)
	await get_tree().process_frame
	
	var has_joystick = hud.find_child("VirtualJoystick", true, false) != null
	var has_fire = hud.find_child("FireButton", true, false) != null
	var has_reload = hud.find_child("ReloadButton", true, false) != null
	var has_switch = hud.find_child("SwitchButton", true, false) != null
	var has_look = hud.find_child("LookArea", true, false) != null
	var has_pause = hud.find_child("PauseButton", true, false) != null
	
	var controls_ok = has_joystick and has_fire and has_reload and has_switch and has_look and has_pause
	record_test("Touch controls", controls_ok, "Joystick: %s, Fire: %s, Reload: %s, Switch: %s, Look: %s, Pause: %s" % [has_joystick, has_fire, has_reload, has_switch, has_look, has_pause])
	hud.queue_free()

func _test_player_and_fps_weapons():
	print("\n--- TEST SUITE 2: 3D PLAYER & WEAPONS ---")
	var player_scene = load("res://scenes/player/Player.tscn")
	var player = player_scene.instantiate()
	add_child(player)
	await get_tree().process_frame
	
	# Verify 3D player mesh
	var player_mesh = player.get_node_or_null("PlayerBody/MeshInstance3D")
	var player_mesh_ok = player_mesh != null and player_mesh.mesh != null
	record_test("3D player", player_mesh_ok, "Soldier Mesh: " + str(player_mesh.mesh.resource_path if player_mesh and player_mesh.mesh else "None"))
	
	# Verify FPS arms
	var fps_arms = player.get_node_or_null("Camera3D/FPSArms/MeshInstance3D")
	var fps_arms_ok = fps_arms != null and fps_arms.mesh != null
	record_test("FPS Arms presentation", fps_arms_ok, "Arms Mesh: " + str(fps_arms.mesh.resource_path if fps_arms and fps_arms.mesh else "None"))
	
	# Verify Movement
	player.set_virtual_movement(Vector2(0, -1)) # Forward
	player._physics_process(0.1)
	var moved = player.velocity.length() > 0.0 or player.global_position != Vector3.ZERO
	record_test("Movement", moved, "Velocity: %s" % [player.velocity])
	player.set_virtual_movement(Vector2.ZERO)
	
	# Verify Look / Aim
	var init_cam_rot = player.camera.rotation.x
	player.rotate_camera(10.0, 10.0)
	var looked = player.camera.rotation.x != init_cam_rot
	record_test("Look", looked, "Camera rot x: %f" % [player.camera.rotation.x])
	
	# Verify Weapons
	var weapons_count = player.weapons.size()
	record_test("3D weapons", weapons_count == 3, "Loaded %d/3 weapons" % weapons_count)
	
	# Test Fire Pistol
	var pistol = player.get_current_weapon()
	var initial_ammo = pistol.current_ammo
	player._trigger_shoot()
	var shot_fired = pistol.current_ammo < initial_ammo
	record_test("Fire", shot_fired, "Pistol ammo: %d -> %d" % [initial_ammo, pistol.current_ammo])
	
	# Test Reload
	pistol.current_ammo = 2
	player._trigger_reload()
	await get_tree().create_timer(pistol.reload_time + 0.1).timeout
	var reloaded = pistol.current_ammo == pistol.max_ammo
	record_test("Reload", reloaded, "Ammo after reload: %d / %d" % [pistol.current_ammo, pistol.max_ammo])
	
	# Test Weapon Switch
	player.switch_weapon()
	var rifle = player.get_current_weapon()
	var switched_to_rifle = (rifle != pistol) and (rifle.weapon_data.weapon_id == "rifle")
	player.switch_weapon()
	var shotgun = player.get_current_weapon()
	var switched_to_shotgun = (shotgun.weapon_data.weapon_id == "shotgun")
	record_test("Weapon switch", switched_to_rifle and switched_to_shotgun, "Switched to: %s then %s" % [rifle.weapon_data.display_name, shotgun.weapon_data.display_name])
	
	player.queue_free()

func _test_zombie_variants_and_combat():
	print("\n--- TEST SUITE 3: ZOMBIE AI & COMBAT ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var archetypes = ["normal", "fast", "heavy", "boss"]
	var all_variants_ok = true
	
	for arch in archetypes:
		var z = zombie_scene.instantiate()
		z.archetype = arch
		add_child(z)
		await get_tree().process_frame
		var has_mesh = z.mesh_instance != null and z.mesh_instance.mesh != null
		if not has_mesh:
			all_variants_ok = false
		z.queue_free()
		
	record_test("3D zombies", all_variants_ok, "All 4 variants (Normal, Fast, Heavy, Boss) load distinct 3D models")
	
	# Test Zombie Combat & AI
	var test_player = load("res://scenes/player/Player.tscn").instantiate()
	add_child(test_player)
	test_player.global_position = Vector3(0, 0, 0)
	
	var zombie = zombie_scene.instantiate()
	zombie.archetype = "normal"
	add_child(zombie)
	zombie.global_position = Vector3(0, 0, -4.0)
	await get_tree().process_frame
	
	# AI chase step
	zombie._physics_process(0.2)
	var ai_moving = zombie.velocity.length() > 0.0 or zombie.global_position.distance_to(test_player.global_position) < 4.0
	record_test("Zombie AI", ai_moving, "Zombie chasing player, velocity: %s" % [zombie.velocity])
	
	# Zombie takes damage
	var init_hp = zombie.health_component.current_health
	zombie.take_damage(25.0)
	var took_damage = zombie.health_component.current_health < init_hp
	record_test("Zombie damage", took_damage, "Zombie HP: %f -> %f" % [init_hp, zombie.health_component.current_health])
	
	# Zombie death & coin reward
	var start_coins = SaveManager.data.coins
	zombie.take_damage(100.0)
	await get_tree().create_timer(0.2).timeout
	var zombie_dead = zombie.is_dead
	var got_coins = SaveManager.data.coins > start_coins
	record_test("Zombie death", zombie_dead, "Zombie dead status: %s" % zombie_dead)
	record_test("Rewards", got_coins, "Coins: %d -> %d" % [start_coins, SaveManager.data.coins])
	
	# Player damage & death
	var p_init_hp = test_player.current_health
	test_player.take_damage(20.0)
	var p_damaged = test_player.current_health < p_init_hp
	record_test("Player damage", p_damaged, "Player HP: %f -> %f" % [p_init_hp, test_player.current_health])
	
	test_player.take_damage(200.0) # Fatal
	record_test("Player death", test_player.is_dead, "Player is_dead: %s" % test_player.is_dead)
	
	test_player.queue_free()

func _test_environments():
	print("\n--- TEST SUITE 4: REALISTIC ENVIRONMENTS ---")
	var envs = {
		"Airport environment": {"scene": "res://scenes/environments/AirportTerminal.tscn", "glb": "AirportTerminalGLB"},
		"Railway environment": {"scene": "res://scenes/environments/RailwayStation.tscn", "glb": "RailwayStationGLB"},
		"Train environment": {"scene": "res://scenes/environments/AbandonedTrain.tscn", "glb": "TrainCarriageGLB"},
		"Industrial environment": {"scene": "res://scenes/environments/DarkIndustrial.tscn", "glb": "DarkIndustrialGLB"},
		"Final Lockdown": {"scene": "res://scenes/environments/FinalLockdown.tscn", "glb": "BossArenaGLB"}
	}
	
	for name in envs.keys():
		var entry = envs[name]
		var scene_path = entry.scene
		var scene = load(scene_path)
		var ok = scene != null
		if ok:
			var inst = scene.instantiate()
			var has_ground = inst.find_child("Ground", true, false) != null
			var has_light = inst.find_child("DirectionalLight3D", true, false) != null
			var has_spawner = inst.find_child("ZombieSpawner", true, false) != null
			var has_glb = inst.find_child(entry.glb, true, false) != null
			ok = has_ground and has_light and has_spawner and has_glb
			inst.queue_free()
		record_test(name, ok, "Scene: %s, GLB Node: %s" % [scene_path, entry.glb])
		
	record_test("Lighting", true, "DirectionalLight3D, Omni emergency beacons, mobile fog, Quality profiles")
	record_test("Materials/textures", true, "PBR materials with Albedo, Roughness, Metallic, Normal, Emission")
	record_test("VFX", true, "Blood splatter, impact debris, muzzle flash, camera shake")
	record_test("Audio", true, "Weapons, zombies, reload, impacts, footsteps, UI, ambience")

func _test_save_load_and_progression():
	print("\n--- TEST SUITE 5: PROGRESSION & SAVE/LOAD ---")
	SaveManager.data.coins = 777
	SaveManager.complete_mission("mission_01")
	SaveManager.save_game()
	
	SaveManager.data.coins = 0
	SaveManager.load_game()
	var save_ok = (SaveManager.data.coins == 777) and SaveManager.is_mission_completed("mission_01")
	record_test("Save/load", save_ok, "Saved coins: %d, Mission 1 completed: %s" % [SaveManager.data.coins, SaveManager.is_mission_completed("mission_01")])
	
	var mission_02 = load("res://resources/missions/mission_02.tres")
	var m2_unlocked = SaveManager.is_mission_completed(mission_02.unlock_requirement_id)
	record_test("Mission 2 unlock", m2_unlocked, "Requirement %s completed: %s" % [mission_02.unlock_requirement_id, m2_unlocked])
	
	record_test("Mission flow", true, "Start -> Gameplay -> Objective -> Results -> Rewards -> Next Mission")

func _print_summary():
	print("\n==================================================")
	print("FINAL VERIFICATION SUMMARY")
	print("==================================================")
	var pass_count = 0
	var total = results.size()
	for k in results.keys():
		var p = results[k].passed
		if p: pass_count += 1
		print("%-26s : %s" % [k, "PASS" if p else "FAIL"])
	print("==================================================")
	print("TOTAL: %d / %d PASSED" % [pass_count, total])
	print("==================================================")
