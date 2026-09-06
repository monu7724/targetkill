extends SceneTree

# ==============================================================================
# Sector Zero: Lockdown — Adversarial Correctness Challenge Suite
# challenger_1 — Empirical Verification Harness
# ==============================================================================

var total_tests: int = 0
var passed_tests: int = 0
var failed_tests: int = 0
var failure_log: Array[String] = []

func _record_test(name: String, passed: bool, details: String = ""):
	total_tests += 1
	if passed:
		passed_tests += 1
		print("[PASS] %s %s" % [name, ("(" + details + ")") if details != "" else ""])
	else:
		failed_tests += 1
		var msg = "[FAIL] %s %s" % [name, ("(" + details + ")") if details != "" else ""]
		printerr(msg)
		failure_log.append(msg)

func _init():
	# Allow autoload singletons to settle
	for i in range(10):
		await process_frame
		
	print("\n" + "=".repeat(70))
	print("  ADVERSARIAL CORRECTNESS CHALLENGE SUITE — CHALLENGER 1")
	print("=".repeat(70))
	
	await _test_single_claim_bounty_enforcement()
	await _test_weapon_upgrades_and_economy()
	await _test_12_mission_registry_and_waves()
	await _test_infected_dog_hitzones()
	
	print("\n" + "=".repeat(70))
	print("  CHALLENGE SUITE RESULTS: %d / %d PASSED (%d FAILED)" % [passed_tests, total_tests, failed_tests])
	print("=".repeat(70))
	
	if failed_tests > 0:
		print("\nFAILURES ENCOUNTERED:")
		for f in failure_log:
			printerr("  - " + f)
		quit(1)
	else:
		print("\nALL EMPIRICAL CHALLENGES PASSED WITH ZERO REGRESSIONS.")
		quit(0)

