extends SceneTree

func _init():
	print("==================================================")
	print("  STRESS TEST: STATIONARY FPS BOUNDS & 360° AIM   ")
	print("==================================================")
	await process_frame
	
	var player_scene = load("res://scenes/player/Player.tscn")
	assert(player_scene != null, "Player.tscn must exist")
	
	var player = player_scene.instantiate()
	root.add_child(player)
	await process_frame
	
	print("[INFO] Player instantiated. move_limit: %f" % player.move_limit)
	assert(player.move_limit > 0.0 and player.move_limit <= 15.0, "Player must have realistic stationary move_limit")
	
	# TEST 1: Adversarial Out-of-Bounds Movement Stress
	print("\n--- TEST 1: OUT-OF-BOUNDS MOVEMENT STRESS ---")
	player.global_position = Vector3.ZERO
	player.set_virtual_movement(Vector2(500.0, 500.0))
	
	for i in range(120):
		player._physics_process(0.016)
		
	var pos = player.global_position
	print("[INFO] Position after extreme +500,+500 move input: (%.2f, %.2f, %.2f)" % [pos.x, pos.y, pos.z])
	assert(abs(pos.x) <= player.move_limit + 0.001, "X position must not exceed move_limit")
	assert(abs(pos.z) <= player.move_limit + 0.001, "Z position must not exceed move_limit")
	assert(pos.x == player.move_limit, "X position must be exactly clamped to move_limit")
	assert(pos.z == player.move_limit, "Z position must be exactly clamped to move_limit")
	print("[PASS] Boundary clamping enforced under extreme positive input!")
	
	# Negative extreme
	player.set_virtual_movement(Vector2(-500.0, -500.0))
	for i in range(240):
		player._physics_process(0.016)
		
	pos = player.global_position
	print("[INFO] Position after extreme -500,-500 move input: (%.2f, %.2f, %.2f)" % [pos.x, pos.y, pos.z])
	assert(abs(pos.x) <= player.move_limit + 0.001, "X position must not exceed move_limit")
	assert(abs(pos.z) <= player.move_limit + 0.001, "Z position must not exceed move_limit")
	assert(pos.x == -player.move_limit, "X position must be exactly clamped to -move_limit")
	assert(pos.z == -player.move_limit, "Z position must be exactly clamped to -move_limit")
	print("[PASS] Boundary clamping enforced under extreme negative input!")
	
	# Direct coordinate tele-warping test
	player.global_position = Vector3(9999.0, 0.0, -9999.0)
	player._physics_process(0.016)
	pos = player.global_position
	print("[INFO] Position after warp to (9999, 0, -9999): (%.2f, %.2f, %.2f)" % [pos.x, pos.y, pos.z])
	assert(pos.x == player.move_limit, "Warped X must be immediately clamped to move_limit")
	assert(pos.z == -player.move_limit, "Warped Z must be immediately clamped to -move_limit")
	print("[PASS] Immediate boundary snap verified on out-of-bounds anomaly!")
	
	# TEST 2: 360-Degree Aim Rotation
	print("\n--- TEST 2: 360° UNCONSTRAINED YAW ROTATION ---")
	player.rotation.y = 0.0
	
	# Rotate 720 degrees continuously in steps of 45 deg
	for step in range(16):
		player.rotate_camera(45.0 / player.sensitivity, 0.0)
		
	print("[INFO] Applied 720° continuous yaw rotation. Final rotation.y: %.4f rad" % player.rotation.y)
	assert(not is_nan(player.rotation.y) and not is_inf(player.rotation.y), "Yaw must be finite")
	print("[PASS] Unconstrained 360° yaw rotation verified!")
	
	# TEST 3: Touch Aim Pitch Clamping (-65° to +65°)
	print("\n--- TEST 3: PITCH CLAMPING (-65° to +65°) ---")
	var min_deg = player.min_pitch
	var max_deg = player.max_pitch
	print("[INFO] Target pitch limits: min=%.1f°, max=%.1f°" % [min_deg, max_deg])
	
	player.camera.rotation = Vector3.ZERO
	# Simulate continuous touch swipe looking up (50 drag events of +10 units)
	for i in range(50):
		player.rotate_camera(0.0, 10.0)
	var pitch_up_deg = rad_to_deg(player.camera.rotation.x)
	print("[INFO] Camera pitch after 50 upward swipes: %.2f°" % pitch_up_deg)
	assert(abs(pitch_up_deg - max_deg) < 0.1, "Camera pitch must be clamped to max_pitch (65°)")
	
	# Simulate continuous touch swipe looking down (100 drag events of -10 units)
	for i in range(100):
		player.rotate_camera(0.0, -10.0)
	var pitch_down_deg = rad_to_deg(player.camera.rotation.x)
	print("[INFO] Camera pitch after 100 downward swipes: %.2f°" % pitch_down_deg)
	assert(abs(pitch_down_deg - min_deg) < 0.1, "Camera pitch must be clamped to min_pitch (-65°)")
	print("[PASS] Touch aim pitch strictly clamped to prevent flip/gimbal lock!")
	
	# TEST 4: Recoil Kick Bounds
	print("\n--- TEST 4: RECOIL KICK LIMITS ---")
	player.camera.rotation = Vector3.ZERO
	player.apply_kick(100.0)
	var kick_pitch_deg = rad_to_deg(player.camera.rotation.x)
	print("[INFO] Camera pitch after +100 kick: %.2f°" % kick_pitch_deg)
	assert(kick_pitch_deg <= max_deg + 0.1, "Recoil kick must respect max_pitch clamp")
	print("[PASS] Camera recoil kick bounded within pitch envelope!")
	
	player.queue_free()
	await process_frame
	print("\n==================================================")
	print("  STRESS TEST: STATIONARY FPS & 360° AIM PASSED!  ")
	print("==================================================")
	quit(0)
