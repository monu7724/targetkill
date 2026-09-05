extends Control

@onready var mission_list = $ScrollContainer/VBoxContainer
@export var mission_card_prefab: PackedScene

@onready var briefing_modal = $BriefingModal
@onready var briefing_header = $BriefingModal/ModalPanel/Margin/VBox/BriefingHeader
@onready var briefing_location = $BriefingModal/ModalPanel/Margin/VBox/BriefingLocation
@onready var briefing_difficulty = $BriefingModal/ModalPanel/Margin/VBox/BriefingDifficulty
@onready var briefing_objective = $BriefingModal/ModalPanel/Margin/VBox/BriefingObjective
@onready var briefing_lore = $BriefingModal/ModalPanel/Margin/VBox/BriefingLore
@onready var briefing_loadout = $BriefingModal/ModalPanel/Margin/VBox/BriefingLoadout
@onready var briefing_reward = $BriefingModal/ModalPanel/Margin/VBox/BriefingReward
@onready var coins_label = $TopBar/CoinsLabel

var selected_mission: MissionData = null

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
		
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and coins_label:
		coins_label.text = "COINS: %d" % save_mgr.data.coins
		
	if briefing_modal:
		briefing_modal.visible = false
		
	populate_missions()
	print("[%d ms] [MISSION_SELECT] MissionSelect ready." % Time.get_ticks_msec())

func populate_missions():
	for child in mission_list.get_children():
		child.queue_free()
		
	for mission_path in missions:
		var data = load(mission_path)
		if data and mission_card_prefab:
			var card = mission_card_prefab.instantiate()
			mission_list.add_child(card)
			card.setup(data)
			if card.has_signal("mission_selected"):
				card.mission_selected.connect(_on_mission_selected)

func _on_mission_selected(data: MissionData):
	selected_mission = data
	if not briefing_modal or not data:
		var mission_mgr = get_node_or_null("/root/MissionManager")
		if mission_mgr:
			mission_mgr.start_mission(data)
		return
		
	briefing_header.text = "OPERATION: " + data.display_name.to_upper()
	briefing_location.text = "📍 LOCATION: " + (data.location_name if "location_name" in data and data.location_name != "" else "Sector Zone")
	
	var stars_count = data.difficulty_stars if "difficulty_stars" in data else 1
	var stars_str = ""
	for i in range(5):
		stars_str += "★" if i < stars_count else "☆"
	briefing_difficulty.text = "THREAT LEVEL: " + stars_str
	
	var obj_text = "Eliminate hostile contacts."
	match data.objective_type:
		MissionData.ObjectiveType.KILL_COUNT:
			obj_text = "Eliminate %d infected hosts." % data.target_count
		MissionData.ObjectiveType.SURVIVE_WAVES:
			obj_text = "Survive %d hostile waves." % data.wave_count
		MissionData.ObjectiveType.BOSS_KILL:
			obj_text = "Neutralize the Sector Apex Alpha specimen."
	briefing_objective.text = "PRIMARY OBJECTIVE: " + obj_text
	
	briefing_lore.text = data.description
	briefing_loadout.text = "RECOMMENDED LOADOUT: " + (data.recommended_loadout if "recommended_loadout" in data and data.recommended_loadout != "" else "Standard Issue Rifle")
	briefing_reward.text = "MISSION BOUNTY: %d COINS" % data.reward_coins
	
	briefing_modal.modulate.a = 0.0
	briefing_modal.visible = true
	var tw = create_tween()
	tw.tween_property(briefing_modal, "modulate:a", 1.0, 0.18)

func _on_deploy_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	if selected_mission:
		var mission_mgr = get_node_or_null("/root/MissionManager")
		if mission_mgr:
			mission_mgr.start_mission(selected_mission)

func _on_close_briefing_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	if briefing_modal:
		var tw = create_tween()
		tw.tween_property(briefing_modal, "modulate:a", 0.0, 0.15)
		tw.tween_callback(func(): briefing_modal.visible = false)

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
