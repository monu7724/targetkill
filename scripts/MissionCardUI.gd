extends PanelContainer

signal mission_selected(data: MissionData)

@onready var title_label = $MarginContainer/VBoxContainer/Title
@onready var location_label = $MarginContainer/VBoxContainer/Location
@onready var stars_label = $MarginContainer/VBoxContainer/Stars
@onready var desc_label = $MarginContainer/VBoxContainer/Description
@onready var reward_label = $MarginContainer/VBoxContainer/Reward
@onready var play_button = $MarginContainer/VBoxContainer/PlayButton

var mission_data: MissionData

func setup(data: MissionData):
	mission_data = data
	title_label.text = data.display_name
	if location_label:
		location_label.text = "📍 " + (data.location_name if "location_name" in data and data.location_name != "" else "Sector Zone")
	if stars_label:
		var stars_count = data.difficulty_stars if "difficulty_stars" in data else 1
		var stars_str = ""
		for i in range(5):
			stars_str += "★" if i < stars_count else "☆"
		stars_label.text = "Difficulty: " + stars_str
		
	desc_label.text = data.description
	reward_label.text = "Reward: " + str(data.reward_coins) + " Coins"
	
	var is_unlocked = true
	if data.unlock_requirement_id != "":
		var save_mgr = get_node_or_null("/root/SaveManager")
		if save_mgr:
			is_unlocked = save_mgr.is_mission_completed(data.unlock_requirement_id)
	
	play_button.disabled = not is_unlocked
	if not is_unlocked:
		modulate = Color(0.5, 0.5, 0.5, 0.8)
		play_button.text = "LOCKED"
	else:
		modulate = Color(1.0, 1.0, 1.0, 1.0)
		var save_mgr = get_node_or_null("/root/SaveManager")
		var is_completed = save_mgr.is_mission_completed(data.mission_id) if save_mgr else false
		if is_completed:
			play_button.text = "BRIEFING (COMPLETED)"
		else:
			play_button.text = "MISSION BRIEFING"

func _on_play_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	mission_selected.emit(mission_data)

