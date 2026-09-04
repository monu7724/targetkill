extends Control

@onready var title_label = $Panel/VBoxContainer/Title
@onready var coins_label = $Panel/VBoxContainer/CoinsLabel
@onready var next_button = $Panel/VBoxContainer/NextButton

var last_mission: MissionData

func _ready():
	MissionManager.mission_completed.connect(_on_mission_completed)
	MissionManager.mission_failed.connect(_on_mission_failed)
	hide()

func _on_mission_completed(mission: MissionData):
	last_mission = mission
	title_label.text = "VICTORY"
	title_label.modulate = Color.GREEN
	coins_label.text = "Reward: " + str(mission.reward_coins) + " Coins"
	next_button.text = "NEXT MISSION"
	show()

func _on_mission_failed(mission: MissionData):
	last_mission = mission
	title_label.text = "MISSION FAILED"
	title_label.modulate = Color.RED
	coins_label.text = "Try again!"
	next_button.text = "RETRY"
	show()

func _on_next_button_pressed():
	if title_label.text == "VICTORY":
		# In a real game, you'd find the next mission resource
		get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
	else:
		MissionManager.start_mission(last_mission)
	hide()

func _on_menu_button_pressed():
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
	hide()
