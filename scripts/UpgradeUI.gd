extends Control

@onready var cash_label = $TopBar/CashLabel
@onready var weapon_title = $ContentContainer/Panel/Margin/VBox/WeaponHeader/WeaponTitle
@onready var weapon_subtitle = $ContentContainer/Panel/Margin/VBox/WeaponHeader/WeaponSubtitle

# Damage nodes
@onready var dmg_level_lbl = $ContentContainer/Panel/Margin/VBox/DamageRow/LabelBox/LevelLbl
@onready var dmg_progress = $ContentContainer/Panel/Margin/VBox/DamageRow/StatBox/ProgressBar
@onready var dmg_diff_lbl = $ContentContainer/Panel/Margin/VBox/DamageRow/StatBox/StatDiff
@onready var dmg_btn = $ContentContainer/Panel/Margin/VBox/DamageRow/UpgradeBtn

# Mag nodes
@onready var mag_level_lbl = $ContentContainer/Panel/Margin/VBox/MagRow/LabelBox/LevelLbl
@onready var mag_progress = $ContentContainer/Panel/Margin/VBox/MagRow/StatBox/ProgressBar
@onready var mag_diff_lbl = $ContentContainer/Panel/Margin/VBox/MagRow/StatBox/StatDiff
@onready var mag_btn = $ContentContainer/Panel/Margin/VBox/MagRow/UpgradeBtn

# Reload nodes
@onready var reload_level_lbl = $ContentContainer/Panel/Margin/VBox/ReloadRow/LabelBox/LevelLbl
@onready var reload_progress = $ContentContainer/Panel/Margin/VBox/ReloadRow/StatBox/ProgressBar
@onready var reload_diff_lbl = $ContentContainer/Panel/Margin/VBox/ReloadRow/StatBox/StatDiff
@onready var reload_btn = $ContentContainer/Panel/Margin/VBox/ReloadRow/UpgradeBtn

# Accuracy nodes
@onready var acc_row = get_node_or_null("ContentContainer/Panel/Margin/VBox/AccuracyRow")
@onready var acc_level_lbl = get_node_or_null("ContentContainer/Panel/Margin/VBox/AccuracyRow/LabelBox/LevelLbl")
@onready var acc_progress = get_node_or_null("ContentContainer/Panel/Margin/VBox/AccuracyRow/StatBox/ProgressBar")
@onready var acc_diff_lbl = get_node_or_null("ContentContainer/Panel/Margin/VBox/AccuracyRow/StatBox/StatDiff")
@onready var acc_btn = get_node_or_null("ContentContainer/Panel/Margin/VBox/AccuracyRow/UpgradeBtn")

var current_weapon_id: String = "m4a1"

var weapon_resources = {
	"usp45": "res://resources/weapons/usp45.tres",
	"pistol": "res://resources/weapons/pistol.tres",
	"m4a1": "res://resources/weapons/m4a1.tres",
	"rifle": "res://resources/weapons/rifle.tres",
	"remington870": "res://resources/weapons/remington870.tres",
	"shotgun": "res://resources/weapons/shotgun.tres",
	"ak47": "res://resources/weapons/ak47.tres",
	"desert_eagle": "res://resources/weapons/desert_eagle.tres",
	"mp5": "res://resources/weapons/mp5.tres",
	"awp": "res://resources/weapons/awp.tres",
	"combat_knife": "res://resources/weapons/combat_knife.tres",
	"crossbow": "res://resources/weapons/crossbow.tres",
	"grenade_launcher": "res://resources/weapons/grenade_launcher.tres",
	"heavy_gun": "res://resources/weapons/heavy_gun.tres"
}

