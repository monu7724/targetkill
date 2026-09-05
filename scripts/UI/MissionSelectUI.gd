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
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
	populate_missions()

func populate_missions():
	for child in mission_list.get_children():
		child.queue_free()
		
	for mission_path in missions:
		var data = load(mission_path)
		if data and mission_card_prefab:
			var card = mission_card_prefab.instantiate()
			mission_list.add_child(card)
			card.setup(data)

func _on_upgrade_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.UPGRADES)
	get_tree().change_scene_to_file("res://scenes/UI/UpgradeUI.tscn")

func _on_settings_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.SETTINGS)
	get_tree().change_scene_to_file("res://scenes/UI/SettingsUI.tscn")

func _on_back_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MAIN_MENU)
	get_tree().change_scene_to_file("res://scenes/UI/MainMenu.tscn")
