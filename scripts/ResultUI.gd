extends Control

@onready var title_label = $Center/Panel/VBox/Title
@onready var kills_label = $Center/Panel/VBox/Kills
@onready var headshots_label = $Center/Panel/VBox/Headshots
@onready var accuracy_label = $Center/Panel/VBox/Accuracy
@onready var cash_label = $Center/Panel/VBox/CashLabel
@onready var next_button = $Center/Panel/VBox/NextButton
@onready var replay_button = $Center/Panel/VBox/ReplayButton

var last_mission: MissionData = null

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		if not mission_mgr.mission_completed.is_connected(_on_mission_completed):
			mission_mgr.mission_completed.connect(_on_mission_completed)
		if not mission_mgr.mission_failed.is_connected(_on_mission_failed):
			mission_mgr.mission_failed.connect(_on_mission_failed)
	hide()

func _on_mission_completed(mission: MissionData):
	last_mission = mission
	var mission_mgr = get_node_or_null("/root/MissionManager")
	var stats = mission_mgr.last_stats if (mission_mgr and "last_stats" in mission_mgr) else {}
	var kills = stats.get("kills", mission.target_count if mission else 0)
	var headshots = stats.get("headshots", 0)
	var accuracy = stats.get("accuracy", 80)
	var bounty_awarded = stats.get("bounty_awarded", stats.get("cash", mission.reward_cash if mission else 100))
	var is_first_time = stats.get("first_time_reward", bounty_awarded > 0)
	
	title_label.text = "MISSION COMPLETE"
	title_label.modulate = Color(0.2, 0.95, 0.4)
	kills_label.text = "Zombies Eliminated: %d" % kills
	headshots_label.text = "Headshots: %d" % headshots
	accuracy_label.text = "Accuracy: %d%%" % accuracy
	
	if not is_first_time or bounty_awarded == 0:
		cash_label.text = "Reward: $0 CASH (PREVIOUSLY CLAIMED)"
	else:
		cash_label.text = "Reward: $0 CASH"
		var tween = create_tween()
		tween.tween_method(func(val: int): cash_label.text = "Reward: +$%d CASH" % val, 0, bounty_awarded, 0.65).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	next_button.visible = true
	replay_button.visible = true
	
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.play_victory()
		
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
	modulate.a = 0.0
	scale = Vector2(0.96, 0.96)
	pivot_offset = size / 2.0
	show()
	var in_tween = create_tween().set_parallel(true)
	in_tween.tween_property(self, "modulate:a", 1.0, 0.22)
	in_tween.tween_property(self, "scale", Vector2.ONE, 0.22).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _on_mission_failed(mission: MissionData):
	last_mission = mission
	var mission_mgr = get_node_or_null("/root/MissionManager")
	var stats = mission_mgr.last_stats if (mission_mgr and "last_stats" in mission_mgr) else {}
	var kills = stats.get("kills", 0)
	var headshots = stats.get("headshots", 0)
	var accuracy = stats.get("accuracy", 0)
	
	title_label.text = "MISSION FAILED"
	title_label.modulate = Color(1.0, 0.25, 0.2)
	kills_label.text = "Zombies Eliminated: %d" % kills
	headshots_label.text = "Headshots: %d" % headshots
	accuracy_label.text = "Accuracy: %d%%" % accuracy
	cash_label.text = "Reward: $0 CASH (MISSION FAILED)"
	
	next_button.visible = false
	replay_button.visible = true
	
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.play_defeat()
		
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
	modulate.a = 0.0
	scale = Vector2(0.96, 0.96)
	pivot_offset = size / 2.0
	show()
	var in_tween = create_tween().set_parallel(true)
	in_tween.tween_property(self, "modulate:a", 1.0, 0.22)
	in_tween.tween_property(self, "scale", Vector2.ONE, 0.22).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _on_next_pressed():
	hide()
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")

func _on_replay_pressed():
	hide()
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr and last_mission:
		mission_mgr.start_mission(last_mission)
	else:
		get_tree().reload_current_scene()