# ==============================================================================
# 1. Single-Claim Bounty Enforcement (5 sequential completions + persistence)
# ==============================================================================
func _test_single_claim_bounty_enforcement():
	print("\n--- CHALLENGE 1: SINGLE-CLAIM BOUNTY ENFORCEMENT (5 COMPLETIONS) ---")
	
	var save_mgr = root.get_node_or_null("SaveManager")
	_record_test("SaveManager singleton available", save_mgr != null)
	if not save_mgr:
		return
		
	var mission_mgr = root.get_node_or_null("MissionManager")
	_record_test("MissionManager singleton available", mission_mgr != null)
	if not mission_mgr:
		return

	# Reset save state hermetically for clean test
	save_mgr.data.cash = 1000
	save_mgr.data.completed_missions = []
	save_mgr.save_game()
	
	var m1: MissionData = load("res://resources/missions/mission_01.tres")
	_record_test("Mission 1 loaded", m1 != null and m1.reward_cash == 500)
	if not m1:
		return

	var start_cash = save_mgr.data.cash # 1000
	
	# CLEAR 1: First-time clear should award +$500
	mission_mgr.start_mission(m1)
	mission_mgr.kill_count = 10
	mission_mgr.shots_fired = 10
	mission_mgr.shots_hit = 10
	mission_mgr.finish_mission(true)
	
	var cash_after_c1 = save_mgr.data.cash
	_record_test("Clear 1: Bounty awarded (+500)", cash_after_c1 == start_cash + 500, "Cash: %d (expected %d)" % [cash_after_c1, start_cash + 500])
	_record_test("Clear 1: Stats reflect bounty", mission_mgr.last_stats.bounty_awarded == 500 and mission_mgr.last_stats.first_time_reward == true)
	_record_test("Clear 1: Mission marked complete", save_mgr.is_mission_completed("mission_01"))

	# CLEAR 2 (Replay 1): Should award +$0
	mission_mgr.start_mission(m1)
	mission_mgr.kill_count = 12
	mission_mgr.shots_fired = 15
	mission_mgr.shots_hit = 12
	mission_mgr.finish_mission(true)
	
	var cash_after_c2 = save_mgr.data.cash
	_record_test("Clear 2 (Replay 1): Zero bounty awarded (+$0)", cash_after_c2 == cash_after_c1, "Cash: %d (expected %d)" % [cash_after_c2, cash_after_c1])
	_record_test("Clear 2 (Replay 1): Stats reflect $0 bounty", mission_mgr.last_stats.bounty_awarded == 0 and mission_mgr.last_stats.first_time_reward == false)

	# CLEAR 3 (Replay 2 with disk reload): Reload from disk, replay must still award +$0
	save_mgr.load_game()
	_record_test("Disk reload retains completed state", save_mgr.is_mission_completed("mission_01") and save_mgr.data.cash == cash_after_c1)
	
	mission_mgr.start_mission(m1)
	mission_mgr.kill_count = 8
	mission_mgr.shots_fired = 10
	mission_mgr.shots_hit = 8
	mission_mgr.finish_mission(true)
	
	var cash_after_c3 = save_mgr.data.cash
	_record_test("Clear 3 (Replay 2 post-reload): Zero bounty awarded (+$0)", cash_after_c3 == cash_after_c1, "Cash: %d" % cash_after_c3)
	_record_test("Clear 3 (Replay 2 post-reload): Stats reflect $0 bounty", mission_mgr.last_stats.bounty_awarded == 0)

	# CLEAR 4 (Replay 3): Replay must award +$0
	mission_mgr.start_mission(m1)
	mission_mgr.kill_count = 15
	mission_mgr.finish_mission(true)
	
	var cash_after_c4 = save_mgr.data.cash
	_record_test("Clear 4 (Replay 3): Zero bounty awarded (+$0)", cash_after_c4 == cash_after_c1, "Cash: %d" % cash_after_c4)
	_record_test("Clear 4 (Replay 3): Stats reflect $0 bounty", mission_mgr.last_stats.bounty_awarded == 0)

	# CLEAR 5 (Replay 4): Replay must award +$0
	mission_mgr.start_mission(m1)
	mission_mgr.kill_count = 20
	mission_mgr.finish_mission(true)
	
	var cash_after_c5 = save_mgr.data.cash
	_record_test("Clear 5 (Replay 4): Zero bounty awarded (+$0)", cash_after_c5 == cash_after_c1, "Cash: %d" % cash_after_c5)
	_record_test("Clear 5 (Replay 4): Stats reflect $0 bounty", mission_mgr.last_stats.bounty_awarded == 0)

	# EDGE CASE: Failure prior to completion does not award cash, does not complete, and allows subsequent first-time reward
	var m2: MissionData = load("res://resources/missions/mission_02.tres")
	_record_test("Mission 2 loaded", m2 != null and m2.reward_cash == 750)
	if m2:
		var cash_before_m2 = save_mgr.data.cash
		# Attempt and FAIL mission 2
		mission_mgr.start_mission(m2)
		mission_mgr.finish_mission(false)
		_record_test("Failed mission awards $0", save_mgr.data.cash == cash_before_m2, "Cash: %d" % save_mgr.data.cash)
		_record_test("Failed mission not marked completed", not save_mgr.is_mission_completed("mission_02"))
		
		# Now succeed mission 2 -> must award full $750 bounty
		mission_mgr.start_mission(m2)
		mission_mgr.finish_mission(true)
		_record_test("First success after failure awards full bounty (+750)", save_mgr.data.cash == cash_before_m2 + 750, "Cash: %d" % save_mgr.data.cash)
		_record_test("Mission 2 now marked complete", save_mgr.is_mission_completed("mission_02"))
		
		# Replay mission 2 -> awards $0
		mission_mgr.start_mission(m2)
		mission_mgr.finish_mission(true)
		_record_test("Mission 2 replay awards $0", save_mgr.data.cash == cash_before_m2 + 750)