var weapon_subtitles = {
	"usp45": "Tactical .45 ACP Sidearm - Reliable Critical Headshots",
	"pistol": "Tactical .45 ACP Sidearm - Reliable Critical Headshots",
	"m4a1": "5.56 NATO Tactical Carbine - High Cyclic Fire Rate",
	"rifle": "5.56 NATO Tactical Carbine - High Cyclic Fire Rate",
	"remington870": "12-Gauge Pump Action - Lethal Close-Quarters Spread",
	"shotgun": "12-Gauge Pump Action - Lethal Close-Quarters Spread",
	"ak47": "7.62x39mm Combat Rifle - Heavy Kinetic Punch",
	"desert_eagle": ".50 Action Express Hand Cannon - Devastating Stopping Power",
	"mp5": "9mm Submachine Gun - Ultra Fast Cyclic Fire Rate",
	"awp": ".338 Lapua Bolt-Action Sniper - Extreme Range One-Shot Lethality",
	"combat_knife": "Serrated Tanto Blade - Silent Rapid Melee Takedowns",
	"crossbow": "Composite Bolt Thrower - High-Tension Silent Piercing",
	"grenade_launcher": "40mm Area Ordinance - High-Explosive Crowd Annihilation"
}

const MAX_LEVEL = 5

func _ready():
	var gsm = get_node_or_null("/root/GameStateManager")
	if gsm:
		gsm.change_state(gsm.State.UPGRADES)
	update_ui()
	print("[%d ms] [UPGRADES] UpgradeUI ready." % Time.get_ticks_msec())

func _on_tab_pressed(wid: String):
	current_weapon_id = wid
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	update_ui()

