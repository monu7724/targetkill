extends Node

signal mission_started(mission: MissionData)
signal mission_completed(mission: MissionData)
signal mission_failed(mission: MissionData)

var current_mission: MissionData = null
var kill_count: int = 0
var wave_count: int = 0

func start_mission(mission: MissionData):
	current_mission = mission
	kill_count = 0
	wave_count = 0
	mission_started.emit(mission)
	get_tree().change_scene_to_file("res://scenes/environments/UrbanStreet.tscn")

func on_zombie_killed():
	kill_count += 1
	check_objective()

func on_wave_completed():
	wave_count += 1
	check_objective()

func check_objective():
	if not current_mission: return
	
	var completed = false
	match current_mission.objective_type:
		MissionData.ObjectiveType.KILL_COUNT:
			if kill_count >= current_mission.target_count:
				completed = true
		MissionData.ObjectiveType.SURVIVE_WAVES:
			if wave_count >= current_mission.wave_count:
				completed = true
	
	if completed:
		finish_mission(true)

func finish_mission(success: bool):
	if success:
		SaveManager.add_coins(current_mission.reward_coins)
		SaveManager.complete_mission(current_mission.mission_id)
		mission_completed.emit(current_mission)
	else:
		mission_failed.emit(current_mission)
	current_mission = null
