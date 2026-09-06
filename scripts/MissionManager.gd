extends Node

signal mission_started(mission: MissionData)
signal mission_completed(mission: MissionData)
signal mission_failed(mission: MissionData)

var current_mission: MissionData = null
var kill_count: int = 0
var wave_count: int = 0
var boss_kill_count: int = 0
var shots_fired: int = 0
var shots_hit: int = 0
var headshots: int = 0

var last_stats: Dictionary = {
	"kills": 0,
	"headshots": 0,
	"accuracy": 0,
	"cash": 0,
	"success": false
}

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		if not event_bus.weapon_fired.is_connected(_on_weapon_fired):
			event_bus.weapon_fired.connect(_on_weapon_fired)
		if not event_bus.damage_dealt.is_connected(_on_damage_dealt):
			event_bus.damage_dealt.connect(_on_damage_dealt)
		if not event_bus.enemy_killed.is_connected(_on_enemy_killed_event):
			event_bus.enemy_killed.connect(_on_enemy_killed_event)
	print("[%d ms] [BOOT:02] MissionManager ready." % Time.get_ticks_msec())

func _on_weapon_fired(_weapon_id: String, _cur: int, _max: int):
	shots_fired += 1

func _on_damage_dealt(_amount: float, is_headshot: bool, _hit_zone: String, _target: Node):
	shots_hit += 1
	if is_headshot:
		headshots += 1

func _on_enemy_killed_event(_archetype: String, is_headshot: bool, _pos: Vector3):
	if is_headshot and headshots == 0:
		headshots += 1

func start_mission(mission: MissionData):
	current_mission = mission
	kill_count = 0
	wave_count = 0
	boss_kill_count = 0
	shots_fired = 0
	shots_hit = 0
	headshots = 0
	
	print("[%d ms] [MISSION:START] Starting mission: %s" % [Time.get_ticks_msec(), mission.display_name if mission else "None"])
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
	
	var accuracy = 0
	if shots_fired > 0:
		accuracy = int(clamp((float(shots_hit) / float(shots_fired)) * 100.0, 0.0, 100.0))
	elif kill_count > 0:
		accuracy = 100
		
	var save_mgr = get_node_or_null("/root/SaveManager")
	var is_first_win = false
	if success:
		if save_mgr:
			is_first_win = not save_mgr.is_mission_completed(current_mission.mission_id)
		else:
			is_first_win = true
			
	var earned_cash = current_mission.reward_cash if (success and is_first_win) else 0
		
	last_stats = {
		"kills": kill_count + boss_kill_count,
		"headshots": headshots,
		"accuracy": accuracy,
		"cash": earned_cash,
		"bounty_awarded": earned_cash,
		"first_time_reward": is_first_win if success else false,
		"success": success
	}
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if success:
		if game_state_mgr:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_COMPLETE)
			
		if save_mgr and not save_mgr.is_mission_completed(current_mission.mission_id):
			save_mgr.add_cash(current_mission.reward_cash)
			last_stats["bounty_awarded"] = current_mission.reward_cash
		else:
			last_stats["bounty_awarded"] = 0
		if save_mgr:
			save_mgr.complete_mission(current_mission.mission_id)
			
		print("[%d ms] [MISSION:COMPLETE] Mission succeeded: %s (Kills: %d, Accuracy: %d%%, Cash Awarded: %d)" % [Time.get_ticks_msec(), current_mission.display_name, last_stats.kills, accuracy, last_stats.bounty_awarded])
		mission_completed.emit(current_mission)
	else:
		if game_state_mgr:
			game_state_mgr.change_state(game_state_mgr.State.MISSION_FAILED)
		print("[%d ms] [MISSION:FAILED] Mission failed: %s" % [Time.get_ticks_msec(), current_mission.display_name])
		mission_failed.emit(current_mission)
		
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.mission_finished.emit(current_mission.mission_id, success)
		
	current_mission = null
