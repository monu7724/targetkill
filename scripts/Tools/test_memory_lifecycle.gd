extends SceneTree

func _init():
	print("==================================================")
	print("STARTING MEMORY LIFECYCLE STRESS & STABILITY AUDIT")
	print("==================================================")
	
	var initial_mem = OS.get_static_memory_usage()
	print("[%d ms] [MEM_AUDIT] Initial baseline static memory: %.2f MB" % [Time.get_ticks_msec(), initial_mem / (1024.0 * 1024.0)])
	
	# Part 1: 5x repeated Mission 1 -> Results -> Mission Select -> Mission 1
	print("\n--- PART 1: 5x REPEATED LOOP (Mission 1 -> Results -> Mission Select) ---")
	var m1_path = "res://scenes/environments/AirportTerminal.tscn"
	var ms_path = "res://scenes/UI/MissionSelect.tscn"
	
	var loop_mems = []
	for i in range(5):
		var cycle_start_ms = Time.get_ticks_msec()
		var pre_mem = OS.get_static_memory_usage()
		
		# 1. Load Mission 1
		var m1_scene = load(m1_path)
		assert(m1_scene != null, "Mission 1 must load")
		var m1_node = m1_scene.instantiate()
		root.add_child(m1_node)
		
		# Let physics and render frames process
		for f in range(5):
			await process_frame
			
		# 2. Trigger Result UI (Victory)
		var res_ui = m1_node.find_child("ResultUI", true, false)
		if res_ui and res_ui.has_method("_on_mission_completed"):
			var dummy_m = MissionData.new()
			dummy_m.mission_id = "mission_01"
			dummy_m.display_name = "First Contact"
			dummy_m.reward_coins = 100
			dummy_m.target_count = 10
			res_ui._on_mission_completed(dummy_m)
			for f in range(3):
				await process_frame
				
		# 3. Clean unload Mission 1
		m1_node.queue_free()
		for f in range(3):
			await process_frame
			
		# 4. Load Mission Select
		var ms_scene = load(ms_path)
		assert(ms_scene != null, "Mission Select must load")
		var ms_node = ms_scene.instantiate()
		root.add_child(ms_node)
		for f in range(3):
			await process_frame
			
		# 5. Clean unload Mission Select
		ms_node.queue_free()
		for f in range(3):
			await process_frame
			
		var post_mem = OS.get_static_memory_usage()
		var delta_kb = (post_mem - pre_mem) / 1024.0
		loop_mems.append(post_mem)
		print("[%d ms] [CYCLE %d/5] Duration: %d ms | Mem: %.2f MB (Delta: %+.1f KB)" % [
			Time.get_ticks_msec(),
			i + 1,
			Time.get_ticks_msec() - cycle_start_ms,
			post_mem / (1024.0 * 1024.0),
			delta_kb
		])
	
	# Part 2: 1x Mission 1 -> Mission 2 -> Mission Select -> Mission 1
	print("\n--- PART 2: MISSION SWITCH FLOW (M1 -> M2 -> Mission Select -> M1) ---")
	var m2_path = "res://scenes/environments/RailwayStation.tscn"
	var switch_start_ms = Time.get_ticks_msec()
	
	# Load M1
	var s1 = load(m1_path).instantiate()
	root.add_child(s1)
	for f in range(3): await process_frame
	s1.queue_free()
	for f in range(3): await process_frame
	
	# Load M2 (Railway Station)
	var s2 = load(m2_path).instantiate()
	root.add_child(s2)
	for f in range(3): await process_frame
	s2.queue_free()
	for f in range(3): await process_frame
	
	# Load Mission Select
	var s_ms = load(ms_path).instantiate()
	root.add_child(s_ms)
	for f in range(3): await process_frame
	s_ms.queue_free()
	for f in range(3): await process_frame
	
	# Load M1 again
	var s1_again = load(m1_path).instantiate()
	root.add_child(s1_again)
	for f in range(3): await process_frame
	s1_again.queue_free()
	for f in range(3): await process_frame
	
	var final_mem = OS.get_static_memory_usage()
	print("[%d ms] [SWITCH_FLOW] Duration: %d ms | Final Static Mem: %.2f MB" % [
		Time.get_ticks_msec(),
		Time.get_ticks_msec() - switch_start_ms,
		final_mem / (1024.0 * 1024.0)
	])
	
	# Verification assertions
	# Memory between Cycle 2 and Cycle 5 should be flat (cached resources stable)
	var mem_growth = (loop_mems[4] - loop_mems[1]) / (1024.0 * 1024.0)
	print("\nMemory growth between Cycle 2 and Cycle 5: %+.2f MB" % mem_growth)
	assert(mem_growth < 5.0, "Memory growth over 4 iterations must not exceed 5 MB (no runaway leaks)")
	
	print("==================================================")
	print("ALL MEMORY LIFECYCLE TESTS PASSED CLEANLY!")
	print("==================================================")
	quit(0)
