class_name EnemyBase
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

@export var move_speed: float = 2.2
@export var attack_range: float = 1.7
@export var attack_damage: float = 12.0
@export var reward_on_kill: int = 10
@export var archetype: String = "normal"
@export var attack_interval: float = 1.2
@export var sight_range: float = 35.0
@export var fly_height: float = 0.0

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

# Core node references (dynamically resolved to allow custom scene hierarchies)
var nav_agent: NavigationAgent3D = null
var anim_player: AnimationPlayer = null
var health_component: Node = null
var mesh_instance: MeshInstance3D = null
var collision_shape: CollisionShape3D = null
var sfx_growl: AudioStreamPlayer3D = null
var sfx_attack: AudioStreamPlayer3D = null
var sfx_death: AudioStreamPlayer3D = null
var sfx_timer: Timer = null

var archetype_data = {
	"normal": {
		"mesh": "res://assets/3d/zombies/zombie_normal.glb",
		"material": "res://resources/materials/mat_zombie_normal.tres",
		"hp": 50.0,
		"speed": 1.4,
		"damage": 6.0,
		"scale": Vector3(1, 1, 1),
		"reward": 10,
		"attack_range": 1.7,
		"attack_interval": 1.2
	},
	"fast": {
		"mesh": "res://assets/3d/zombies/zombie_fast.glb",
		"material": "res://resources/materials/mat_zombie_fast.tres",
		"hp": 30.0,
		"speed": 2.8,
		"damage": 5.0,
		"scale": Vector3(0.95, 0.95, 0.95),
		"reward": 15,
		"attack_range": 1.7,
		"attack_interval": 1.0
	},
	"heavy": {
		"mesh": "res://assets/3d/zombies/zombie_heavy.glb",
		"material": "res://resources/materials/mat_zombie_heavy.tres",
		"hp": 160.0,
		"speed": 0.8,
		"damage": 14.0,
		"scale": Vector3(1.2, 1.2, 1.2),
		"reward": 25,
		"attack_range": 2.2,
		"attack_interval": 1.8
	},
	"special": {
		"mesh": "res://assets/3d/zombies/zombie_normal.glb",
		"material": "res://resources/materials/mat_zombie_normal.tres",
		"hp": 40.0,
		"speed": 1.2,
		"damage": 8.0,
		"scale": Vector3(0.9, 0.9, 0.9),
		"reward": 20,
		"attack_range": 14.0,
		"attack_interval": 2.5
	},
	"spitter": {
		"mesh": "res://assets/3d/zombies/zombie_normal.glb",
		"material": "res://resources/materials/mat_zombie_normal.tres",
		"hp": 40.0,
		"speed": 1.2,
		"damage": 8.0,
		"scale": Vector3(0.9, 0.9, 0.9),
		"reward": 20,
		"attack_range": 14.0,
		"attack_interval": 2.5
	},
	"dog": {
		"mesh": "res://assets/3d/zombies/infected_dog.glb",
		"material": "res://resources/materials/mat_zombie_fast.tres",
		"hp": 50.0,
		"speed": 4.5,
		"damage": 12.0,
		"scale": Vector3(1.0, 1.0, 1.0),
		"reward": 15,
		"attack_range": 2.0,
		"attack_interval": 1.8
	},
	"rat": {
		"mesh": "",
		"material": "",
		"hp": 15.0,
		"speed": 3.8,
		"damage": 3.0,
		"scale": Vector3(0.35, 0.35, 0.35),
		"reward": 5,
		"attack_range": 1.2,
		"attack_interval": 0.8
	},
	"rats": {
		"mesh": "",
		"material": "",
		"hp": 15.0,
		"speed": 3.8,
		"damage": 3.0,
		"scale": Vector3(0.35, 0.35, 0.35),
		"reward": 5,
		"attack_range": 1.2,
		"attack_interval": 0.8
	},
	"bat": {
		"mesh": "",
		"material": "",
		"hp": 12.0,
		"speed": 3.6,
		"damage": 4.0,
		"scale": Vector3(0.4, 0.4, 0.4),
		"reward": 5,
		"attack_range": 1.5,
		"attack_interval": 1.0,
		"fly_height": 2.2
	},
	"bats": {
		"mesh": "",
		"material": "",
		"hp": 12.0,
		"speed": 3.6,
		"damage": 4.0,
		"scale": Vector3(0.4, 0.4, 0.4),
		"reward": 5,
		"attack_range": 1.5,
		"attack_interval": 1.0,
		"fly_height": 2.2
	},
	"boss": {
		"mesh": "res://assets/3d/zombies/zombie_boss.glb",
		"material": "res://resources/materials/mat_zombie_boss.tres",
		"hp": 500.0,
		"speed": 1.1,
		"damage": 22.0,
		"scale": Vector3(1.45, 1.45, 1.45),
		"reward": 100,
		"attack_range": 2.5,
		"attack_interval": 2.0
	}
}

func _init():
	add_to_group("zombies")