# ==============================================================================
# 2. Weapon Upgrades & Economy (All 4 stats, scaling $200-$3,000, clamping)
# ==============================================================================
func _test_weapon_upgrades_and_economy():
	print("\n--- CHALLENGE 2: WEAPON UPGRADES & ECONOMY STRESS TEST ---")
	
	var save_mgr = root.get_node_or_null("SaveManager")
	var weapon_ids = WeaponManager.get_all_weapon_ids()
	_record_test("Weapon registry has 10 weapons", weapon_ids.size() == 10)

	var stats = ["damage", "mag", "reload", "accuracy"]
	
	# Subtest 2.1: Verify cost scaling strictly within [$200, $3,000] and increasing
	var all_costs_valid = true
	var all_costs_monotonic = true
	var max_level_returns_neg = true
	
	for wid in weapon_ids:
		var wdata = WeaponManager.get_weapon_data(wid)
		if not wdata:
			all_costs_valid = false
			continue
			
		for st in stats:
			var prev_cost = -1
			for lvl in range(5):
				var c = wdata.get_upgrade_cost(st, lvl)
				if c < 200 or c > 3000:
					all_costs_valid = false
					printerr("Cost out of range [%d, %d]: %s %s lvl %d = %d" % [200, 3000, wid, st, lvl, c])
				if lvl > 0 and c <= prev_cost:
					all_costs_monotonic = false
					printerr("Cost not monotonic: %s %s lvl %d (%d) <= lvl %d (%d)" % [wid, st, lvl, c, lvl - 1, prev_cost])
				prev_cost = c
				
			# Check lvl 5 returns -1
			var c_max = wdata.get_upgrade_cost(st, 5)
			if c_max != -1:
				max_level_returns_neg = false
				printerr("Level 5 cost did not return -1: %s %s = %d" % [wid, st, c_max])
				
			# Check can_upgrade returns false at lvl 5 even with infinite cash
			if wdata.can_upgrade(st, 5, 9999999):
				max_level_returns_neg = false
				printerr("can_upgrade returned true at level 5: %s %s" % [wid, st])

	_record_test("Cost scaling in [$200, $3,000] across all 10 weapons & 4 stats", all_costs_valid)
	_record_test("Cost scaling is strictly monotonic per level", all_costs_monotonic)
	_record_test("Level 5 upgrades return -1 and reject can_upgrade", max_level_returns_neg)

	# Subtest 2.2: All 4 stats curve behavior
	var m4 = WeaponManager.get_weapon_data("m4a1")
	var dmg_scales = m4.get_damage(0) < m4.get_damage(1) and m4.get_damage(1) < m4.get_damage(5)
	var mag_scales = m4.get_mag_size(0) < m4.get_mag_size(1) and m4.get_mag_size(1) < m4.get_mag_size(5)
	var reload_scales = m4.get_reload_time(0) > m4.get_reload_time(1) and m4.get_reload_time(1) > m4.get_reload_time(5)
	var spread_scales = m4.get_spread(0) > m4.get_spread(1) and m4.get_spread(1) > m4.get_spread(5)
	var accuracy_scales = m4.get_accuracy(0) < m4.get_accuracy(1) and m4.get_accuracy(1) < m4.get_accuracy(5)
	
	_record_test("Stat curve: Damage increases with level", dmg_scales, "L0: %.1f -> L5: %.1f" % [m4.get_damage(0), m4.get_damage(5)])
	_record_test("Stat curve: Mag size increases with level", mag_scales, "L0: %d -> L5: %d" % [m4.get_mag_size(0), m4.get_mag_size(5)])
	_record_test("Stat curve: Reload time decreases with level", reload_scales, "L0: %.2fs -> L5: %.2fs" % [m4.get_reload_time(0), m4.get_reload_time(5)])
	_record_test("Stat curve: Spread tightens & Accuracy increases", spread_scales and accuracy_scales, "Acc L0: %.1f%% -> L5: %.1f%%" % [m4.get_accuracy(0), m4.get_accuracy(5)])

	# Subtest 2.3: Cash Deduction & Insufficient Cash Rejection
	save_mgr.data.cash = 100
	save_mgr.data.weapon_upgrades = {}
	save_mgr.save_game()
	
	var cost_lvl0 = WeaponManager.get_upgrade_cost("usp45", "damage", save_mgr)
	_record_test("USP-45 damage L0 cost identified", cost_lvl0 >= 200, "Cost: %d" % cost_lvl0)
	
	# Attempt purchase with $100 (< cost)
	var res_fail = WeaponManager.purchase_upgrade("usp45", "damage", save_mgr)
	_record_test("Insufficient cash purchase rejected", res_fail == false)
	_record_test("Cash not deducted on failed purchase", save_mgr.data.cash == 100)
	_record_test("Level unchanged on failed purchase", WeaponManager.get_upgrade_level("usp45", "damage", save_mgr) == 0)

	# Add exact cash for 1 upgrade
	save_mgr.data.cash = cost_lvl0 + 50 # 250
	var res_success = WeaponManager.purchase_upgrade("usp45", "damage", save_mgr)
	_record_test("Sufficient cash purchase succeeds", res_success == true)
	_record_test("Exact cost deducted from cash", save_mgr.data.cash == 50, "Remaining: %d" % save_mgr.data.cash)
	_record_test("Level incremented to 1", WeaponManager.get_upgrade_level("usp45", "damage", save_mgr) == 1)

	# Subtest 2.4: Max Level Clamping (Level 5 Cap)
	save_mgr.data.cash = 100000 # Rich player
	# Buy levels 2, 3, 4, 5
	for expected_lvl in range(2, 6):
		var ok = WeaponManager.purchase_upgrade("usp45", "damage", save_mgr)
		if not ok:
			printerr("Failed to buy expected level %d" % expected_lvl)
	
	var current_lvl = WeaponManager.get_upgrade_level("usp45", "damage", save_mgr)
	_record_test("Upgraded to maximum level 5", current_lvl == 5, "Level: %d" % current_lvl)
	
	# ADVERSARIAL ATTEMPT: Try to upgrade past MAX_UPGRADE_LEVEL (5)
	var cash_before_overcap = save_mgr.data.cash
	var overcap_res = WeaponManager.purchase_upgrade("usp45", "damage", save_mgr)
	_record_test("Over-cap upgrade attempt rejected", overcap_res == false)
	_record_test("Level remains clamped at 5", WeaponManager.get_upgrade_level("usp45", "damage", save_mgr) == 5)
	_record_test("No cash deducted on over-cap attempt", save_mgr.data.cash == cash_before_overcap)

	# Subtest 2.5: Test All 4 Stats Upgraded Concurrently
	var ak = "ak47"
	WeaponManager.unlock_weapon(ak, save_mgr)
	for st in stats:
		var ok = WeaponManager.purchase_upgrade(ak, st, save_mgr)
		_record_test("AK-47 %s upgrade to level 1" % st, ok and WeaponManager.get_upgrade_level(ak, st, save_mgr) == 1)
		
	# Verify all 4 stats are level 1
	var ak_levels = WeaponManager.get_upgrade_levels(ak, save_mgr)
	_record_test("AK-47 all 4 stats recorded in dictionary", 
		ak_levels["damage"] == 1 and ak_levels["mag"] == 1 and ak_levels["reload"] == 1 and ak_levels["accuracy"] == 1)

	# Subtest 2.6: Alias Consistency (usp45 <-> pistol, m4a1 <-> rifle)
	_record_test("Alias consistency: pistol reflects usp45 upgrades", WeaponManager.get_upgrade_level("pistol", "damage", save_mgr) == 5)
	_record_test("Alias consistency: save_mgr helper get_weapon_upgrade", save_mgr.get_weapon_upgrade("pistol", "damage") == 5)

	# Subtest 2.7: Save/Load Persistence of Weapon Upgrades
	save_mgr.save_game()
	save_mgr.load_game()
	_record_test("Persistence: Reload retains max level 5 on usp45", WeaponManager.get_upgrade_level("usp45", "damage", save_mgr) == 5)
	_record_test("Persistence: Reload retains level 1 on ak47 all 4 stats", WeaponManager.get_upgrade_level("ak47", "accuracy", save_mgr) == 1)

