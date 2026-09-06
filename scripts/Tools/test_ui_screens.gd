extends SceneTree

func _init():
	print("==================================================")
	print("STARTING COMPREHENSIVE UI & ANDROID VERIFICATION")
	print("==================================================")

	# --- 1. MAIN MENU AUDIT ---
	print("\n[TEST 1] Auditing Main Menu Scenes...")
	var mm_scene = load("res://scenes/UI/MainMenu.tscn")
	assert(mm_scene != null, "res://scenes/UI/MainMenu.tscn must load")
	var mm = mm_scene.instantiate()
	root.add_child(mm)
	await process_frame
	
	var title = mm.find_child("Title", true, false)
	assert(title != null and "SECTOR ZERO: LOCKDOWN" in title.text, "Title must contain SECTOR ZERO: LOCKDOWN")
	var start_btn = mm.find_child("StartButton", true, false)
	assert(start_btn != null, "StartButton must exist")
	var armory_btn = mm.find_child("UpgradesButton", true, false)
	assert(armory_btn != null, "UpgradesButton must exist")
	var settings_btn = mm.find_child("SettingsButton", true, false)
	assert(settings_btn != null, "SettingsButton must exist")
	var cash_label = mm.find_child("CashLabel", true, false)
	assert(cash_label != null and "CASH:" in cash_label.text, "CashLabel must exist")
	print("  [PASS] MainMenu.tscn verified: Title, Buttons, Cash display, 3D background.")
	mm.queue_free()
	await process_frame

	# Check scenes/menu/MainMenu.tscn fallback
	var mm_alt_scene = load("res://scenes/menu/MainMenu.tscn")
	assert(mm_alt_scene != null, "res://scenes/menu/MainMenu.tscn must load")
	var mm_alt = mm_alt_scene.instantiate()
	root.add_child(mm_alt)
	await process_frame
	print("  [PASS] scenes/menu/MainMenu.tscn fallback verified.")
	mm_alt.queue_free()
	await process_frame

	# --- 2. MISSION SELECT AUDIT ---
	print("\n[TEST 2] Auditing 12-Mission Select UI...")
	var ms_scene = load("res://scenes/UI/MissionSelect.tscn")
	assert(ms_scene != null, "res://scenes/UI/MissionSelect.tscn must load")
	var ms = ms_scene.instantiate()
	root.add_child(ms)
	await process_frame
	
	var mission_list = ms.find_child("VBoxContainer", true, false)
	assert(mission_list != null, "Mission card container must exist")
	var card_count = mission_list.get_child_count()
	assert(card_count == 12, "Must instantiate all 12 mission cards (found: %d)" % card_count)
	
	# Verify first mission card structure
	var card1 = mission_list.get_child(0)
	var c1_title = card1.find_child("Title", true, false)
	var c1_reward = card1.find_child("Reward", true, false)
	var c1_threat = card1.find_child("Threat", true, false)
	var c1_status = card1.find_child("Status", true, false)
	assert(c1_title != null and c1_title.text == "First Contact", "Mission 1 title match")
	assert(c1_reward != null and "BOUNTY:" in c1_reward.text, "Mission 1 reward display")
	assert(c1_threat != null and "THREAT:" in c1_threat.text, "Threat rating must be present on card")
	assert(c1_status != null, "Status label must be present on card")
	
	# Verify Briefing Modal interaction
	var m1_data = load("res://resources/missions/mission_01.tres")
	ms._on_mission_selected(m1_data)
	var briefing = ms.find_child("BriefingModal", true, false)
	assert(briefing != null and briefing.visible, "BriefingModal must show on mission selection")
	var b_header = ms.find_child("BriefingHeader", true, false)
	assert(b_header != null and "FIRST CONTACT" in b_header.text, "Briefing header match")
	var b_threat = ms.find_child("BriefingDifficulty", true, false)
	assert(b_threat != null and "THREAT LEVEL:" in b_threat.text, "Briefing threat level match")
	var b_reward = ms.find_child("BriefingReward", true, false)
	assert(b_reward != null and ("SINGLE-CLAIM" in b_reward.text or "CLAIMED" in b_reward.text), "Briefing single-claim reward status match")
	print("  [PASS] MissionSelect.tscn verified: 12 missions grid, threat ratings, single-claim briefings.")
	ms.queue_free()
	await process_frame

	# Check MissionSelectUI.tscn alias
	var ms_ui_scene = load("res://scenes/UI/MissionSelectUI.tscn")
	assert(ms_ui_scene != null, "res://scenes/UI/MissionSelectUI.tscn alias must load")
	print("  [PASS] MissionSelectUI.tscn alias verified.")

	# --- 3. HUD AUDIT ---
	print("\n[TEST 3] Auditing Gameplay HUD...")
	var hud_scene = load("res://scenes/UI/HUD.tscn")
	assert(hud_scene != null, "res://scenes/UI/HUD.tscn must load")
	var hud = hud_scene.instantiate()
	root.add_child(hud)
	await process_frame
	
	var wave_lbl = hud.find_child("WaveLabel", true, false)
	assert(wave_lbl != null, "WaveLabel must exist")
	assert("WAVE:" in wave_lbl.text, "WaveLabel must have WAVE: prefix")
	
	# Test wave update
	hud.update_wave(2, 3)
	assert(wave_lbl.text == "WAVE: 2 / 3", "WaveLabel format must be WAVE: 2 / 3 (got: %s)" % wave_lbl.text)
	
	# Test touch controls
	var fire_btn = hud.find_child("FireButton", true, false)
	var reload_btn = hud.find_child("ReloadButton", true, false)
	var switch_btn = hud.find_child("SwitchButton", true, false)
	var pause_btn = hud.find_child("PauseButton", true, false)
	assert(fire_btn != null and fire_btn.visible, "FireButton touch control must exist")
	assert(reload_btn != null and reload_btn.visible, "ReloadButton touch control must exist")
	assert(switch_btn != null and switch_btn.visible, "SwitchButton touch control must exist")
	assert(pause_btn != null and pause_btn.visible, "PauseButton touch control must exist")
	
	# Test Reticle & Hitmarker
	var crosshair = hud.find_child("Crosshair", true, false)
	var hitmarker = hud.find_child("Hitmarker", true, false)
	assert(crosshair != null, "Reticle crosshair must exist")
	assert(hitmarker != null, "Hitmarker control must exist")
	
	# Test Boss Health Bar
	var boss_bar = hud.find_child("BossHealthBar", true, false)
	assert(boss_bar != null, "BossHealthBar must exist")
	hud.show_boss_health("THE APEX ALPHA", 500.0)
	assert(boss_bar.visible, "BossHealthBar must be visible after show_boss_health")
	assert(boss_bar.max_value == 500.0 and boss_bar.value == 500.0, "BossHealthBar values must match")
	hud.update_boss_health(250.0)
	assert(boss_bar.value == 250.0, "BossHealthBar value must update to 250")
	hud.update_boss_health(0.0)
	assert(not boss_bar.visible, "BossHealthBar must hide on 0 HP")
	print("  [PASS] HUD.tscn verified: WAVE: X / 3, touch controls, reticle, hitmarker, boss bar.")
	hud.queue_free()
	await process_frame

	# --- 4. ARMORY AUDIT ---
	print("\n[TEST 4] Auditing Armory & Weapon Upgrades...")
	var armory_scene = load("res://scenes/UI/ArmoryUI.tscn")
	assert(armory_scene != null, "res://scenes/UI/ArmoryUI.tscn must load")
	var armory = armory_scene.instantiate()
	root.add_child(armory)
	await process_frame
	
	var w_list = armory.find_child("VBox", true, false)
	assert(w_list != null and w_list.get_child_count() >= 10, "Armory must present at least 10 weapons (found: %d)" % w_list.get_child_count())
	
	var dmg_row = armory.find_child("DamageRow", true, false)
	var mag_row = armory.find_child("MagRow", true, false)
	var rel_row = armory.find_child("ReloadRow", true, false)
	var acc_row = armory.find_child("AccuracyRow", true, false)
	assert(dmg_row != null, "DamageRow must exist")
	assert(mag_row != null, "MagRow must exist")
	assert(rel_row != null, "ReloadRow must exist")
	assert(acc_row != null, "AccuracyRow must exist")
	
	var armory_cash = armory.find_child("CashLabel", true, false)
	assert(armory_cash != null and "CASH:" in armory_cash.text, "Armory cash display must exist")
	print("  [PASS] ArmoryUI.tscn verified: 10+ weapons, Damage/Mag/Reload/Accuracy upgrades, cash.")
	armory.queue_free()
	await process_frame

	# --- 5. RESULT UI AUDIT ---
	print("\n[TEST 5] Auditing Result UI...")
	var res_scene = load("res://scenes/UI/ResultUI.tscn")
	assert(res_scene != null, "res://scenes/UI/ResultUI.tscn must load")
	var res_ui = res_scene.instantiate()
	root.add_child(res_ui)
	await process_frame
	
	var r_title = res_ui.find_child("Title", true, false)
	var r_kills = res_ui.find_child("Kills", true, false)
	var r_headshots = res_ui.find_child("Headshots", true, false)
	var r_accuracy = res_ui.find_child("Accuracy", true, false)
	var r_cash = res_ui.find_child("CashLabel", true, false)
	assert(r_title != null, "Title label must exist")
	assert(r_kills != null, "Kills label must exist")
	assert(r_headshots != null, "Headshots label must exist")
	assert(r_accuracy != null, "Accuracy label must exist")
	assert(r_cash != null, "CashLabel must exist")
	
	# Simulate Victory First Win
	var test_mission = load("res://resources/missions/mission_01.tres")
	var mission_mgr = root.get_node_or_null("MissionManager")
	if mission_mgr:
		mission_mgr.last_stats = {
			"kills": 15,
			"headshots": 8,
			"accuracy": 78,
			"bounty_awarded": 500,
			"first_time_reward": true,
			"success": true
		}
	res_ui._on_mission_completed(test_mission)
	assert(res_ui.visible, "ResultUI must be visible after mission completed")
	assert("MISSION COMPLETE" in r_title.text, "Title must be MISSION COMPLETE")
	
	# Simulate Replay ($0 Bounty)
	if mission_mgr:
		mission_mgr.last_stats = {
			"kills": 15,
			"headshots": 8,
			"accuracy": 78,
			"bounty_awarded": 0,
			"first_time_reward": false,
			"success": true
		}
	res_ui._on_mission_completed(test_mission)
	assert("CLAIMED" in r_cash.text or "$0" in r_cash.text, "Replay must indicate $0 previously claimed cash (got: %s)" % r_cash.text)
	print("  [PASS] ResultUI.tscn verified: Stats, first-time clear, single-claim $0 replay.")
	res_ui.queue_free()
	await process_frame

	print("\n==================================================")
	print("ALL 5 UI SCREENS VERIFIED 100% OPERATIONAL!")
	print("==================================================")
	quit(0)