func update_ui():
	var save_mgr = get_node_or_null("/root/SaveManager")
	var cash = save_mgr.data.cash if save_mgr else 0
	cash_label.text = "CASH $: $%d" % cash
	
	var res_path = weapon_resources.get(current_weapon_id, "")
	if res_path == "" or not ResourceLoader.exists(res_path):
		res_path = "res://resources/weapons/m4a1.tres"
	var data = load(res_path) as WeaponData
	if not data: return
	
	weapon_title.text = data.display_name.to_upper()
	weapon_subtitle.text = weapon_subtitles.get(current_weapon_id, data.display_name)
	
	var upgrades_dict = {}
	if save_mgr:
		upgrades_dict = WeaponManager.get_upgrade_levels(current_weapon_id, save_mgr)
	var lvl_dmg: int = upgrades_dict.get("damage", 0)
	var lvl_mag: int = upgrades_dict.get("mag", 0)
	var lvl_rel: int = upgrades_dict.get("reload", 0)
	var lvl_acc: int = upgrades_dict.get("accuracy", 0)
	
	# Handle Unlocks
	var vbox = $ContentContainer/Panel/Margin/VBox
	var unlock_btn = get_node_or_null("UnlockBtn")
	if not unlock_btn:
		unlock_btn = Button.new()
		unlock_btn.name = "UnlockBtn"
		unlock_btn.custom_minimum_size = Vector2(0, 80)
		unlock_btn.add_theme_font_size_override("font_size", 20)
		$ContentContainer/Panel/Margin.add_child(unlock_btn)
		unlock_btn.pressed.connect(_on_unlock_pressed)
		
	var is_unlocked = WeaponManager.is_weapon_unlocked(current_weapon_id, save_mgr) if save_mgr else true
	if is_unlocked:
		vbox.visible = true
		unlock_btn.visible = false
	else:
		vbox.visible = false
		unlock_btn.visible = true
		var price = data.unlock_price if data.unlock_price > 0 else 1500
		unlock_btn.text = "UNLOCK " + data.display_name.to_upper() + "\n(Price: $" + str(price) + ")"
		unlock_btn.disabled = (cash < price)
		
	# 1. Damage Row
	dmg_level_lbl.text = "LVL %d / %d" % [lvl_dmg, MAX_LEVEL]
	dmg_progress.max_value = float(MAX_LEVEL)
	dmg_progress.value = float(lvl_dmg)
	var cur_dmg = data.get_damage(lvl_dmg)
	var next_dmg = data.get_damage(lvl_dmg + 1)
	if lvl_dmg >= MAX_LEVEL:
		dmg_diff_lbl.text = "%.1f DMG (MAX)" % cur_dmg
		dmg_btn.text = "MAX LEVEL"
		dmg_btn.disabled = true
	else:
		var cost = data.get_upgrade_cost("damage", lvl_dmg)
		dmg_diff_lbl.text = "%.1f -> %.1f DMG" % [cur_dmg, next_dmg]
		if cash < cost:
			dmg_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			dmg_btn.disabled = true
		else:
			dmg_btn.text = "UPGRADE ($%d)" % cost
			dmg_btn.disabled = false
			
	# 2. Mag Row
	mag_level_lbl.text = "LVL %d / %d" % [lvl_mag, MAX_LEVEL]
	mag_progress.max_value = float(MAX_LEVEL)
	mag_progress.value = float(lvl_mag)
	var cur_mag = data.get_mag_size(lvl_mag)
	var next_mag = data.get_mag_size(lvl_mag + 1)
	if lvl_mag >= MAX_LEVEL:
		mag_diff_lbl.text = "%d ROUNDS (MAX)" % cur_mag
		mag_btn.text = "MAX LEVEL"
		mag_btn.disabled = true
	else:
		var cost = data.get_upgrade_cost("mag", lvl_mag)
		mag_diff_lbl.text = "%d -> %d ROUNDS" % [cur_mag, next_mag]
		if cash < cost:
			mag_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			mag_btn.disabled = true
		else:
			mag_btn.text = "UPGRADE ($%d)" % cost
			mag_btn.disabled = false
			
	# 3. Reload Row
	reload_level_lbl.text = "LVL %d / %d" % [lvl_rel, MAX_LEVEL]
	reload_progress.max_value = float(MAX_LEVEL)
	reload_progress.value = float(lvl_rel)
	var cur_rel = data.get_reload_time(lvl_rel)
	var next_rel = data.get_reload_time(lvl_rel + 1)
	if lvl_rel >= MAX_LEVEL:
		reload_diff_lbl.text = "%.2fs (MAX)" % cur_rel
		reload_btn.text = "MAX LEVEL"
		reload_btn.disabled = true
	else:
		var cost = data.get_upgrade_cost("reload", lvl_rel)
		reload_diff_lbl.text = "%.2fs -> %.2fs" % [cur_rel, next_rel]
		if cash < cost:
			reload_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			reload_btn.disabled = true
		else:
			reload_btn.text = "UPGRADE ($%d)" % cost
			reload_btn.disabled = false

	# 4. Accuracy Row
	if acc_row and acc_level_lbl and acc_progress and acc_diff_lbl and acc_btn:
		acc_level_lbl.text = "LVL %d / %d" % [lvl_acc, MAX_LEVEL]
		acc_progress.max_value = float(MAX_LEVEL)
		acc_progress.value = float(lvl_acc)
		var cur_acc = data.get_accuracy(lvl_acc)
		var next_acc = data.get_accuracy(lvl_acc + 1)
		if lvl_acc >= MAX_LEVEL:
			acc_diff_lbl.text = "%.0f%% ACCURACY (MAX)" % cur_acc
			acc_btn.text = "MAX LEVEL"
			acc_btn.disabled = true
		else:
			var cost = data.get_upgrade_cost("accuracy", lvl_acc)
			acc_diff_lbl.text = "%.0f%% -> %.0f%% ACCURACY" % [cur_acc, next_acc]
			if cash < cost:
				acc_btn.text = "NOT ENOUGH CASH ($%d)" % cost
				acc_btn.disabled = true
			else:
				acc_btn.text = "UPGRADE ($%d)" % cost
				acc_btn.disabled = false

func _on_unlock_pressed():
	var save_mgr = get_node_or_null("/root/SaveManager")
	if not save_mgr: return
	
	var res_path = weapon_resources.get(current_weapon_id, "")
	var data = load(res_path) as WeaponData
	var price = data.unlock_price if data and data.unlock_price > 0 else 1500
	
	if save_mgr.data.cash >= price:
		save_mgr.add_cash(-price)
		WeaponManager.unlock_weapon(current_weapon_id, save_mgr)
		var audio_mgr = get_node_or_null("/root/AudioManager")
		if audio_mgr: audio_mgr.play_ui_click()
		update_ui()

func _on_upgrade_pressed(type: String):
	var save_mgr = get_node_or_null("/root/SaveManager")
	if not save_mgr: return
	
	var success = WeaponManager.purchase_upgrade(current_weapon_id, type, save_mgr)
	if success:
		var audio_mgr = get_node_or_null("/root/AudioManager")
		if audio_mgr: audio_mgr.play_ui_click()
		update_ui()

func _on_back_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	var gsm = get_node_or_null("/root/GameStateManager")
	if gsm:
		gsm.change_state(gsm.State.MISSION_SELECT)
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
