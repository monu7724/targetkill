extends CharacterBody3D

@onready var nav_agent = $NavigationAgent3D
@onready var anim_player = $AnimationPlayer
@onready var health_component = $HealthComponent
@onready var mesh_instance = $MeshInstance3D
@onready var collision_shape = $CollisionShape3D
@onready var sfx_growl = $SfxGrowl
@onready var sfx_attack = $SfxAttack
@onready var sfx_death = $SfxDeath
@onready var sfx_timer = $SfxTimer

@export var move_speed: float = 2.2
@export var attack_range: float = 1.6
@export var attack_damage: float = 12.0
@export var reward_on_kill: int = 10
@export var archetype: String = "normal"
@export var attack_interval: float = 1.1

var player = null
var is_dead: bool = false
var path_update_timer: float = 0.0
var path_update_interval: float = 0.4
var attack_timer: float = 1.0

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
			mesh_instance.visible = false # Skinned model will be rendered by model_instance
			
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
			
		# Apply subtle controlled variation (Section 4)
		var sk_mesh: MeshInstance3D = model_instance.find_child("*Mesh*", true, false)
		if sk_mesh and sk_mesh.mesh:
			var hue_shift = randf_range(-0.06, 0.06)
			var val_shift = randf_range(0.92, 1.08)
			for s_idx in range(sk_mesh.mesh.get_surface_count()):
				var mat = sk_mesh.get_active_material(s_idx)
				if mat is StandardMaterial3D:
					var new_mat = mat.duplicate()
					if "Shirt" in mat.resource_name or "Top" in mat.resource_name or s_idx == 3:
						new_mat.albedo_color = Color.from_hsv(fposmod(new_mat.albedo_color.h + randf_range(-0.12, 0.12), 1.0), clamp(new_mat.albedo_color.s * randf_range(0.85, 1.15), 0.0, 1.0), clamp(new_mat.albedo_color.v * randf_range(0.85, 1.15), 0.0, 1.0))
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

func take_damage(amount: float, is_headshot: bool = false, hit_dir: Vector3 = Vector3.ZERO):
	if is_dead:
		return
	health_component.take_damage(amount)
	if is_dead:
		return
		
	if is_headshot and (active_anim_player and active_anim_player.has_animation("headshot_reaction")):
		_play_anim("headshot_reaction")
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
	elif amount > 25.0 and (active_anim_player and active_anim_player.has_animation("stagger")):
		_play_anim("stagger")
	elif active_anim_player and active_anim_player.has_animation("hit_front"):
		_play_anim("hit_front")
	elif active_anim_player and active_anim_player.has_animation("hit"):
		_play_anim("hit")
	elif anim_player.has_animation("hit_react") and anim_player.current_animation != "attack":
		anim_player.play("hit_react")

func _physics_process(delta):
	if is_dead:
		return
	if not player:
		player = get_tree().get_first_node_in_group("player")
		if not player:
			return
		
	var target_pos = player.global_position
	attack_timer -= delta
	
	path_update_timer -= delta
	if path_update_timer <= 0:
		nav_agent.target_position = target_pos
		path_update_timer = path_update_interval
	
	if global_position.distance_to(target_pos) <= attack_range:
		_attack()
		return
		
	var move_dir = (target_pos - global_position)
	move_dir.y = 0.0
	if not nav_agent.is_navigation_finished():
		var next_path_pos = nav_agent.get_next_path_position()
		var nav_dir = (next_path_pos - global_position)
		nav_dir.y = 0.0
		if nav_dir.length() > 0.1:
			move_dir = nav_dir
			
	if move_dir.length() > 0.01:
		velocity = move_dir.normalized() * move_speed
		move_and_slide()
	
	# Rotate towards player
	if global_position.distance_to(target_pos) < 25.0 or velocity.length() > 0.1:
		var target_look = Vector3(target_pos.x, global_position.y, target_pos.z)
		if global_position.distance_to(target_look) > 0.01:
			look_at(target_look, Vector3.UP)
	
	if velocity.length() > 0.1:
		var move_anim = "walk"
		if archetype == "fast":
			move_anim = "run"
		elif archetype == "heavy":
			move_anim = "heavy_walk"
		elif archetype == "normal" and global_position.distance_to(target_pos) > 10.0:
			move_anim = "fast_walk"
			
		var cur_anim = active_anim_player.current_animation if active_anim_player else anim_player.current_animation
		if cur_anim != move_anim and not cur_anim.begins_with("attack") and not cur_anim.begins_with("heavy_attack") and cur_anim != "stagger":
			_play_anim(move_anim)
	else:
		var cur_anim = active_anim_player.current_animation if active_anim_player else anim_player.current_animation
		if cur_anim != "idle" and not cur_anim.begins_with("attack") and not cur_anim.begins_with("heavy_attack") and cur_anim != "stagger":
			_play_anim("idle")

func _attack():
	if attack_timer > 0.0:
		return
	
	attack_timer = attack_interval
	if archetype == "heavy":
		_play_anim("heavy_attack")
	elif archetype == "boss":
		if randf() > 0.4:
			_play_anim("heavy_attack")
		else:
			_play_anim("roar")
	else:
		_play_anim("attack")
	sfx_attack.play()
	
	if player and player.has_method("take_damage"):
		player.take_damage(attack_damage)

func _on_died():
	if is_dead: return
	is_dead = true
	sfx_death.play()
	_play_anim("death")
	collision_layer = 0
	collision_mask = 0
	
	var mm = get_node_or_null("/root/MissionManager")
	if mm:
		if archetype == "boss":
			mm.on_boss_killed()
		else:
			mm.on_zombie_killed()
	var sm = get_node_or_null("/root/SaveManager")
	if sm:
		sm.add_coins(reward_on_kill)
	
	await get_tree().create_timer(1.3).timeout
	queue_free()

func _on_sfx_timer_timeout():
	if not is_dead:
		sfx_growl.play()
		sfx_timer.start(randf_range(5.0, 9.0))
