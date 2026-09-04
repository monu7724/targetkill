extends Control

@onready var coins_label = $Header/CoinsLabel
@onready var weapon_title = $Panel/VBoxContainer/WeaponTitle
@onready var damage_btn = $Panel/VBoxContainer/DamageBtn
@onready var mag_btn = $Panel/VBoxContainer/MagBtn
@onready var reload_btn = $Panel/VBoxContainer/ReloadBtn

var current_weapon_id = "pistol"
var weapon_resources = {
	"pistol": "res://resources/weapons/pistol.tres",
	"rifle": "res://resources/weapons/rifle.tres",
	"shotgun": "res://resources/weapons/shotgun.tres"
}

func _ready():
	update_ui()

func update_ui():
	var data = load(weapon_resources[current_weapon_id])
	var levels = SaveManager.data.weapon_upgrades.get(current_weapon_id, {"damage": 0, "mag": 0, "reload": 0})
	
	coins_label.text = "Coins: " + str(SaveManager.data.coins)
	weapon_title.text = data.display_name
	
	damage_btn.text = "Upgrade Damage (Cost: " + str(data.upgrade_cost_damage) + ") - Lvl " + str(levels.damage)
	mag_btn.text = "Upgrade Mag (Cost: " + str(data.upgrade_cost_mag) + ") - Lvl " + str(levels.mag)
	reload_btn.text = "Upgrade Reload (Cost: " + str(data.upgrade_cost_reload) + ") - Lvl " + str(levels.reload)

func _on_upgrade_pressed(type: String):
	var data = load(weapon_resources[current_weapon_id])
	var levels = SaveManager.data.weapon_upgrades[current_weapon_id]
	var cost = 0
	match type:
		"damage": cost = data.upgrade_cost_damage
		"mag": cost = data.upgrade_cost_mag
		"reload": cost = data.upgrade_cost_reload
	
	if SaveManager.data.coins >= cost:
		SaveManager.add_coins(-cost)
		levels[type] += 1
		SaveManager.save_game()
		update_ui()

func _on_back_pressed():
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
