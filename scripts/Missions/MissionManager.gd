extends Node

signal mission_started(mission: MissionData)
signal mission_completed(mission: MissionData)
signal mission_failed(mission: MissionData)

var current_mission: MissionData = null
var kill_count: int = 0
var wave_count: int = 0
var boss_kill_count: int = 0

func start_mission(mission: MissionData):
	current_mission = mission
	kill_count = 0
	wave_count = 0
	boss_kill_count = 0
	mission_started.emit(mission)
	
	var target_scene = "res://scenes/environments/AirportTerminal.tscn"
	if mission and mission.scene_path != "":
		target_scene = mission.scene_path
		
	var loading_mgr = get_node_or_null("/root/LoadingManager")
	if loading_mgr and loading_mgr.has_method("load_scene_async"):
		loading_mgr.load_scene_async(target_scene, mission)
	else:
		get_tree().change_scene_to_file(target_scene)

func on_zombie_killed():
	kill_count += 1
	_notify_objective()
	check_objective()

func on_boss_killed():
	boss_kill_count += 1
	_notify_objective()
	check_objective()

func on_wave_completed():
	wave_count += 1
	_notify_objective()
	check_objective()

func _notify_objective():
	if not current_mission: return
	var current_prog = 0
	var target_prog = 1
	match current_mission.objective_type:
		MissionData.ObjectiveType.KILL_COUNT:
			current_prog = kill_count
			target_prog = current_mission.target_count
		MissionData.ObjectiveType.SURVIVE_WAVES:
			current_prog = wave_count
			target_prog = current_mission.wave_count
		MissionData.ObjectiveType.BOSS_KILL:
			current_prog = boss_kill_count
			target_prog = current_mission.target_count
			
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.objective_updated.emit(current_mission.display_name, current_mission.description, current_prog, target_prog)

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
		MissionData.ObjectiveType.BOSS_KILL:
			if boss_kill_count >= current_mission.target_count:
				completed = true
	
	if completed:
		finish_mission(true)

func finish_mission(success: bool):
	if not current_mission:
		return
		
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if success:
		if game_state_mgr:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_COMPLETE)
			
		var save_mgr = get_node_or_null("/root/SaveManager")
		if save_mgr:
			save_mgr.add_coins(current_mission.reward_coins)
			save_mgr.complete_mission(current_mission.mission_id)
			
		mission_completed.emit(current_mission)
	else:
		if game_state_mgr:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_FAILED)
		mission_failed.emit(current_mission)
		
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.mission_finished.emit(current_mission.mission_id, success)
		
	current_mission = null
