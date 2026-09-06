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
	var total_waves = mission.wave_count if mission else 3
	
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.wave_started.emit(current_wave, total_waves)
	
	# Check if structured waves are defined in mission
	if mission and not mission.waves.is_empty() and current_wave <= mission.waves.size():
		var wave_data = mission.waves[current_wave - 1]
		var groups = wave_data.get("groups", [])
		zombies_to_spawn = 0
		for g in groups:
			zombies_to_spawn += g.get("count", 1)
		spawn_structured_wave(groups)
		return
	
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

func spawn_structured_wave(groups: Array):
	is_spawning_wave = true
	for group in groups:
		if not is_inside_tree():
			return
		var arch = group.get("enemy_type", "normal")
		var count = group.get("count", 1)
		var dir = group.get("spawn_direction", "")
		var delay = group.get("delay", 1.2)
		for i in range(count):
			while zombies_alive >= max_active_zombies:
				await get_tree().create_timer(0.8).timeout
				if not is_inside_tree():
					return
			spawn_zombie(arch, dir)
			if delay > 0 and (i < count - 1 or group != groups.back()):
				await get_tree().create_timer(delay).timeout
				if not is_inside_tree():
					return
	is_spawning_wave = false
	if zombies_alive <= 0:
		_check_wave_end()

func spawn_wave():
	is_spawning_wave = true
	var count = zombies_to_spawn
	for i in range(count):
		# Throttle spawning if too many zombies are active
		while zombies_alive >= max_active_zombies:
			await get_tree().create_timer(0.8).timeout
			if not is_inside_tree():
				return
			
		spawn_zombie()
		if i < count - 1:
			await get_tree().create_timer(1.4).timeout
			if not is_inside_tree():
				return
			
	is_spawning_wave = false
	if zombies_alive <= 0:
		_check_wave_end()

func spawn_zombie(specific_archetype: String = "", direction: String = ""):
	if spawn_points.is_empty() or not zombie_scene:
		return
		
	if not player_ref:
		player_ref = get_tree().get_first_node_in_group("player")
	var player_pos = player_ref.global_position if player_ref else Vector3.ZERO
	
	# Select spawn point matching direction if provided
	var candidate_points: Array[Node3D] = []
	if direction != "":
		for sp in spawn_points:
			if sp and sp.name.to_lower().contains(direction.to_lower()):
				candidate_points.append(sp)
				
	if candidate_points.is_empty():
		# Filter spawn points that maintain tactical distance (>10m)
		for sp in spawn_points:
			if sp and sp.global_position.distance_to(player_pos) > 10.0:
				candidate_points.append(sp)
			
	var spawn_point = candidate_points.pick_random() if not candidate_points.is_empty() else spawn_points.pick_random()
	if not spawn_point:
		return
		
	var arch = specific_archetype if specific_archetype != "" else _pick_archetype()
	var zombie = null
	if arch == "dog" and ResourceLoader.exists("res://scenes/zombies/InfectedDog.tscn"):
		var dog_scene = load("res://scenes/zombies/InfectedDog.tscn")
		if dog_scene:
			zombie = dog_scene.instantiate()
			
	if not zombie:
		zombie = zombie_scene.instantiate()
		zombie.archetype = arch
		
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
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.wave_completed.emit(current_wave)
		
	if not mission:
		return
		
	var total_waves = mission.wave_count if mission else 3
	if current_wave < total_waves:
		if mission.objective_type == MissionData.ObjectiveType.SURVIVE_WAVES:
			await get_tree().create_timer(wave_delay).timeout
			if is_inside_tree():
				start_next_wave()
		else:
			if mission_mgr and mission_mgr.kill_count < mission.target_count:
				await get_tree().create_timer(wave_delay).timeout
				if is_inside_tree():
					start_next_wave()