func _ready():
	_resolve_nodes()
	if health_component:
		health_component.died.connect(_on_died)
		health_component.health_changed.connect(_on_health_changed)
	player = get_tree().get_first_node_in_group("player")
	attack_timer = 1.2
	if sfx_timer:
		sfx_timer.start(randf_range(3.0, 6.0))
	_apply_archetype()

func _resolve_nodes():
	if not nav_agent: nav_agent = get_node_or_null("NavigationAgent3D")
	if not anim_player: anim_player = get_node_or_null("AnimationPlayer")
	if not health_component: health_component = get_node_or_null("HealthComponent")
	if not mesh_instance: mesh_instance = get_node_or_null("MeshInstance3D")
	if not collision_shape: collision_shape = get_node_or_null("CollisionShape3D")
	if not sfx_growl: sfx_growl = get_node_or_null("SfxGrowl")
	if not sfx_attack: sfx_attack = get_node_or_null("SfxAttack")
	if not sfx_death: sfx_death = get_node_or_null("SfxDeath")
	if not sfx_timer: sfx_timer = get_node_or_null("SfxTimer")

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
	if cfg.has("attack_range"): attack_range = cfg.attack_range
	if cfg.has("attack_interval"): attack_interval = cfg.attack_interval
	if cfg.has("fly_height"): fly_height = cfg.fly_height
	
	if cfg.mesh != "" and ResourceLoader.exists(cfg.mesh):
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
				
			var wrapper = Node3D.new()
			wrapper.name = "ModelWrapper"
			wrapper.rotation.y = PI
			add_child(wrapper)
			
			model_instance = res.instantiate()
			model_instance.name = "SkeletalModel"
			wrapper.add_child(model_instance)
			
			var anims = model_instance.find_children("*", "AnimationPlayer", true, false)
			if not anims.is_empty():
				active_anim_player = anims[0]
				active_anim_player.speed_scale = randf_range(0.92, 1.12)
				
			# Material appearance variation
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
			var mat_res = load(cfg.material) if cfg.material != "" and ResourceLoader.exists(cfg.material) else null
			mesh_instance.mesh = res
			mesh_instance.material_override = mat_res
			mesh_instance.visible = true
			mesh_instance.rotation.y = PI
	
	scale = cfg.scale * randf_range(0.96, 1.04)
	move_speed = cfg.speed
	attack_damage = cfg.damage
	reward_on_kill = cfg.reward
	if health_component:
		health_component.max_health = cfg.hp
		health_component.current_health = cfg.hp
		
	if archetype == "spitter" or archetype == "special":
		attack_range = 14.0
		if model_instance:
			var sk_mesh: MeshInstance3D = model_instance.find_child("*Mesh*", true, false)
			if sk_mesh and sk_mesh.mesh:
				for s_idx in range(sk_mesh.mesh.get_surface_count()):
					var mat = sk_mesh.get_active_material(s_idx)
					if mat is StandardMaterial3D:
						var new_mat = mat.duplicate()
						new_mat.albedo_color = Color(0.2, 0.9, 0.3, 1.0)
						sk_mesh.set_surface_override_material(s_idx, new_mat)
	elif archetype == "dog":
		attack_range = 2.0
		attack_interval = 1.8
		
	if archetype == "boss":
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("show_boss_health"):
			hud.show_boss_health("THE ALPHA MUTANT", cfg.hp)
		var event_bus = get_node_or_null("/root/EventBus")
		if event_bus and event_bus.has_signal("boss_spawned"):
			event_bus.boss_spawned.emit("THE ALPHA MUTANT", cfg.hp)

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
		var event_bus = get_node_or_null("/root/EventBus")
		if event_bus and event_bus.has_signal("boss_health_changed"):
			var max_hp = archetype_data["boss"]["hp"]
			event_bus.boss_health_changed.emit(hp, max_hp)

var last_hit_was_headshot: bool = false

