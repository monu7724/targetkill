extends Node3D

@export var zombie_scene: PackedScene
@export var spawn_points: Array[Node3D]
@export var wave_delay: float = 4.5
@export var max_active_zombies: int = 10

var mission: MissionData
var current_wave: int = 0
var zombies_to_spawn: int = 0
var zombies_alive: int = 0
var is_spawning_wave: bool = false
var player_ref: Node3D = null

func _ready():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.GAMEPLAY)
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr and mission_mgr.current_mission:
		mission = mission_mgr.current_mission
	else:
		mission = load("res://resources/missions/mission_01.tres")
		
	player_ref = get_tree().get_first_node_in_group("player")
	start_next_wave()

func start_next_wave():
	current_wave += 1
	
	if mission and mission.objective_type == MissionData.ObjectiveType.BOSS_KILL:
		zombies_to_spawn = max(1, mission.target_count)
		spawn_wave()
		return
	
	# Progressive tension scaling
	zombies_to_spawn = 4 + (current_wave * 2)
	if current_wave >= 3:
		zombies_to_spawn += 2
	if current_wave >= 5:
		zombies_to_spawn += 3
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission and mission.objective_type == MissionData.ObjectiveType.KILL_COUNT and mission_mgr:
		var remaining = mission.target_count - mission_mgr.kill_count
		zombies_to_spawn = min(zombies_to_spawn, remaining)
		
	if zombies_to_spawn <= 0 and mission and mission.objective_type == MissionData.ObjectiveType.KILL_COUNT:
		return

	spawn_wave()

func spawn_wave():
	is_spawning_wave = true
	var count = zombies_to_spawn
	for i in range(count):
		# Throttle spawning if too many zombies are active
		while zombies_alive >= max_active_zombies:
			await get_tree().create_timer(0.8).timeout
			
		spawn_zombie()
		if i < count - 1:
			await get_tree().create_timer(1.4).timeout
			
	is_spawning_wave = false
	if zombies_alive <= 0:
		_check_wave_end()

func spawn_zombie():
	if spawn_points.is_empty() or not zombie_scene:
		return
		
	if not player_ref:
		player_ref = get_tree().get_first_node_in_group("player")
	var player_pos = player_ref.global_position if player_ref else Vector3.ZERO
	
	# Filter spawn points that maintain tactical distance (>10m)
	var distant_points = []
	for sp in spawn_points:
		if sp.global_position.distance_to(player_pos) > 10.0:
			distant_points.append(sp)
			
	var spawn_point = distant_points.pick_random() if not distant_points.is_empty() else spawn_points.pick_random()
	var zombie = zombie_scene.instantiate()
	
	zombie.archetype = _pick_archetype()
	add_child(zombie)
	zombie.global_position = spawn_point.global_position
	
	zombies_alive += 1
	zombie.tree_exited.connect(_on_zombie_death)

func _pick_archetype() -> String:
	var rand = randf()
	var cumulative_weight = 0.0
	if mission and not mission.spawn_config.is_empty():
		for entry in mission.spawn_config:
			cumulative_weight += entry.weight
			if rand <= cumulative_weight:
				return entry.type
	
	if current_wave >= 5 and randf() < 0.2:
		return "boss"
	if current_wave >= 3 and randf() < 0.35:
		return "heavy"
	if current_wave >= 2 and randf() < 0.3:
		return "fast"
	return "normal"

func _on_zombie_death():
	zombies_alive = max(0, zombies_alive - 1)
	if not is_spawning_wave and zombies_alive <= 0:
		_check_wave_end()

func _check_wave_end():
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		mission_mgr.on_wave_completed()
	if not mission:
		return
	if mission.objective_type == MissionData.ObjectiveType.SURVIVE_WAVES:
		if current_wave < mission.wave_count:
			await get_tree().create_timer(wave_delay).timeout
			start_next_wave()
	else:
		if mission_mgr and mission_mgr.kill_count < mission.target_count:
			await get_tree().create_timer(wave_delay).timeout
			start_next_wave()
