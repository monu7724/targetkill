extends PanelContainer

signal mission_selected(data: MissionData)

@onready var title_label = $HBox/VBox/Title
@onready var obj_label = $HBox/VBox/Objective
@onready var reward_label = $HBox/VBox/Reward
@onready var status_label = $HBox/VBox/Status
@onready var threat_label = get_node_or_null("HBox/VBox/Threat")
@onready var play_button = $HBox/Margin/PlayButton

var mission_data: MissionData

func setup(data: MissionData):
	mission_data = data
	title_label.text = data.display_name
	
	var obj_text = "Eliminate hostile contacts."
	match data.objective_type:
		MissionData.ObjectiveType.KILL_COUNT:
			obj_text = "Eliminate %d infected hosts." % data.target_count
		MissionData.ObjectiveType.SURVIVE_WAVES:
			obj_text = "Survive %d hostile waves." % data.wave_count
		MissionData.ObjectiveType.BOSS_KILL:
			obj_text = "Neutralize the Sector Apex Alpha specimen."
	obj_label.text = "Objective: " + obj_text
	
	var stars_count = data.difficulty_stars if "difficulty_stars" in data else 1
	var stars_str = ""
	for i in range(5):
		stars_str += "★" if i < stars_count else "☆"
	if threat_label:
		threat_label.text = "THREAT: " + stars_str
	
	var is_unlocked = true
	if data.unlock_requirement_id != "":
		var save_mgr = get_node_or_null("/root/SaveManager")
		if save_mgr:
			is_unlocked = save_mgr.is_mission_completed(data.unlock_requirement_id)
	
	play_button.disabled = false
	if not is_unlocked:
		modulate = Color(0.65, 0.65, 0.65, 0.9)
		status_label.text = "STATUS: LOCKED"
		status_label.add_theme_color_override("font_color", Color(1.0, 0.3, 0.3))
		reward_label.text = "BOUNTY: $" + str(data.reward_cash) + " (SINGLE CLAIM)"
		play_button.text = "WATCH AD"
	else:
		modulate = Color(1.0, 1.0, 1.0, 1.0)
		var save_mgr = get_node_or_null("/root/SaveManager")
		var is_completed = save_mgr.is_mission_completed(data.mission_id) if save_mgr else false
		if is_completed:
			status_label.text = "STATUS: COMPLETED"
			status_label.add_theme_color_override("font_color", Color(0.3, 1.0, 0.3))
			reward_label.text = "BOUNTY: $" + str(data.reward_cash) + " (CLAIMED)"
			play_button.text = "REPLAY"
		else:
			status_label.text = "STATUS: ACTIVE"
			status_label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.3))
			reward_label.text = "BOUNTY: $" + str(data.reward_cash) + " (FIRST CLEAR)"
			play_button.text = "DEPLOY"

func _on_play_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	if play_button.text == "WATCH AD":
		print("[AdMob] Show Rewarded Ad to unlock mission")
		var save_mgr = get_node_or_null("/root/SaveManager")
		if save_mgr and mission_data.unlock_requirement_id != "":
			save_mgr.complete_mission(mission_data.unlock_requirement_id)
			setup(mission_data)
		return
		
	mission_selected.emit(mission_data)
