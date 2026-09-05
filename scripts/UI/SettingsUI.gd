extends Control

@onready var master_slider = $Panel/VBoxContainer/AudioSettings/MasterSlider
@onready var quality_option = $Panel/VBoxContainer/GraphicsSettings/QualityOption

func _ready():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.SETTINGS)
		
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr and master_slider:
		master_slider.value = audio_mgr.master_volume
		
	var q_mgr = get_node_or_null("/root/QualityManager")
	if q_mgr and quality_option:
		quality_option.selected = q_mgr.current_quality
		
	show()

func _on_master_slider_value_changed(value: float):
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.set_master_volume(value)
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and save_mgr.data.has("settings"):
		save_mgr.data.settings["master_volume"] = value
		save_mgr.save_game()

func _on_quality_option_item_selected(index: int):
	var q_mgr = get_node_or_null("/root/QualityManager")
	if q_mgr:
		q_mgr.apply_quality(index)
	var perf_mgr = get_node_or_null("/root/PerformanceManager")
	if perf_mgr:
		perf_mgr.set_profile(index)
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr:
		save_mgr.data["selected_quality"] = index
		save_mgr.save_game()

func _on_back_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		var target_state = game_state_mgr.previous_state
		if target_state == game_state_mgr.State.MAIN_MENU:
			game_state_mgr.change_state(game_state_mgr.State.MAIN_MENU)
			get_tree().change_scene_to_file("res://scenes/UI/MainMenu.tscn")
			return
		else:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
			get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
			return
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
