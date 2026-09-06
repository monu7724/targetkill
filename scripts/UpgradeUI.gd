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

# Tabs
@onready var pistol_tab = $ContentContainer/TabsBar/PistolTab
@onready var rifle_tab = $ContentContainer/TabsBar/RifleTab
@onready var shotgun_tab = $ContentContainer/TabsBar/ShotgunTab
@onready var heavy_gun_tab = $ContentContainer/TabsBar/HeavyGunTab

var current_weapon_id: String = "rifle"

var weapon_resources = {
	"pistol": "res://resources/weapons/pistol.tres",
	"rifle": "res://resources/weapons/rifle.tres",
	"shotgun": "res://resources/weapons/shotgun.tres",
	"heavy_gun": "res://resources/weapons/heavy_gun.tres",
	"heavy_m134": "res://resources/weapons/heavy_m134.tres",
	"heavy_rpg7": "res://resources/weapons/heavy_rpg7.tres",
	"heavy_rpd": "res://resources/weapons/heavy_rpd.tres",
	"heavy_mg42": "res://resources/weapons/heavy_mg42.tres",
	"heavy_l86": "res://resources/weapons/heavy_l86.tres",
	"heavy_m249": "res://resources/weapons/heavy_m249.tres",
	"heavy_pkm": "res://resources/weapons/heavy_pkm.tres",
	"heavy_m60": "res://resources/weapons/heavy_m60.tres",
	"heavy_m2browning": "res://resources/weapons/heavy_m2browning.tres",
	"heavy_flamethrower": "res://resources/weapons/heavy_flamethrower.tres"

}

var weapon_subtitles = {
	"pistol": "Tactical .45 ACP Sidearm - Reliable Critical Headshots",
	"rifle": "5.56 NATO Tactical Carbine - High Cyclic Fire Rate",
	"shotgun": "12-Gauge Pump Action - Lethal Close-Quarters Spread",
	"heavy_gun": "5.56 NATO Light Machine Gun - Massive Magazine Capacity"
}