func take_damage(amount: float, is_headshot: bool = false, hit_dir: Vector3 = Vector3.ZERO):
	if is_dead:
		return
	last_hit_was_headshot = is_headshot
	if health_component:
		health_component.take_damage(amount)
	if is_dead:
		return
		
	# Hurt reactions
	if is_headshot:
		if active_anim_player and active_anim_player.has_animation("headshot_reaction"):
			_play_anim("headshot_reaction")
		elif active_anim_player and active_anim_player.has_animation("hit_head"):
			_play_anim("hit_head")
		elif active_anim_player and active_anim_player.has_animation("stagger"):
			_play_anim("stagger")
		if model_instance:
			model_instance.rotation.x = -deg_to_rad(32.0)
			model_instance.position.y += 0.05
		ai_state = AIState.STAGGER
		stagger_timer = 0.45
	elif amount > 25.0:
		if active_anim_player and active_anim_player.has_animation("stagger"):
			_play_anim("stagger")
		elif active_anim_player and active_anim_player.has_animation("hit_body"):
			_play_anim("hit_body")
		if model_instance:
			model_instance.rotation.y += deg_to_rad(randf_range(-22.0, 22.0))
		ai_state = AIState.STAGGER
		stagger_timer = 0.55
	elif hit_dir != Vector3.ZERO:
		var local_dir = global_transform.basis.inverse() * hit_dir
		if abs(local_dir.x) > abs(local_dir.z):
			if local_dir.x > 0 and (active_anim_player and active_anim_player.has_animation("hit_right")):
				_play_anim("hit_right")
			elif active_anim_player and active_anim_player.has_animation("hit_left"):
				_play_anim("hit_left")
			elif active_anim_player and active_anim_player.has_animation("hit_body"):
				_play_anim("hit_body")
			else:
				_play_anim("hit_front")
		elif local_dir.z > 0 and (active_anim_player and active_anim_player.has_animation("hit_back")):
			_play_anim("hit_back")
		elif active_anim_player and active_anim_player.has_animation("hit_body"):
			_play_anim("hit_body")
		else:
			_play_anim("hit_front")
	elif active_anim_player and active_anim_player.has_animation("hit_body"):
		_play_anim("hit_body")
	elif active_anim_player and active_anim_player.has_animation("hit_front"):
		_play_anim("hit_front")
	elif active_anim_player and active_anim_player.has_animation("hit"):
		_play_anim("hit")

func take_hit(damage: float, impact_vector: Vector3 = Vector3.ZERO) -> Dictionary:
	take_damage(damage, false, impact_vector)
	return {
		"final_damage": damage,
		"is_headshot": false,
		"zone": "body"
	}

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
		if model_instance:
			model_instance.rotation.x = lerp(model_instance.rotation.x, 0.0, 5.0 * delta)
			model_instance.rotation.y = lerp(model_instance.rotation.y, 0.0, 5.0 * delta)
			model_instance.position.y = lerp(model_instance.position.y, 0.0, 5.0 * delta)
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
	if fly_height <= 0.0:
		look_target.y = global_position.y
	if global_position.distance_to(look_target) > 0.1:
		look_at(look_target, Vector3.UP)
	
	var dir = (player.global_position - global_position).normalized()
	if fly_height > 0.0:
		# Hover/swoop for airborne enemies
		var target_y = player.global_position.y + fly_height
		dir.y = clamp(target_y - global_position.y, -1.0, 1.0) * 0.5
	else:
		dir.y = 0.0
	velocity = dir * move_speed
	move_and_slide()
	
	var walk_anim = "run" if (archetype in ["fast", "dog"]) else ("heavy_walk" if archetype == "heavy" else "walk")
	if active_anim_player and active_anim_player.current_animation != walk_anim:
		_play_anim(walk_anim)
		
	# Organic humanoid/quadruped gait oscillation
	if model_instance and archetype != "dog":
		var wobble = sin(Time.get_ticks_msec() * 0.007) * 0.05
		var pitch_hitch = (sin(Time.get_ticks_msec() * 0.014) * 0.5 + 0.5) * 0.04
		model_instance.rotation.z = lerp(model_instance.rotation.z, wobble, 10.0 * delta)
		model_instance.rotation.x = lerp(model_instance.rotation.x, pitch_hitch, 10.0 * delta)

func _handle_attack(dist_to_player: float, _delta: float):
	velocity = Vector3.ZERO
	move_and_slide()
	
	var look_target = player.global_position
	if fly_height <= 0.0:
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

var acid_prefab = preload("res://scenes/zombies/AcidSpit.tscn")

func _perform_attack_strike():
	await get_tree().create_timer(0.35).timeout
	if is_dead: return
	if archetype == "spitter" or archetype == "special":
		if acid_prefab and player:
			var spit = acid_prefab.instantiate()
			get_tree().current_scene.add_child(spit)
			spit.global_position = global_position + Vector3(0, 1.2, 0)
			spit.direction = (player.global_position + Vector3(0, 1.0, 0) - spit.global_position).normalized()
	else:
		if player and global_position.distance_to(player.global_position) <= attack_range * 1.3:
			if player.has_method("take_damage"):
				player.take_damage(attack_damage)

func _on_died():
	if is_dead: return
	is_dead = true
	ai_state = AIState.DEAD
	
	if collision_shape:
		collision_shape.set_deferred("disabled", true)
	velocity = Vector3.ZERO
	
	_play_anim("death")
	if model_instance and archetype != "dog":
		var tw = create_tween()
		tw.tween_property(model_instance, "position:y", -0.4, 0.45).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
		tw.parallel().tween_property(model_instance, "rotation:x", deg_to_rad(75.0), 0.55).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	if sfx_death:
		sfx_death.play()
		
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.enemy_killed.emit(archetype, last_hit_was_headshot, global_position)
		
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr:
		save_mgr.add_cash(reward_on_kill)
		
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
		if sfx_timer:
			sfx_timer.start(randf_range(4.0, 8.0))
