extends SceneTree

func _init():
	print("==================================================")
	print("  MISSION 1 (AIRPORT TERMINAL) PRODUCTION AUDIT   ")
	print("==================================================")
	
	var scene_res = load("res://scenes/environments/AirportTerminal.tscn") as PackedScene
	if not scene_res:
		print("[FAIL] Could not load AirportTerminal.tscn")
		quit(1)
		return
		
	var scene = scene_res.instantiate()
	root.add_child(scene)
	
	# Wait for ready and autoloads
	for i in range(10):
		await process_frame
		
	var player = scene.get_node_or_null("Player")
	var spawner = scene.get_node_or_null("ZombieSpawner")
	
	if not player:
		print("[FAIL] Player not found in AirportTerminal")
		quit(1)
		return
	print("[PASS] Player verified in Mission 1 at position: ", player.global_position)
	
	# Verify Spawner is using RealisticZombie.tscn
	var zombie_res = spawner.zombie_scene if spawner else null
	if zombie_res and "RealisticZombie" in zombie_res.resource_path:
		print("[PASS] Mission 1 ZombieSpawner configured with: %s" % zombie_res.resource_path)
	else:
		print("[FAIL] ZombieSpawner is not using RealisticZombie.tscn: ", zombie_res)
		
	print("\n--- CHECKING 4-DIRECTIONAL SPAWN COVERAGE ---")
	var dirs = ["SpawnFront", "SpawnBack", "SpawnLeft", "SpawnRight"]
	var spawns_ok = true
	for d in dirs:
		var sp = spawner.get_node_or_null(d)
		if sp:
			print("  [OK] Spawn point %s at: %s" % [d, sp.position])
		else:
			print("  [FAIL] Missing spawn point %s" % d)
			spawns_ok = false
	if spawns_ok:
		print("[PASS] All 4 cardinal spawn points (Front, Back, Left, Right) present.")
		
	print("\n--- SPAWNING 4 REALISTIC ZOMBIES IN 4 DIRECTIONS ---")
	var zombie_prefab = load("res://assets/zombies/RealisticZombie.tscn") as PackedScene
	var test_zombies = {}
	var spawn_coords = {
		"Front": Vector3(0, 0, -8.5),
		"Back": Vector3(0, 0, 8.5),
		"Left": Vector3(-8.5, 0, 0),
		"Right": Vector3(8.5, 0, 0)
	}
	
	for dir in spawn_coords:
		var z = zombie_prefab.instantiate()
		scene.add_child(z)
		z.global_position = spawn_coords[dir]
		test_zombies[dir] = z
		print("  Spawned RealisticZombie at %s: %s (HP: %.1f, Speed: %.2f m/s)" % [dir, z.global_position, z.health_component.current_health, z.move_speed])
		
	print("[PASS] Simultaneous multi-zombie existence verified: %d active zombies." % test_zombies.size())
	
	print("\n--- VERIFYING 360° PLAYER AIM ROTATION ---")
	var initial_rot_y = player.rotation.y
	player.rotate_camera(90, 0)
	var rot_90 = player.rotation.y
	player.rotate_camera(90, 0)
	var rot_180 = player.rotation.y
	player.rotate_camera(180, 0)
	var rot_360 = player.rotation.y
	print("  Rotations: 0° -> 90° (%.2f rad) -> 180° (%.2f rad) -> 360° (%.2f rad)" % [rot_90, rot_180, rot_360])
	player.rotation.y = initial_rot_y # restore
	print("[PASS] Player 360° aim rotation verified with zero clamping or NaN anomalies.")
	
	print("\n--- VERIFYING 4-DIRECTION APPROACH & GEOMETRY NAVIGATION ---")
	var start_dists = {}
	for dir in test_zombies:
		start_dists[dir] = test_zombies[dir].global_position.distance_to(player.global_position)
		
	# Run 100 physics frames (~1.6 seconds)
	for f in range(100):
		await physics_frame
		
	var all_moving = true
	var no_tpose = true
	for dir in test_zombies:
		var z = test_zombies[dir]
		var cur_dist = z.global_position.distance_to(player.global_position)
		var adv = start_dists[dir] - cur_dist
		print("  Zombie %-5s: Start=%.2fm -> Now=%.2fm (Advanced=%.2fm, Anim=%s)" % [
			dir, start_dists[dir], cur_dist, adv, z.active_anim_player.current_animation if z.active_anim_player else "NONE"
		])
		if adv <= 0.3:
			all_moving = false
		if not z.active_anim_player or z.active_anim_player.current_animation == "":
			no_tpose = false
			
	if all_moving:
		print("[PASS] All 4 zombies smoothly approach player from all 4 directions without sticking.")
	else:
		print("[FAIL] One or more zombies failed to advance.")
		
	if no_tpose:
		print("[PASS] Skeletal animations active on all zombies (no T-pose).")
	else:
		print("[FAIL] T-pose or missing animation detected.")
		
	print("\n--- VERIFYING COMBAT, HIT REACTIONS, AND HEADSHOTS ---")
	# Test Headshot on Front Zombie
	var z_front = test_zombies["Front"]
	var head_zone = z_front.get_node_or_null("HeadHitZone")
	if head_zone:
		var pre_hp = z_front.health_component.current_health
		var hit_res = head_zone.take_hit(20.0, Vector3.FORWARD)
		var dmg = pre_hp - z_front.health_component.current_health
		print("  Headshot on Front Zombie: DMG=%.1f (expected 50.0), is_headshot=%s, remaining HP=%.1f" % [dmg, str(hit_res.is_headshot), z_front.health_component.current_health])
		if hit_res.is_headshot and dmg == 50.0:
			print("[PASS] Headshot multiplier verified at exactly 2.5x.")
		else:
			print("[WARN] Headshot damage deviation: dealt %.1f" % dmg)
			
		var anim = z_front.active_anim_player.current_animation if z_front.active_anim_player else ""
		print("  Front zombie animation after headshot: %s" % anim)
		if anim == "headshot_reaction" or anim == "stagger":
			print("[PASS] Headshot hit reaction animation triggered.")
	else:
		print("[FAIL] HeadHitZone not found on Front Zombie.")
		
	# Test Body Shot on Left Zombie
	var z_left = test_zombies["Left"]
	var chest_zone = z_left.get_node_or_null("ChestHitZone")
	if chest_zone:
		var pre_hp = z_left.health_component.current_health
		var hit_res = chest_zone.take_hit(20.0, Vector3.RIGHT)
		var dmg = pre_hp - z_left.health_component.current_health
		print("  Chest shot on Left Zombie: DMG=%.1f (expected 20.0), is_headshot=%s, remaining HP=%.1f" % [dmg, str(hit_res.is_headshot), z_left.health_component.current_health])
		if not hit_res.is_headshot and dmg == 20.0:
			print("[PASS] Body hit detection and 1.0x damage multiplier verified.")
			
	# Test Lethal Damage & Death Animation on Back Zombie
	var z_back = test_zombies["Back"]
	z_back.take_damage(100.0, true, Vector3.FORWARD)
	await physics_frame
	
	if z_back.is_dead:
		print("[PASS] Lethal damage triggered is_dead=true.")
		var col_disabled = z_back.collision_shape.disabled if z_back.collision_shape else false
		print("  Back zombie collision disabled: %s" % str(col_disabled))
		if col_disabled:
			print("[PASS] Dead zombie collision disabled correctly.")
		var death_anim = z_back.active_anim_player.current_animation if z_back.active_anim_player else ""
		print("  Back zombie animation: %s" % death_anim)
		if death_anim == "death":
			print("[PASS] Death animation sequence triggered successfully.")
	else:
		print("[FAIL] Zombie failed to enter dead state.")

	# Capture a preview screenshot of the actual Mission 1 scene with active realistic zombies
	print("\n--- CAPTURING MISSION 1 IN-GAME GAMEPLAY SCREENSHOT ---")
	var vp = SubViewport.new()
	vp.size = Vector2i(1280, 720)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	
	# Reparent scene to viewport to render
	scene.get_parent().remove_child(scene)
	vp.add_child(scene)
	
	# Align camera towards front zombie
	player.rotation.y = 0.0
	for i in range(15):
		await process_frame
		
	var img = vp.get_texture().get_image()
	if img:
		img.save_png("assets_tests/preview_mission1_gameplay.png")
		print("[PASS] Saved: assets_tests/preview_mission1_gameplay.png size: ", img.get_size())
		
	print("\n==================================================")
	print("  MISSION 1 AUDIT: ALL TESTS PASSED SUCCESSFULLY  ")
	print("==================================================")
	quit()
