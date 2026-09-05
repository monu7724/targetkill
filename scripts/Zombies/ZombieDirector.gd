class_name ZombieDirector
extends Node

signal wave_started(wave_idx: int, total_enemies: int)
signal wave_cleared(wave_idx: int)
signal all_waves_completed()

@export var max_active_zombies: int = 10
@export var spawn_interval: float = 1.4
@export var inter_wave_delay: float = 4.5

var zombie_scene: PackedScene = preload("res://scenes/zombies/Zombie.tscn")
var spawn_points: Array[Node3D] = []
var active_zombies: Array[Node3D] = []
var spawn_queue: Array[String] = []

var current_wave: int = 0
var total_waves: int = 3
var is_spawning: bool = false
var mission_ref: MissionData = null
var player_ref: Node3D = null

func initialize(points: Array[Node3D], mission: MissionData, player: Node3D):
	spawn_points = points
	mission_ref = mission
	player_ref = player
	if mission:
		total_waves = max(1, mission.wave_count)
	start_next_wave()

func start_next_wave():
	current_wave += 1
	spawn_queue.clear()
	_compose_wave()
	
	wave_started.emit(current_wave, spawn_queue.size())
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.wave_started.emit(current_wave, total_waves)
		
	_process_spawn_queue()

func _compose_wave():
	if mission_ref and mission_ref.objective_type == MissionData.ObjectiveType.BOSS_KILL:
		spawn_queue.append("boss")
		for i in range(3):
			spawn_queue.append("fast")
		return
		
	# Tension curve:
	# Wave 1: Intro pack (normals)
	# Wave 2: Pressure (normals + fast)
	# Wave 3+: Heavy assault (normals + heavy + fast)
	var base_count = 4 + (current_wave * 2)
	
	if mission_ref and mission_ref.objective_type == MissionData.ObjectiveType.KILL_COUNT:
		var mission_mgr = get_node_or_null("/root/MissionManager")
		var remaining = mission_ref.target_count - (mission_mgr.kill_count if mission_mgr else 0)
		base_count = min(base_count, remaining)
		
	for i in range(base_count):
		if current_wave >= 3 and i == base_count - 1:
			spawn_queue.append("heavy")
		elif current_wave >= 2 and i % 3 == 1:
			spawn_queue.append("fast")
		else:
			spawn_queue.append("normal")

func _process_spawn_queue():
	if is_spawning: return
	is_spawning = true
	
	while not spawn_queue.is_empty():
		# Maintain active zombie cap for mobile performance
		while active_zombies.size() >= max_active_zombies:
			await get_tree().create_timer(0.6).timeout
			_cleanup_dead_zombies()
			
		if spawn_queue.is_empty():
			break
			
		var archetype = spawn_queue.pop_front()
		_spawn_zombie(archetype)
		await get_tree().create_timer(spawn_interval).timeout
		_cleanup_dead_zombies()
		
	is_spawning = false
	_check_wave_status()

func _spawn_zombie(archetype: String):
	if spawn_points.is_empty() or not zombie_scene:
		return
		
	var valid_points = []
	var player_pos = player_ref.global_position if player_ref else Vector3.ZERO
	
	for p in spawn_points:
		if p is SpawnPoint:
			if p.is_valid_for_spawn(player_pos):
				valid_points.append(p)
		else:
			# Standard Node3D check (>10m distance from player)
			if p.global_position.distance_to(player_pos) > 10.0:
				valid_points.append(p)
				
	var spawn_node = valid_points.pick_random() if not valid_points.is_empty() else spawn_points.pick_random()
	if not spawn_node: return
	
	var zombie = zombie_scene.instantiate()
	zombie.archetype = archetype
	get_parent().add_child(zombie)
	zombie.global_position = spawn_node.global_position
	
	active_zombies.append(zombie)
	zombie.tree_exited.connect(_on_zombie_removed.bind(zombie))

func _on_zombie_removed(zombie: Node3D):
	if zombie in active_zombies:
		active_zombies.erase(zombie)
	_check_wave_status()

func _cleanup_dead_zombies():
	var valid = []
	for z in active_zombies:
		if is_instance_valid(z) and not z.is_queued_for_deletion():
			valid.append(z)
	active_zombies = valid

func _check_wave_status():
	_cleanup_dead_zombies()
	if not is_spawning and spawn_queue.is_empty() and active_zombies.is_empty():
		wave_cleared.emit(current_wave)
		var event_bus = get_node_or_null("/root/EventBus")
		if event_bus:
			event_bus.wave_completed.emit(current_wave)
			
		var mission_mgr = get_node_or_null("/root/MissionManager")
		if mission_mgr:
			mission_mgr.on_wave_completed()
			
		if current_wave < total_waves:
			await get_tree().create_timer(inter_wave_delay).timeout
			start_next_wave()
		else:
			all_waves_completed.emit()
