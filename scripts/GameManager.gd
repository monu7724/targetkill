extends Node3D

@export var zombie_scene: PackedScene
@export var spawn_points: Array[Node3D]
@export var wave_delay: float = 5.0

var mission: MissionData
var current_wave: int = 0
var zombies_to_spawn: int = 0
var zombies_alive: int = 0

func _ready():
	mission = MissionManager.current_mission
	if not mission:
		# Default for testing
		mission = load("res://resources/missions/mission_01.tres")
	
	start_next_wave()

func start_next_wave():
	current_wave += 1
	
	if mission and mission.objective_type == MissionData.ObjectiveType.BOSS_KILL:
		zombies_to_spawn = max(1, mission.target_count)
		print("Boss Encounter: ", current_wave)
		spawn_wave()
		return
	
	# Scale wave difficulty for a stronger survival loop
	zombies_to_spawn = 5 + (current_wave * 2)
	if current_wave >= 3:
		zombies_to_spawn += 2
	if current_wave >= 5:
		zombies_to_spawn += 3
	if mission and mission.objective_type == MissionData.ObjectiveType.KILL_COUNT:
		var remaining = mission.target_count - MissionManager.kill_count
		zombies_to_spawn = min(zombies_to_spawn, remaining)
		
	if zombies_to_spawn <= 0 and mission and mission.objective_type == MissionData.ObjectiveType.KILL_COUNT:
		return

	print("Starting Wave: ", current_wave)
	spawn_wave()

var is_spawning_wave: bool = false

func spawn_wave():
	is_spawning_wave = true
	var count = zombies_to_spawn
	for i in range(count):
		spawn_zombie()
		if i < count - 1:
			await get_tree().create_timer(1.5).timeout
	is_spawning_wave = false
	if zombies_alive <= 0:
		_check_wave_end()

func spawn_zombie():
	if spawn_points.is_empty() or not zombie_scene:
		return
		
	var spawn_point = spawn_points.pick_random()
	var zombie = zombie_scene.instantiate()
	
	# Select archetype based on mission config
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
	zombies_alive -= 1
	if not is_spawning_wave and zombies_alive <= 0:
		_check_wave_end()

func _check_wave_end():
	MissionManager.on_wave_completed()
	if not mission:
		return
	if mission.objective_type == MissionData.ObjectiveType.SURVIVE_WAVES:
		if current_wave < mission.wave_count:
			await get_tree().create_timer(wave_delay).timeout
			start_next_wave()
	else:
		if MissionManager.kill_count < mission.target_count:
			await get_tree().create_timer(wave_delay).timeout
			start_next_wave()