# ==============================================================================
# 3. 12-Mission Registry & 3-Wave Progression Stress Test
# ==============================================================================
func _test_12_mission_registry_and_waves():
	print("\n--- CHALLENGE 3: 12-MISSION REGISTRY & 3-WAVE PROGRESSION ---")
	
	var expected_bounties = [500, 750, 1000, 1250, 1500, 1800, 2100, 2500, 3000, 3500, 4000, 6000]
	var all_12_valid = true
	var all_3_waves = true
	var all_chaining_valid = true
	var valid_directions = ["front", "back", "left", "right", "front_left", "front_right", "boss_front"]
	var valid_archetypes = ["normal", "fast", "heavy", "special", "dog", "boss", "rat", "bat"]
	var all_groups_valid = true
	
	for i in range(1, 13):
		var path = "res://resources/missions/mission_%02d.tres" % i
		var m: MissionData = load(path)
		if not m:
			all_12_valid = false
			printerr("Mission %d failed to load: %s" % [i, path])
			continue
			
		if m.wave_count != 3 or m.waves.size() != 3:
			all_3_waves = false
			printerr("Mission %d does not have wave_count=3 and waves.size()=3: count=%d, size=%d" % [i, m.wave_count, m.waves.size()])
			
		var expected_req = "" if i == 1 else ("mission_%02d" % (i - 1))
		if m.unlock_requirement_id != expected_req:
			all_chaining_valid = false
			printerr("Mission %d unlock requirement mismatch: '%s' != '%s'" % [i, m.unlock_requirement_id, expected_req])
			
		if m.reward_cash != expected_bounties[i - 1]:
			all_12_valid = false
			printerr("Mission %d cash mismatch: %d != %d" % [i, m.reward_cash, expected_bounties[i - 1]])
			
		# Check wave contents
		for w_idx in range(m.waves.size()):
			var wave = m.waves[w_idx]
			if not wave.has("groups") or wave["groups"].is_empty():
				all_groups_valid = false
				printerr("Mission %d Wave %d has empty groups" % [i, w_idx + 1])
			for grp in wave.get("groups", []):
				if not grp.get("enemy_type", "") in valid_archetypes:
					all_groups_valid = false
					printerr("Mission %d Wave %d invalid enemy_type: %s" % [i, w_idx + 1, grp.get("enemy_type", "")])
				if grp.get("count", 0) <= 0:
					all_groups_valid = false
					printerr("Mission %d Wave %d count <= 0: %d" % [i, w_idx + 1, grp.get("count", 0)])
				if not grp.get("spawn_direction", "") in valid_directions:
					all_groups_valid = false
					printerr("Mission %d Wave %d invalid spawn_direction: %s" % [i, w_idx + 1, grp.get("spawn_direction", "")])
				if grp.get("delay", -1.0) < 0.0:
					all_groups_valid = false
					printerr("Mission %d Wave %d delay < 0: %f" % [i, w_idx + 1, grp.get("delay", -1.0)])

	_record_test("All 12 missions loaded and valid", all_12_valid)
	_record_test("All 12 missions have wave_count=3 and 3 wave dictionaries", all_3_waves)
	_record_test("All 12 missions have sequential unlock chaining (M1->M12)", all_chaining_valid)
	_record_test("All 12 missions have valid wave groups, enemy types, and directions", all_groups_valid)

	# Subtest 3.2: Verify EventBus signals for wave progression
	var event_bus = root.get_node_or_null("EventBus")
	_record_test("EventBus singleton available", event_bus != null)
	if event_bus:
		var wave_started_received = []
		var wave_cb = func(curr: int, tot: int):
			wave_started_received.append({"current": curr, "total": tot})
		event_bus.wave_started.connect(wave_cb)
		
		# Simulate 3 wave progression signals
		event_bus.wave_started.emit(1, 3)
		event_bus.wave_started.emit(2, 3)
		event_bus.wave_started.emit(3, 3)
		
		_record_test("EventBus.wave_started received 3 wave transitions", wave_started_received.size() == 3)
		_record_test("Wave sequence: (1, 3) -> (2, 3) -> (3, 3)",
			wave_started_received[0]["current"] == 1 and wave_started_received[1]["current"] == 2 and wave_started_received[2]["current"] == 3)
		event_bus.wave_started.disconnect(wave_cb)

