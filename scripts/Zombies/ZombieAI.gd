extends CharacterBody3D

enum AIState {
	IDLE,
	WANDER,
	NOTICE_PLAYER,
	CHASE,
	ATTACK,
	STAGGER,
	SEARCH,
	LOST_PLAYER,
	DEAD
}

@onready var nav_agent: NavigationAgent3D = $NavigationAgent3D
@onready var anim_player: AnimationPlayer = $AnimationPlayer
@onready var health_component = $HealthComponent
@onready var mesh_instance: MeshInstance3D = $MeshInstance3D
@onready var collision_shape = $CollisionShape3D
@onready var sfx_growl: AudioStreamPlayer3D = $SfxGrowl
@onready var sfx_attack: AudioStreamPlayer3D = $SfxAttack
@onready var sfx_death: AudioStreamPlayer3D = $SfxDeath
@onready var sfx_timer: Timer = $SfxTimer

@export var move_speed: float = 2.2
@export var attack_range: float = 1.7
@export var attack_damage: float = 12.0
@export var reward_on_kill: int = 10
@export var archetype: String = "normal"
@export var attack_interval: float = 1.2
@export var sight_range: float = 35.0

var ai_state: AIState = AIState.CHASE
var player: Node3D = null
var is_dead: bool = false
var path_update_timer: float = 0.0
var path_update_interval: float = 0.35
var attack_timer: float = 1.0
var stagger_timer: float = 0.0
var search_timer: float = 0.0
var last_known_player_pos: Vector3 = Vector3.ZERO
var has_los_to_player: bool = false

var model_instance: Node3D = null
var active_anim_player: AnimationPlayer = null

var archetype_data = {
	"normal": {
		"mesh": "res://assets/3d/zombies/zombie_normal.glb",
		"material": "res://resources/materials/mat_zombie_normal.tres",
		"hp": 50.0,
		"speed": 2.2,
		"damage": 12.0,
		"scale": Vector3(1, 1, 1),
		"reward": 10
	},
	"fast": {
		"mesh": "res://assets/3d/zombies/zombie_fast.glb",
		"material": "res://resources/materials/mat_zombie_fast.tres",
		"hp": 30.0,
		"speed": 4.2,
		"damage": 10.0,
		"scale": Vector3(0.95, 0.95, 0.95),
		"reward": 15
	},
	"heavy": {
		"mesh": "res://assets/3d/zombies/zombie_heavy.glb",
		"material": "res://resources/materials/mat_zombie_heavy.tres",
		"hp": 160.0,
		"speed": 1.4,
		"damage": 26.0,
		"scale": Vector3(1.2, 1.2, 1.2),
		"reward": 25
	},
	"boss": {
		"mesh": "res://assets/3d/zombies/zombie_boss.glb",
		"material": "res://resources/materials/mat_zombie_boss.tres",
		"hp": 500.0,
		"speed": 1.8,
		"damage": 40.0,
		"scale": Vector3(1.45, 1.45, 1.45),
		"reward": 100
	}
}

func _ready():
	health_component.died.connect(_on_died)
	health_component.health_changed.connect(_on_health_changed)
	player = get_tree().get_first_node_in_group("player")
	attack_timer = 1.2
	sfx_timer.start(randf_range(3.0, 6.0))
	_apply_archetype()

func _extract_mesh_from_scene(packed_scene: PackedScene) -> Mesh:
	if not packed_scene: return null
	var inst = packed_scene.instantiate()
	var mesh_nodes = inst.find_children("*", "MeshInstance3D", true, false)
	var result_mesh: Mesh = null
	if not mesh_nodes.is_empty() and mesh_nodes[0].mesh:
		result_mesh = mesh_nodes[0].mesh
	inst.queue_free()
	return result_mesh