const MAX_LEVEL = 3

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
	
	# Update tab states
	
	var res_path = weapon_resources.get(current_weapon_id, "")
	var data = load(res_path)
	if not data: return
	
	weapon_title.text = data.display_name.to_upper()
	weapon_subtitle.text = weapon_subtitles.get(current_weapon_id, "")
	
	var upgrades_dict = save_mgr.data.weapon_upgrades.get(current_weapon_id, {}) if save_mgr else {}
	var lvl_dmg: int = upgrades_dict.get("damage", 0)
	var lvl_mag: int = upgrades_dict.get("mag", 0)
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
		
	if current_weapon_id in save_mgr.data.unlocked_weapons:
		vbox.visible = true
		unlock_btn.visible = false
	else:
		vbox.visible = false
		unlock_btn.visible = true
		unlock_btn.text = "WATCH AD TO UNLOCK " + data.display_name.to_upper() + "\n(Or Buy for $5000)"
		
	# 1. Damage Row
	dmg_level_lbl.text = "LVL %d / %d" % [lvl_dmg, MAX_LEVEL]
	dmg_progress.value = float(lvl_dmg)
	var base_dmg = data.base_damage
	var cur_dmg = base_dmg * (1.0 + lvl_dmg * 0.2)
	var next_dmg = base_dmg * (1.0 + (lvl_dmg + 1) * 0.2)
	if lvl_dmg >= MAX_LEVEL:
		dmg_diff_lbl.text = "%.0f DMG (MAX)" % cur_dmg
		dmg_btn.text = "MAX LEVEL"
		dmg_btn.disabled = true
	else:
		var cost = data.upgrade_cost_damage * (lvl_dmg + 1)
		dmg_diff_lbl.text = "%.0f -> %.0f DMG (+20%%)" % [cur_dmg, next_dmg]
		if cash < cost:
			dmg_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			dmg_btn.disabled = true
		else:
			dmg_btn.text = "UPGRADE ($%d)" % cost
			dmg_btn.disabled = false
			
	# 2. Mag Row
	mag_level_lbl.text = "LVL %d / %d" % [lvl_mag, MAX_LEVEL]
	mag_progress.value = float(lvl_mag)
	var base_mag = data.base_mag_size
	var cur_mag = base_mag + (lvl_mag * int(base_mag * 0.25))
	var next_mag = base_mag + ((lvl_mag + 1) * int(base_mag * 0.25))
	if lvl_mag >= MAX_LEVEL:
		mag_diff_lbl.text = "%d ROUNDS (MAX)" % cur_mag
		mag_btn.text = "MAX LEVEL"
		mag_btn.disabled = true
	else:
		var cost = data.upgrade_cost_mag * (lvl_mag + 1)
		mag_diff_lbl.text = "%d -> %d ROUNDS" % [cur_mag, next_mag]
		if cash < cost:
			mag_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			mag_btn.disabled = true
		else:
			mag_btn.text = "UPGRADE ($%d)" % cost
			mag_btn.disabled = false
			
	# 3. Reload Row
	reload_level_lbl.text = "LVL %d / %d" % [lvl_rel, MAX_LEVEL]
	reload_progress.value = float(lvl_rel)
	var base_rel = data.base_reload_time
	var cur_rel = max(0.6, base_rel * (1.0 - lvl_rel * 0.15))
	var next_rel = max(0.6, base_rel * (1.0 - (lvl_rel + 1) * 0.15))
	if lvl_rel >= MAX_LEVEL:
		reload_diff_lbl.text = "%.2fs (MAX)" % cur_rel
		reload_btn.text = "MAX LEVEL"
		reload_btn.disabled = true
	else:
		var cost = data.upgrade_cost_reload * (lvl_rel + 1)
		reload_diff_lbl.text = "%.2fs -> %.2fs (-15%%)" % [cur_rel, next_rel]
		if cash < cost:
			reload_btn.text = "NOT ENOUGH CASH ($%d)" % cost
			reload_btn.disabled = true
		else:
			reload_btn.text = "UPGRADE ($%d)" % cost
			reload_btn.disabled = false

func _on_unlock_pressed():
	var save_mgr = get_node_or_null("/root/SaveManager")
	if not save_mgr: return
	
	# Simulate AdMob Rewarded Video
	print("[AdMob] Show Rewarded Ad for Weapon Unlock")
	# Fake Ad Callback (in a real game, wait for AdMob callback)
	if save_mgr.data.cash >= 5000:
		save_mgr.add_cash(-5000)
		_unlock_current_weapon(save_mgr)
	else:
		# Just simulate the user watched an ad
		_unlock_current_weapon(save_mgr)

func _unlock_current_weapon(save_mgr):
	if not current_weapon_id in save_mgr.data.unlocked_weapons:
		save_mgr.data.unlocked_weapons.append(current_weapon_id)
		save_mgr.save_game()
		
		# Also add to player's weapon configs so it spawns!
		# In a real setup, Player.gd loads from SaveManager
		update_ui()

func _on_upgrade_pressed(type: String):
	var save_mgr = get_node_or_null("/root/SaveManager")
	if not save_mgr: return
	
	var data = load(weapon_resources[current_weapon_id])
	if not data: return
	
	var upgrades_dict = save_mgr.data.weapon_upgrades.get(current_weapon_id, {})
	var cur_lvl = upgrades_dict.get(type, 0)
	if cur_lvl >= MAX_LEVEL: return
	
	var base_cost = 0
	match type:
		"damage": base_cost = data.upgrade_cost_damage
		"mag": base_cost = data.upgrade_cost_mag
		"reload": base_cost = data.upgrade_cost_reload
		
	var cost = base_cost * (cur_lvl + 1)
	if save_mgr.data.cash >= cost:
		save_mgr.add_cash(-cost)
		upgrades_dict[type] = cur_lvl + 1
		save_mgr.data.weapon_upgrades[current_weapon_id] = upgrades_dict
		save_mgr.save_game()
		
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
