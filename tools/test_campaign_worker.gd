extends SceneTree

func _init():
	# Wait for autoloads to initialize
	for i in range(10):
		await process_frame
		
	print("\n==================================================")
	print("WORKER_CAMPAIGN VERIFICATION SUITE")
	print("==================================================\n")
	
	var passed = 0
	var total = 0
	
	# Test 1: 12 missions loaded and valid
	total += 1
	var m_loaded = true
	var expected_rewards = [500, 750, 1000, 1250, 1500, 1800, 2100, 2500, 3000, 3500, 4000, 6000]
	for i in range(1, 13):
		var path = "res://resources/missions/mission_%02d.tres" % i
		var m = load(path)
		if not m or m.wave_count != 3 or m.reward_cash != expected_rewards[i - 1]:
			m_loaded = false
			print("[FAIL] M%02d invalid: m=%s, waves=%s, cash=%s" % [i, m, m.wave_count if m else 0, m.reward_cash if m else 0])
		var expected_req = "" if i == 1 else ("mission_%02d" % (i - 1))
		if m and m.unlock_requirement_id != expected_req:
			m_loaded = false
			print("[FAIL] M%02d req mismatch: '%s' != '%s'" % [i, m.unlock_requirement_id, expected_req])
	if m_loaded:
		passed += 1
		print("[PASS] 1. 12 Missions: All loaded, wave_count=3, linear cash scaling, sequential unlock chaining")
	else:
		print("[FAIL] 1. 12 Missions validation failed")
		
	# Test 2: Mission 1 scene_path and Mission 2 scene_path
	total += 1
	var m1 = load("res://resources/missions/mission_01.tres")
	var m2 = load("res://resources/missions/mission_02.tres")
	var scenes_ok = (m1.scene_path == "res://scenes/environments/AirportTerminal.tscn" and 
					 m2.scene_path == "res://scenes/environments/AirportServiceRoad.tscn")
	if scenes_ok:
		passed += 1
		print("[PASS] 2. Scene paths: M1 -> AirportTerminal.tscn, M2 -> AirportServiceRoad.tscn")
	else:
		print("[FAIL] 2. Scene paths invalid: M1=%s, M2=%s" % [m1.scene_path, m2.scene_path])
		
	# Test 3: AirportServiceRoad.tscn loading and node structure
	total += 1
	var asr_scene = load("res://scenes/environments/AirportServiceRoad.tscn")
	var asr_ok = false
	if asr_scene:
		var asr = asr_scene.instantiate()
		var has_player = asr.find_child("Player", true, false) != null
		var has_spawner = asr.find_child("ZombieSpawner", true, false) != null
		var has_ground = asr.find_child("Ground", true, false) != null
		var has_light = asr.find_child("DirectionalLight3D", true, false) != null
		var has_props = asr.find_child("Props", true, false) != null
		var spawner = asr.find_child("ZombieSpawner", true, false)
		var has_spawn_points = spawner and spawner.spawn_points.size() == 6
		asr_ok = has_player and has_spawner and has_ground and has_light and has_props and has_spawn_points
		asr.queue_free()
	if asr_ok:
		passed += 1
		print("[PASS] 3. AirportServiceRoad.tscn: Instantiates with Player, ZombieSpawner, Ground, DirectionalLight3D, Props, and 6 spawn points")
	else:
		print("[FAIL] 3. AirportServiceRoad.tscn structure invalid")
		
	# Test 4: Single-Claim Bounty Enforcement in MissionManager.gd
	total += 1
	var save_mgr = root.get_node_or_null("/root/SaveManager")
	var mission_mgr = root.get_node_or_null("/root/MissionManager")
	var single_claim_ok = false
	if save_mgr and mission_mgr:
		save_mgr.data.completed_missions.clear()
		save_mgr.data.cash = 0
		save_mgr.save_game()
		
		# First win on M2 (should award $750)
		mission_mgr.current_mission = m2
		mission_mgr.finish_mission(true)
		var c1 = save_mgr.data.cash
		var b1 = mission_mgr.last_stats.bounty_awarded
		
		# Second win (replay) on M2 (should award $0)
		mission_mgr.current_mission = m2
		mission_mgr.finish_mission(true)
		var c2 = save_mgr.data.cash
		var b2 = mission_mgr.last_stats.bounty_awarded
		
		single_claim_ok = (c1 == 750 and b1 == 750 and c2 == 750 and b2 == 0)
	if single_claim_ok:
		passed += 1
		print("[PASS] 4. Single-Claim Bounty Enforcement: Win 1 awards $750, Win 2 (replay) awards $0")
	else:
		print("[FAIL] 4. Single-Claim Bounty Enforcement failed")
		
	# Test 5: GameManager 3-wave progression and EventBus.wave_started emission
	total += 1
	var event_bus = root.get_node_or_null("/root/EventBus")
	var gm_ok = false
	if event_bus:
		var waves_seen = []
		var cb = func(w, t): waves_seen.append([w, t])
		event_bus.wave_started.connect(cb)
		
		var gm = Node3D.new()
		gm.set_script(load("res://scripts/GameManager.gd"))
		gm.mission = m2
		root.add_child(gm)
		
		gm_ok = (waves_seen.size() >= 1 and waves_seen[0][0] == 1 and waves_seen[0][1] == 3 and gm.current_wave == 1)
		
		event_bus.wave_started.disconnect(cb)
		gm.queue_free()
	if gm_ok:
		passed += 1
		print("[PASS] 5. GameManager.gd: Emits EventBus.wave_started(1, 3) on wave start")
	else:
		print("[FAIL] 5. GameManager wave_started emission failed")
		
	# Test 6: Mission 2 waves structured with dog groups
	total += 1
	var m2_waves_ok = m2.waves.size() == 3
	var all_dogs = true
	var total_dog_count = 0
	for w in m2.waves:
		for g in w.get("groups", []):
			if g.get("enemy_type") != "dog":
				all_dogs = false
			total_dog_count += g.get("count", 0)
	m2_waves_ok = m2_waves_ok and all_dogs and total_dog_count == 32
	if m2_waves_ok:
		passed += 1
		print("[PASS] 6. Mission 2 3-Wave Dog Structure: 3 waves, 32 dogs total across directional groups")
	else:
		print("[FAIL] 6. Mission 2 wave dog structure invalid")

	# Restore save state
	if save_mgr:
		save_mgr.data.cash = 777
		save_mgr.data.completed_missions = ["mission_01", "mission_02"]
		save_mgr.save_game()
		
	print("\n==================================================")
	print("WORKER_CAMPAIGN SUITE: %d / %d PASSED" % [passed, total])
	print("==================================================")
	
	if passed == total:
		quit(0)
	else:
		quit(1)