func _apply_archetype():
	var cfg = archetype_data.get(archetype, archetype_data["normal"])
	var res = load(cfg.mesh)
	
	if res is PackedScene:
		var m = _extract_mesh_from_scene(res)
		if m and mesh_instance:
			mesh_instance.mesh = m
			mesh_instance.material_override = null
			mesh_instance.visible = false
			
		if model_instance:
			model_instance.queue_free()
			model_instance = null
			
		model_instance = res.instantiate()
		model_instance.name = "SkeletalModel"
		add_child(model_instance)
		
		var anims = model_instance.find_children("*", "AnimationPlayer", true, false)
		if not anims.is_empty():
			active_anim_player = anims[0]
			active_anim_player.speed_scale = randf_range(0.92, 1.12)
			
		# Low-cost material appearance variations (Civilian, Airport Worker, Runner)
		var sk_mesh: MeshInstance3D = model_instance.find_child("*Mesh*", true, false)
		if sk_mesh and sk_mesh.mesh:
			var hue_shift = randf_range(-0.08, 0.08)
			var val_shift = randf_range(0.90, 1.10)
			for s_idx in range(sk_mesh.mesh.get_surface_count()):
				var mat = sk_mesh.get_active_material(s_idx)
				if mat is StandardMaterial3D:
					var new_mat = mat.duplicate()
					if "Shirt" in mat.resource_name or "Top" in mat.resource_name or s_idx == 3:
						new_mat.albedo_color = Color.from_hsv(fposmod(new_mat.albedo_color.h + randf_range(-0.15, 0.15), 1.0), clamp(new_mat.albedo_color.s * randf_range(0.8, 1.2), 0.0, 1.0), clamp(new_mat.albedo_color.v * randf_range(0.8, 1.2), 0.0, 1.0))
					elif "Flesh" in mat.resource_name or s_idx == 0:
						new_mat.albedo_color = new_mat.albedo_color * Color(1.0 + hue_shift, 1.0 - abs(hue_shift), 1.0 - hue_shift, 1.0) * val_shift
					sk_mesh.set_surface_override_material(s_idx, new_mat)
	elif res is Mesh and mesh_instance:
		var mat_res = load(cfg.material)
		mesh_instance.mesh = res
		mesh_instance.material_override = mat_res
		mesh_instance.visible = true
	
	scale = cfg.scale * randf_range(0.96, 1.04)
	move_speed = cfg.speed
	attack_damage = cfg.damage
	reward_on_kill = cfg.reward
	health_component.max_health = cfg.hp
	health_component.current_health = cfg.hp
	
	if archetype == "boss":
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("show_boss_health"):
			hud.show_boss_health("THE ALPHA MUTANT", cfg.hp)

func _play_anim(anim_name: String, custom_blend: float = -1.0):
	if active_anim_player and active_anim_player.has_animation(anim_name):
		active_anim_player.play(anim_name, custom_blend)
	elif anim_player and anim_player.has_animation(anim_name):
		anim_player.play(anim_name, custom_blend)

func _on_health_changed(hp):
	if archetype == "boss":
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("update_boss_health"):
			hud.update_boss_health(hp)

var last_hit_was_headshot: bool = false

func take_damage(amount: float, is_headshot: bool = false, hit_dir: Vector3 = Vector3.ZERO):
	if is_dead:
		return
	last_hit_was_headshot = is_headshot
	health_component.take_damage(amount)
	if is_dead:
		return
		
	# Hurt reactions
	if is_headshot and (active_anim_player and active_anim_player.has_animation("headshot_reaction")):
		_play_anim("headshot_reaction")
		ai_state = AIState.STAGGER
		stagger_timer = 0.4
	elif amount > 25.0 and (active_anim_player and active_anim_player.has_animation("stagger")):
		_play_anim("stagger")
		ai_state = AIState.STAGGER
		stagger_timer = 0.55
	elif hit_dir != Vector3.ZERO:
		var local_dir = global_transform.basis.inverse() * hit_dir
		if abs(local_dir.x) > abs(local_dir.z):
			if local_dir.x > 0 and (active_anim_player and active_anim_player.has_animation("hit_right")):
				_play_anim("hit_right")
			elif active_anim_player and active_anim_player.has_animation("hit_left"):
				_play_anim("hit_left")
			else:
				_play_anim("hit_front")
		elif local_dir.z > 0 and (active_anim_player and active_anim_player.has_animation("hit_back")):
			_play_anim("hit_back")
		else:
			_play_anim("hit_front")
	elif active_anim_player and active_anim_player.has_animation("hit_front"):
		_play_anim("hit_front")
	elif active_anim_player and active_anim_player.has_animation("hit"):
		_play_anim("hit")

func _check_line_of_sight() -> bool:
	if not player: return false
	var space = get_world_3d().direct_space_state
	var start = global_position + Vector3(0, 1.4, 0)
	var end = player.global_position + Vector3(0, 1.2, 0)
	var query = PhysicsRayQueryParameters3D.create(start, end)
	query.exclude = [self]
	var res = space.intersect_ray(query)
	if res.is_empty():
		return true
	if res.collider == player or res.collider.is_in_group("player"):
		return true
	return false

