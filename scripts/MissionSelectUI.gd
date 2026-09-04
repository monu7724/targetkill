extends Control

@onready var mission_list = $ScrollContainer/VBoxContainer
@export var mission_card_prefab: PackedScene

var missions = [
	"res://resources/missions/mission_01.tres",
	"res://resources/missions/mission_02.tres",
	"res://resources/missions/mission_03.tres",
	"res://resources/missions/mission_04.tres",
	"res://resources/missions/mission_05.tres"
]

func _ready():
	populate_missions()

func populate_missions():
	for mission_path in missions:
		var data = load(mission_path)
		var card = mission_card_prefab.instantiate()
		mission_list.add_child(card)
		card.setup(data)

func _on_upgrade_button_pressed():
	get_tree().change_scene_to_file("res://scenes/UI/UpgradeUI.tscn")

func _on_settings_button_pressed():
	get_tree().change_scene_to_file("res://scenes/UI/SettingsUI.tscn")
