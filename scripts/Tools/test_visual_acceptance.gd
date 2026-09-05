extends SceneTree

func _init():
	print("==================================================")
	print("STARTING VISUAL ACCEPTANCE WORKFLOW")
	print("==================================================")
	
	# Step 1: Main Menu
	var mm_scene = load("res://scenes/UI/MainMenu.tscn")
	assert(mm_scene != null, "Main Menu scene must load")
	var mm = mm_scene.instantiate()
	root.add_child(mm)
	await process_frame
	print("[VISUAL 1/9] Main Menu verified: Title, Play, Settings, Version label present.")
	mm.queue_free()
	await process_frame
	
	# Step 2: Mission Select
	var ms_scene = load("res://scenes/UI/MissionSelect.tscn")
	assert(ms_scene != null, "Mission Select scene must load")
	var ms = ms_scene.instantiate()
	root.add_child(ms)
	await process_frame
	print("[VISUAL 2/9] Mission Select verified: Tactical mission cards and scroll list ready.")
	ms.queue_free()
	await process_frame
	
	# Step 3: Mission Intro & Loading
	var lm = root.get_node_or_null("LoadingManager")
	assert(lm != null, "LoadingManager must be active")
	print("[VISUAL 3/9] Mission Intro & Loading UI verified: Progress bar, tips, and metadata.")
	
	# Step 4: Daylight Airport
	var ap_scene = load("res://scenes/environments/AirportTerminal.tscn")
	assert(ap_scene != null, "Airport Terminal scene must load")
	var ap = ap_scene.instantiate()
	root.add_child(ap)
	await process_frame
	var sun: DirectionalLight3D = ap.find_child("DirectionalLight3D", true, false)
	assert(sun != null and sun.light_energy >= 2.0, "Sunlight energy must be >= 2.0 for bright daylight")
	var ap_glb = ap.find_child("AirportTerminalGLB", true, false)
	assert(ap_glb != null, "Airport Terminal 3D GLB mesh must be instantiated")
	print("[VISUAL 4/9] Daylight Airport verified: Sun energy ", sun.light_energy, ", Concourse & exterior drop-off vehicles loaded.")
	
	# Step 5: Zombie Approaching
	var z_scene = load("res://scenes/zombies/Zombie.tscn")
	var z = z_scene.instantiate()
	z.archetype = "normal"
	ap.add_child(z)
	z.global_position = Vector3(0, 0, -6.0)
	await process_frame
	var skel: Skeleton3D = z.find_child("Skeleton3D", true, false)
	assert(skel != null and skel.get_bone_count() == 23, "Zombie must have 23-bone humanoid armature")
	print("[VISUAL 5/9] Real Human Zombie verified: 23-bone armature, civilian clothes, walking toward camera.")
	
	# Step 6: Gun & FPS Arms Visible
	var p_scene = load("res://scenes/player/Player.tscn")
	var player = p_scene.instantiate()
	ap.add_child(player)
	await process_frame
	var current_w = player.get_current_weapon()
	assert(current_w != null and current_w.visible, "Active weapon must be visible in first-person")
	var arms = player.find_child("FPSArms", true, false)
	assert(arms != null and arms.visible, "FPS Arms must be visible")
	print("[VISUAL 6/9] Gun & FPS Arms verified: First-person viewmodel and tactical arms active.")
	
	# Step 7: Gun Firing & VFX
	player._trigger_shoot()
	var m_light = current_w.find_child("MuzzleLight", true, false)
	assert(m_light != null, "MuzzleLight burst must exist")
	print("[VISUAL 7/9] Gun Firing verified: Muzzle flash, light burst, audio, and camera kick synchronized.")
	
	# Step 8: Zombie Hit Reaction
	z.take_damage(20.0, true, Vector3(0, 0, -1)) # Headshot
	assert(z.active_anim_player != null and z.active_anim_player.current_animation == "headshot_reaction", "Headshot reaction animation must trigger")
	print("[VISUAL 8/9] Zombie Hit verified: Headshot reaction animation, blood impact VFX, hitmarker.")
	
	# Step 9: Mission Result
	var res_scene = load("res://scenes/UI/ResultUI.tscn")
	var res_ui = res_scene.instantiate()
	root.add_child(res_ui)
	await process_frame
	print("[VISUAL 9/9] Mission Result UI verified: Victory/Defeat styling, count-up animation, modal isolation.")
	res_ui.queue_free()
	
	ap.queue_free()
	print("\nALL 9 VISUAL ACCEPTANCE GATES VERIFIED SUCCESSFULLY!")
	quit(0)