func _physics_process(delta):
	if is_dead:
		return
	if not player:
		player = get_tree().get_first_node_in_group("player")
		if not player:
			return
		
	var dist_to_player = global_position.distance_to(player.global_position)
	attack_timer -= delta
	
	# Stagger recovery
	if ai_state == AIState.STAGGER:
		stagger_timer -= delta
		velocity = velocity.move_toward(Vector3.ZERO, 6.0 * delta)
		move_and_slide()
		if stagger_timer <= 0:
			ai_state = AIState.CHASE
		return

	# Line of Sight & Target Tracking
	path_update_timer -= delta
	if path_update_timer <= 0:
		has_los_to_player = _check_line_of_sight()
		if has_los_to_player:
			last_known_player_pos = player.global_position
			if ai_state == AIState.SEARCH or ai_state == AIState.IDLE or ai_state == AIState.LOST_PLAYER:
				ai_state = AIState.CHASE
		else:
			if ai_state == AIState.CHASE and dist_to_player > attack_range * 1.5:
				ai_state = AIState.SEARCH
				search_timer = 4.0
				
		path_update_timer = path_update_interval

	# AI State Machine
	match ai_state:
		AIState.CHASE:
			_handle_chase(dist_to_player, delta)
		AIState.ATTACK:
			_handle_attack(dist_to_player, delta)
		AIState.SEARCH:
			_handle_search(delta)
		AIState.LOST_PLAYER, AIState.IDLE:
			velocity = velocity.move_toward(Vector3.ZERO, 4.0 * delta)
			move_and_slide()
			_play_anim("idle")
			if dist_to_player < sight_range and has_los_to_player:
				ai_state = AIState.CHASE

func _handle_chase(dist_to_player: float, delta: float):
	if dist_to_player <= attack_range:
		ai_state = AIState.ATTACK
		velocity = Vector3.ZERO
		return
		
	# Look towards player
	var look_target = player.global_position
	look_target.y = global_position.y
	if global_position.distance_to(look_target) > 0.1:
		look_at(look_target, Vector3.UP)
	
	var dir = (player.global_position - global_position).normalized()
	dir.y = 0.0
	velocity = dir * move_speed
	move_and_slide()
	
	var walk_anim = "run" if archetype == "fast" else ("heavy_walk" if archetype == "heavy" else "walk")
	if active_anim_player and active_anim_player.current_animation != walk_anim:
		_play_anim(walk_anim)

func _handle_attack(dist_to_player: float, _delta: float):
	velocity = Vector3.ZERO
	move_and_slide()
	
	var look_target = player.global_position
	look_target.y = global_position.y
	if global_position.distance_to(look_target) > 0.1:
		look_at(look_target, Vector3.UP)
		
	if dist_to_player > attack_range * 1.3:
		ai_state = AIState.CHASE
		return
		
	if attack_timer <= 0:
		attack_timer = attack_interval
		var atk_anim = "heavy_attack" if (archetype in ["heavy", "boss"]) else "attack"
		_play_anim(atk_anim)
		if sfx_attack:
			sfx_attack.play()
		_perform_attack_strike()

func _handle_search(delta: float):
	search_timer -= delta
	var dist_to_last = global_position.distance_to(last_known_player_pos)
	if dist_to_last > 1.5:
		var dir = (last_known_player_pos - global_position).normalized()
		dir.y = 0.0
		velocity = dir * (move_speed * 0.75)
		look_at(last_known_player_pos, Vector3.UP)
		move_and_slide()
		_play_anim("walk")
	else:
		velocity = Vector3.ZERO
		move_and_slide()
		_play_anim("idle")
		if search_timer <= 0:
			ai_state = AIState.LOST_PLAYER

func _perform_attack_strike():
	await get_tree().create_timer(0.35).timeout
	if is_dead: return
	if player and global_position.distance_to(player.global_position) <= attack_range * 1.25:
		if player.has_method("take_damage"):
			player.take_damage(attack_damage)

func _on_died():
	if is_dead: return
	is_dead = true
	ai_state = AIState.DEAD
	
	collision_shape.set_deferred("disabled", true)
	velocity = Vector3.ZERO
	
	_play_anim("death")
	if sfx_death:
		sfx_death.play()
		
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.enemy_killed.emit(archetype, last_hit_was_headshot, global_position)
		
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr:
		save_mgr.add_coins(reward_on_kill)
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		if archetype == "boss":
			mission_mgr.on_boss_killed()
		else:
			mission_mgr.on_zombie_killed()
			
	await get_tree().create_timer(2.2).timeout
	queue_free()

func _on_sfx_timer_timeout():
	if not is_dead and sfx_growl:
		sfx_growl.play()
		sfx_timer.start(randf_range(4.0, 8.0))
