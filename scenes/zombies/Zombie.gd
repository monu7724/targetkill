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

var archetype_data = {
	"normal": {
		"mesh": "res://models/zombies/zombie_normal.obj",
		"material": "res://resources/materials/mat_zombie_normal.tres",
		"hp": 50.0,
		"speed": 2.2,
		"damage": 12.0,
		"scale": Vector3(1, 1, 1),
		"reward": 10
	},
	"fast": {
		"mesh": "res://models/zombies/zombie_fast.obj",
		"material": "res://resources/materials/mat_zombie_fast.tres",
		"hp": 30.0,
		"speed": 4.2,
		"damage": 10.0,
		"scale": Vector3(0.95, 0.95, 0.95),
		"reward": 15
	},
	"heavy": {
		"mesh": "res://models/zombies/zombie_heavy.obj",
		"material": "res://resources/materials/mat_zombie_heavy.tres",
		"hp": 160.0,
		"speed": 1.4,
		"damage": 26.0,
		"scale": Vector3(1.2, 1.2, 1.2),
		"reward": 25
	},
	"boss": {
		"mesh": "res://models/zombies/zombie_boss.obj",
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

func _apply_archetype():
	var cfg = archetype_data.get(archetype, archetype_data["normal"])
	if mesh_instance:
		var m_res = load(cfg.mesh)
		var mat_res = load(cfg.material)
		mesh_instance.mesh = m_res
		mesh_instance.material_override = mat_res
	
	scale = cfg.scale
	move_speed = cfg.speed
	attack_damage = cfg.damage
	reward_on_kill = cfg.reward
	health_component.max_health = cfg.hp
	health_component.current_health = cfg.hp
	
	if archetype == "boss":
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("show_boss_health"):
			hud.show_boss_health("THE ALPHA MUTANT", cfg.hp)

func _on_health_changed(hp):
	if archetype == "boss":
		var hud = get_tree().get_first_node_in_group("hud")
		if hud and hud.has_method("update_boss_health"):
			hud.update_boss_health(hp)

func take_damage(amount: float):
	if is_dead:
		return
	health_component.take_damage(amount)
	if not is_dead and anim_player.has_animation("hit_react") and anim_player.current_animation != "attack":
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
		if not anim_player.is_playing() or (anim_player.current_animation != "walk" and anim_player.current_animation != "attack"):
			anim_player.play("walk")

func _attack():
	if attack_timer > 0.0:
		return
	
	attack_timer = attack_interval
	if anim_player.has_animation("attack"):
		anim_player.play("attack")
	sfx_attack.play()
	
	if player and player.has_method("take_damage"):
		player.take_damage(attack_damage)

func _on_died():
	if is_dead: return
	is_dead = true
	sfx_death.play()
	anim_player.play("death")
	collision_layer = 0
	collision_mask = 0
	
	if archetype == "boss":
		MissionManager.on_boss_killed()
	else:
		MissionManager.on_zombie_killed()
	SaveManager.add_coins(reward_on_kill)
	
	await get_tree().create_timer(1.2).timeout
	queue_free()

func _on_sfx_timer_timeout():
	if not is_dead:
		sfx_growl.play()
		sfx_timer.start(randf_range(5.0, 9.0))