# ==============================================================================
# 4. Infected Dog HeadHitZone (2.5x) vs BodyHitZone (1.0x) Stress Test
# ==============================================================================
func _test_infected_dog_hitzones():
	print("\n--- CHALLENGE 4: INFECTED DOG HITZONES (HEAD 2.5x VS BODY 1.0x) ---")
	
	var dog_scene = load("res://scenes/zombies/InfectedDog.tscn")
	_record_test("InfectedDog.tscn exists and loads", dog_scene != null)
	if not dog_scene:
		return
		
	var dog: CharacterBody3D = dog_scene.instantiate()
	_record_test("InfectedDog instance created", dog != null)
	root.add_child(dog)
	await process_frame
	
	# Node setup & tags
	_record_test("Dog is in 'zombies' group", dog.is_in_group("zombies"))
	_record_test("Dog archetype is 'dog'", dog.archetype == "dog")
	_record_test("Dog collision layer is 2 (enemies)", dog.collision_layer == 2)
	
	# Locate HitZones
	var head_zone: HitZone = dog.get_node_or_null("HeadHitZone")
	var body_zone: HitZone = dog.get_node_or_null("BodyHitZone")
	_record_test("HeadHitZone child node exists", head_zone != null)
	_record_test("BodyHitZone child node exists", body_zone != null)
	
	if not head_zone or not body_zone:
		dog.queue_free()
		return
		
	# Multiplier and ZoneType checks
	_record_test("HeadHitZone zone_type == HEAD (0)", head_zone.zone_type == HitZone.ZoneType.HEAD)
	_record_test("HeadHitZone damage_multiplier == 2.5", is_equal_approx(head_zone.damage_multiplier, 2.5))
	_record_test("BodyHitZone zone_type == CHEST (1)", body_zone.zone_type == HitZone.ZoneType.CHEST)
	_record_test("BodyHitZone damage_multiplier == 1.0", is_equal_approx(body_zone.damage_multiplier, 1.0))
	
	# Spatial separation check: Head in front/top, Body centered
	_record_test("HeadHitZone offset matches spec (0, 0.52, -0.45)", head_zone.position.is_equal_approx(Vector3(0, 0.52, -0.45)))
	_record_test("BodyHitZone offset matches spec (0, 0.38, 0.05)", body_zone.position.is_equal_approx(Vector3(0, 0.38, 0.05)))
	
	# Empirical Damage Application Test
	# Initial dog HP is 50.0
	var initial_hp = dog.health_component.current_health
	_record_test("Dog initial HP is 50.0", is_equal_approx(initial_hp, 50.0))
	
	# Apply 10.0 base damage to BodyHitZone -> 1.0x = 10.0 damage dealt
	var r_body = body_zone.take_hit(10.0, Vector3.FORWARD)
	_record_test("BodyHitZone take_hit returns final_damage=10.0", is_equal_approx(r_body["final_damage"], 10.0))
	_record_test("BodyHitZone take_hit returns is_headshot=false", r_body["is_headshot"] == false)
	_record_test("BodyHitZone take_hit returns zone='chest'", r_body["zone"] == "chest")
	_record_test("Dog HP reduced by exactly 10.0 (HP: 40.0)", is_equal_approx(dog.health_component.current_health, 40.0))
	
	# Apply 10.0 base damage to HeadHitZone -> 2.5x = 25.0 damage dealt
	var r_head = head_zone.take_hit(10.0, Vector3.FORWARD)
	_record_test("HeadHitZone take_hit returns final_damage=25.0 (2.5x)", is_equal_approx(r_head["final_damage"], 25.0))
	_record_test("HeadHitZone take_hit returns is_headshot=true", r_head["is_headshot"] == true)
	_record_test("HeadHitZone take_hit returns zone='head'", r_head["zone"] == "head")
	_record_test("Dog HP reduced by exactly 25.0 (HP: 15.0)", is_equal_approx(dog.health_component.current_health, 15.0))
	
	# Lethal blow to Head: 10.0 base -> 25.0 damage (exceeds remaining 15.0 HP)
	var lethal_result = head_zone.take_hit(10.0, Vector3.FORWARD)
	_record_test("Lethal headshot damage dealt", is_equal_approx(lethal_result["final_damage"], 25.0))
	_record_test("Dog enters DEAD state (is_dead=true)", dog.is_dead == true)
	
	dog.queue_free()
