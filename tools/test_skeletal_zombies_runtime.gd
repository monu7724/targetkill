extends SceneTree

func _init():
	print("--- UNIT TEST: SKELETAL ZOMBIE RIGS & ANIMATIONS ---")
	var z_scene = load("res://scenes/zombies/Zombie.tscn")
	assert(z_scene != null, "Zombie.tscn must load")
	
	# Test 1: Normal Zombie Skeletal Rig & Animations
	var z_normal = z_scene.instantiate()
	z_normal.archetype = "normal"
	root.add_child(z_normal)
	await process_frame
	
	assert(z_normal.model_instance != null, "Skeletal model must be instantiated")
	assert(z_normal.active_anim_player != null, "Active AnimationPlayer must be found")
	
	var normal_anims = z_normal.active_anim_player.get_animation_list()
	print("Normal Zombie Animations: ", normal_anims)
	for req in ["idle", "walk", "fast_walk", "attack", "hit_front", "hit_back", "hit_left", "hit_right", "headshot_reaction", "stagger", "death"]:
		assert(normal_anims.has(req), "Normal Zombie must have animation: " + req)
	print("[PASS] Normal Zombie has all 11 required skeletal animations")
	
	# Verify Skeleton3D bone count
	var skel: Skeleton3D = z_normal.model_instance.find_child("Skeleton3D", true, false)
	assert(skel != null, "Skeleton3D must exist in model")
	assert(skel.get_bone_count() == 23, "Humanoid armature must have 23 bones")
	print("[PASS] Normal Zombie humanoid armature verified (23 bones)")
	
	# Test 2: Directional Hit Reacts
	z_normal.health_component.current_health = 500.0
	z_normal.take_damage(10.0, true, Vector3(0, 0, -1)) # Headshot
	assert(z_normal.active_anim_player.current_animation == "headshot_reaction", "Headshot must play headshot_reaction")
	print("[PASS] Headshot triggers headshot_reaction animation")
	
	z_normal.take_damage(10.0, false, Vector3(-1, 0, 0)) # Left flank hit
	assert(z_normal.active_anim_player.current_animation == "hit_left", "Left hit must play hit_left")
	print("[PASS] Left flank bullet triggers hit_left animation")
	
	z_normal.take_damage(10.0, false, Vector3(1, 0, 0)) # Right flank hit
	assert(z_normal.active_anim_player.current_animation == "hit_right", "Right hit must play hit_right")
	print("[PASS] Right flank bullet triggers hit_right animation")
	
	z_normal.take_damage(30.0, false, Vector3.ZERO) # Heavy body shot
	assert(z_normal.active_anim_player.current_animation == "stagger", "Heavy shot must play stagger")
	print("[PASS] Heavy shot triggers stagger animation")
	
	z_normal.queue_free()
	
	# Test 3: Fast Zombie
	var z_fast = z_scene.instantiate()
	z_fast.archetype = "fast"
	root.add_child(z_fast)
	await process_frame
	var fast_anims = z_fast.active_anim_player.get_animation_list()
	for req in ["idle", "run", "turn", "attack", "hit", "stagger", "death"]:
		assert(fast_anims.has(req), "Fast Zombie must have animation: " + req)
	print("[PASS] Fast Zombie has all 7 required skeletal animations")
	z_fast.queue_free()
	
	# Test 4: Heavy Zombie
	var z_heavy = z_scene.instantiate()
	z_heavy.archetype = "heavy"
	root.add_child(z_heavy)
	await process_frame
	var heavy_anims = z_heavy.active_anim_player.get_animation_list()
	for req in ["idle", "heavy_walk", "heavy_attack", "impact", "stagger", "death"]:
		assert(heavy_anims.has(req), "Heavy Zombie must have animation: " + req)
	print("[PASS] Heavy Zombie has all 6 required skeletal animations")
	z_heavy.queue_free()
	
	# Test 5: Boss Zombie
	var z_boss = z_scene.instantiate()
	z_boss.archetype = "boss"
	root.add_child(z_boss)
	await process_frame
	var boss_anims = z_boss.active_anim_player.get_animation_list()
	for req in ["idle", "walk", "attack_windup", "heavy_attack", "roar", "hit", "stagger", "death"]:
		assert(boss_anims.has(req), "Boss Zombie must have animation: " + req)
	print("[PASS] Boss Zombie has all 8 required skeletal animations")
	var boss_skel: Skeleton3D = z_boss.model_instance.find_child("Skeleton3D", true, false)
	assert(boss_skel.get_bone_count() == 24, "Boss armature must have 24 bones (including ScytheBlade)")
	print("[PASS] Boss Zombie 24-bone armature with ScytheBlade verified")
	z_boss.queue_free()
	
	print("\nALL SKELETAL RIG AND ANIMATION TESTS PASSED!")
	quit(0)
