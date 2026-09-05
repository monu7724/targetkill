extends PanelContainer

@onready var title_label = $MarginContainer/VBoxContainer/Title
@onready var desc_label = $MarginContainer/VBoxContainer/Description
@onready var reward_label = $MarginContainer/VBoxContainer/Reward
@onready var play_button = $MarginContainer/VBoxContainer/PlayButton

var mission_data: MissionData

func setup(data: MissionData):
	mission_data = data
	title_label.text = data.display_name
	desc_label.text = data.description
	reward_label.text = "Reward: " + str(data.reward_coins) + " Coins"
	
	var is_unlocked = true
	if data.unlock_requirement_id != "":
		is_unlocked = SaveManager.is_mission_completed(data.unlock_requirement_id)
	
	play_button.disabled = not is_unlocked
	if not is_unlocked:
		modulate = Color(0.5, 0.5, 0.5, 0.8)
		play_button.text = "LOCKED"
	else:
		var is_completed = SaveManager.is_mission_completed(data.mission_id)
		if is_completed:
			modulate = Color(1.0, 1.0, 1.0, 1.0)
			play_button.text = "COMPLETED"
		else:
			modulate = Color(1.0, 1.0, 1.0, 1.0)
			play_button.text = "DEPLOY"

func _on_play_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	MissionManager.start_mission(mission_data)
