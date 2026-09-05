extends Control

@onready var title_label = $Panel/VBoxContainer/Title
@onready var coins_label = $Panel/VBoxContainer/CoinsLabel
@onready var next_button = $Panel/VBoxContainer/NextButton

var last_mission: MissionData = null

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		mission_mgr.mission_completed.connect(_on_mission_completed)
		mission_mgr.mission_failed.connect(_on_mission_failed)
	hide()

func _on_mission_completed(mission: MissionData):
	last_mission = mission
	title_label.text = "VICTORY"
	title_label.modulate = Color(0.2, 1.0, 0.4)
	var reward = mission.reward_coins if mission else 100
	
	# Smooth animated reward count-up (Section 22)
	coins_label.text = "Reward: 0 Coins"
	var tween = create_tween()
	tween.tween_method(func(val: int): coins_label.text = "Reward: %d Coins" % val, 0, reward, 0.65).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	next_button.text = "NEXT MISSION"
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.play_victory()
		
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	
	# Modal scale/fade in
	modulate.a = 0.0
	scale = Vector2(0.96, 0.96)
	pivot_offset = size / 2.0
	show()
	var in_tween = create_tween().set_parallel(true)
	in_tween.tween_property(self, "modulate:a", 1.0, 0.22)
	in_tween.tween_property(self, "scale", Vector2.ONE, 0.22).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)

func _on_mission_failed(mission: MissionData):
	last_mission = mission
	title_label.text = "MISSION FAILED"
	title_label.modulate = Color(1.0, 0.25, 0.2)
	coins_label.text = "Try again!"
	next_button.text = "RETRY"
	
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

func _on_next_button_pressed():
	hide()
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if title_label.text == "VICTORY":
		if game_state_mgr:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
		get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
	else:
		var mission_mgr = get_node_or_null("/root/MissionManager")
		if mission_mgr and last_mission:
			mission_mgr.start_mission(last_mission)
		else:
			get_tree().reload_current_scene()

func _on_menu_button_pressed():
	hide()
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
