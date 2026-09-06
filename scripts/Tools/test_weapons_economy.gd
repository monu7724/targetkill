extends SceneTree

func _init():
	print("\n==================================================")
	print("TEST SUITE: WEAPONS & ECONOMY VERIFICATION")
	print("==================================================")
	
	var results = {"passed": 0, "failed": 0}
	
	var test = func(name: String, condition: bool, details: String = ""):
		if condition:
			results["passed"] += 1
			print("[PASS] %s %s" % [name, ("(" + details + ")") if details != "" else ""])
		else:
			results["failed"] += 1
			printerr("[FAIL] %s %s" % [name, ("(" + details + ")") if details != "" else ""])

	# 1. Weapon Registry & Data Integrity
	print("\n--- TEST 1: 10 DISTINCT WEAPONS DATA & MODELS ---")
	var weapon_ids = WeaponManager.get_all_weapon_ids()
	test.call("Weapon Count", weapon_ids.size() == 10, "Found %d weapons" % weapon_ids.size())
	
	var damages = []
	var fire_rates = []
	var mag_sizes = []
	var reload_times = []
	
	for wid in weapon_ids:
		var data = WeaponManager.get_weapon_data(wid)
		var has_data = data != null
		test.call("Weapon Data: " + wid, has_data, "Display: %s" % (data.display_name if has_data else "None"))
		
		if has_data:
			damages.append(data.base_damage)
			fire_rates.append(data.base_fire_rate)
			mag_sizes.append(data.base_mag_size)
			reload_times.append(data.base_reload_time)
			
			# Check 3D GLB file
			var glb_path = "res://assets/3d/weapons/%s.glb" % wid
			var glb_exists = FileAccess.file_exists(glb_path)
			test.call("3D Model GLB: " + wid, glb_exists, glb_path)
			
			# Check Weapon Scene
			var scene = WeaponManager.get_weapon_scene(wid)
			test.call("Weapon Scene: " + wid, scene != null, "Scene loaded")

	# Verify distinct stats
	var unique_damages = {}
	for d in damages: unique_damages[d] = true
	test.call("Distinct Damage Stats", unique_damages.size() >= 7, "%d unique damages among 10 weapons" % unique_damages.size())

	# 2. 4 Upgrade Paths Verification
	print("\n--- TEST 2: 4 UPGRADE PATHS (DAMAGE, MAG, RELOAD, ACCURACY) ---")
	var m4 = WeaponManager.get_weapon_data("m4a1")
	test.call("M4A1 Base Damage", is_equal_approx(m4.get_damage(0), m4.base_damage), "Base: %.1f" % m4.base_damage)
	test.call("M4A1 Level 1 Damage (+18%)", m4.get_damage(1) > m4.get_damage(0), "L0: %.1f -> L1: %.1f" % [m4.get_damage(0), m4.get_damage(1)])
	test.call("M4A1 Level 5 Damage Max", m4.get_damage(5) > m4.get_damage(4), "L5: %.1f" % m4.get_damage(5))
	
	test.call("M4A1 Base Mag", m4.get_mag_size(0) == m4.base_mag_size, "Base Mag: %d" % m4.base_mag_size)
	test.call("M4A1 Upgraded Mag", m4.get_mag_size(2) > m4.get_mag_size(0), "L0: %d -> L2: %d" % [m4.get_mag_size(0), m4.get_mag_size(2)])
	
	test.call("M4A1 Base Reload", is_equal_approx(m4.get_reload_time(0), m4.base_reload_time), "Base Reload: %.2fs" % m4.base_reload_time)
	test.call("M4A1 Upgraded Reload", m4.get_reload_time(3) < m4.get_reload_time(0), "L0: %.2fs -> L3: %.2fs" % [m4.get_reload_time(0), m4.get_reload_time(3)])
	
	test.call("M4A1 Base Spread", is_equal_approx(m4.get_spread(0), m4.spread), "Base Spread: %.4f" % m4.spread)
	test.call("M4A1 Upgraded Spread (Tightened)", m4.get_spread(3) < m4.get_spread(0), "L0: %.4f -> L3: %.4f" % [m4.get_spread(0), m4.get_spread(3)])
	test.call("M4A1 Accuracy Scaling", m4.get_accuracy(3) > m4.get_accuracy(0), "L0: %.1f%% -> L3: %.1f%%" % [m4.get_accuracy(0), m4.get_accuracy(3)])

	# 3. Upgrade Cost Curves ($200 to $3,000)
	print("\n--- TEST 3: UPGRADE COST CURVES ($200 - $3,000) ---")
	var all_costs_in_range = true
	var cost_progression_ok = true
	for wid in weapon_ids:
		var wdata = WeaponManager.get_weapon_data(wid)
		for stat in ["damage", "mag", "reload", "accuracy"]:
			var prev_cost = 0
			for lvl in range(WeaponData.MAX_UPGRADE_LEVEL):
				var cost = wdata.get_upgrade_cost(stat, lvl)
				if cost < 200 or cost > 3000:
					all_costs_in_range = false
					printerr("Cost out of range: %s %s lvl %d = %d" % [wid, stat, lvl, cost])
				if lvl > 0 and cost <= prev_cost:
					cost_progression_ok = false
				prev_cost = cost
			# Beyond max level
			var max_cost = wdata.get_upgrade_cost(stat, WeaponData.MAX_UPGRADE_LEVEL)
			if max_cost != -1:
				all_costs_in_range = false
	test.call("All Upgrade Costs Within $200 - $3,000", all_costs_in_range, "All 10 weapons, 4 stats, 5 levels")
	test.call("Monotonically Increasing Cost Progression", cost_progression_ok, "Curves scale progressively per level")

	# 4. SaveManager & Economy Integration
	print("\n--- TEST 4: SAVEMANAGER & CASH ECONOMY INTEGRATION ---")
	var save_mgr = root.get_node_or_null("SaveManager")
	if not save_mgr:
		var sm_script = load("res://scripts/SaveManager.gd")
		save_mgr = sm_script.new()
		root.add_child(save_mgr)
		
	# Reset test state
	save_mgr.data.cash = 5000
	save_mgr.data.unlocked_weapons = ["pistol", "rifle", "shotgun"]
	save_mgr.save_game()
	
	test.call("Pistol is unlocked by default", save_mgr.is_weapon_unlocked("pistol"))
	test.call("USP-45 alias is recognized unlocked", save_mgr.is_weapon_unlocked("usp45"))
	test.call("AWP is locked initially", not save_mgr.is_weapon_unlocked("awp"))
	
	# Purchase weapon with cash
	var awp_price = WeaponManager.get_weapon_entry("awp").unlock_price
	var cash_before = save_mgr.data.cash
	var unlocked_awp = WeaponManager.purchase_weapon("awp", save_mgr)
	test.call("Purchase AWP with Cash", unlocked_awp and save_mgr.is_weapon_unlocked("awp"), "Cash: %d -> %d" % [cash_before, save_mgr.data.cash])
	test.call("Cash Deducted Correctly", save_mgr.data.cash == cash_before - awp_price, "Deducted: $%d" % awp_price)
	
	# Purchase upgrade with cash
	var deagle_dmg_cost = WeaponManager.get_upgrade_cost("desert_eagle", "damage", save_mgr)
	var cash_pre_upg = save_mgr.data.cash
	var upg_ok = WeaponManager.purchase_upgrade("desert_eagle", "damage", save_mgr)
	test.call("Purchase Deagle Damage Upgrade", upg_ok, "Cost: $%d" % deagle_dmg_cost)
	test.call("Upgrade Level Incremented to 1", WeaponManager.get_upgrade_level("desert_eagle", "damage", save_mgr) == 1)
	test.call("Cash Deducted for Upgrade", save_mgr.data.cash == cash_pre_upg - deagle_dmg_cost)

	# Test Persistence
	print("\n--- TEST 5: PERSISTENCE (SAVE & LOAD) ---")
	save_mgr.save_game()
	save_mgr.data.cash = 0
	save_mgr.data.unlocked_weapons = []
	save_mgr.data.weapon_upgrades = {}
	save_mgr.load_game()
	test.call("Loaded AWP Unlock State", save_mgr.is_weapon_unlocked("awp"))
	test.call("Loaded Deagle Damage Upgrade Level 1", save_mgr.get_weapon_upgrade("desert_eagle", "damage") == 1)
	test.call("Loaded Cash Correctly", save_mgr.data.cash == cash_pre_upg - deagle_dmg_cost)

	# 5. Combat & Instantiation Execution
	print("\n--- TEST 6: RUNTIME WEAPON INSTANTIATION & BEHAVIOR ---")
	var knife_scene = WeaponManager.get_weapon_scene("combat_knife")
	var knife = knife_scene.instantiate()
	root.add_child(knife)
	knife._ready()
	knife.shoot()
	test.call("Combat Knife Melee Fire", knife.current_ammo == 1, "Melee knife maintains readiness")
	knife.queue_free()

	var awp_scene = WeaponManager.get_weapon_scene("awp")
	var awp = awp_scene.instantiate()
	root.add_child(awp)
	awp._ready()
	var awp_init_ammo = awp.current_ammo
	awp.shoot()
	test.call("AWP Fire Consumes Ammo", awp.current_ammo == awp_init_ammo - 1, "Ammo: %d -> %d" % [awp_init_ammo, awp.current_ammo])
	awp.queue_free()

	var gl_scene = WeaponManager.get_weapon_scene("grenade_launcher")
	var gl = gl_scene.instantiate()
	root.add_child(gl)
	gl._ready()
	test.call("Grenade Launcher Area Damage Method Ready", gl.has_method("_apply_area_explosion"))
	gl.queue_free()

	print("\n==================================================")
	print("WEAPONS & ECONOMY TEST SUMMARY: %d PASSED, %d FAILED" % [results["passed"], results["failed"]])
	print("==================================================")
	
	if results["failed"] > 0:
		quit(1)
	else:
		quit(0)

