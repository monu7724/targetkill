extends CharacterBody3D

@onready var nav_agent = $NavigationAgent3D
@onready var anim_player = $AnimationPlayer
@onready var health_component = $HealthComponent
@onready var sfx_growl = $SfxGrowl
@onready var sfx_attack = $SfxAttack
@onready var sfx_death = $SfxDeath
@onready var sfx_timer = $SfxTimer

@export var move_speed: float = 2.0
@export var attack_range: float = 1.5
@export var attack_damage: float = 10.0
@export var reward_on_kill: int = 10
@export var archetype: String = "normal"

var player = null
var is_dead: bool = false
var path_update_timer: float = 0.0
var path_update_interval: float = 0.5 # Update path every 0.5s

func _ready():
	health_component.died.connect(_on_died)
	player = get_tree().get_first_node_in_group("player")
	sfx_timer.start(randf_range(3.0, 7.0))
	
	# Archetype adjustments
	match archetype:
		"fast":
			move_speed = 4.0
			health_component.max_health = 25.0
			health_component.current_health = 25.0
		"heavy":
			move_speed = 1.0
			health_component.max_health = 150.0
			health_component.current_health = 150.0
			attack_damage = 25.0
		"boss":
			scale *= 1.5
			move_speed = 1.5
			health_component.max_health = 500.0
			health_component.current_health = 500.0
			var timer = Timer.new()
			timer.wait_time = 5.0
			timer.autostart = true
			timer.timeout.connect(_on_boss_special)
			add_child(timer)

func _on_boss_special():
	if is_dead or archetype != "boss": return
	anim_player.play("attack")
	if player and global_position.distance_to(player.global_position) < 10.0:
		if player.has_method("apply_shake"):
			player.apply_shake(0.5)

func _physics_process(delta):
	if is_dead or not player:
		return
		
	var target_pos = player.global_position
	
	# Optimize pathfinding updates
	path_update_timer -= delta
	if path_update_timer <= 0:
		nav_agent.target_position = target_pos
		path_update_timer = path_update_interval
	
	if global_position.distance_to(target_pos) < attack_range:
		_attack()
		return
		
	if not nav_agent.is_navigation_finished():
		var next_path_pos = nav_agent.get_next_path_position()
		var new_velocity = (next_path_pos - global_position).normalized() * move_speed
		velocity = new_velocity
		move_and_slide()
	
	# Only look at player if reasonably close or moving
	if global_position.distance_to(target_pos) < 20.0 or velocity.length() > 0.1:
		var target_look = Vector3(target_pos.x, global_position.y, target_pos.z)
		if global_position.distance_to(target_look) > 0.01:
			look_at(target_look, Vector3.UP)
	
	if velocity.length() > 0.1:
		if not anim_player.is_playing() or anim_player.current_animation != "walk":
			anim_player.play("walk")

func _attack():
	if not anim_player.is_playing() or anim_player.current_animation != "attack":
		anim_player.play("attack")
		sfx_attack.play()

func take_damage(amount: float):
	if is_dead:
		return
	health_component.take_damage(amount)
	if anim_player.current_animation != "attack":
		anim_player.play("hit_react")

func _on_died():
	if is_dead: return
	is_dead = true
	sfx_death.play()
	anim_player.play("death")
	collision_layer = 0
	collision_mask = 0
	
	MissionManager.on_zombie_killed()
	SaveManager.add_coins(reward_on_kill)
	
	await get_tree().create_timer(3.0).timeout
	queue_free()

func _on_sfx_timer_timeout():
	if not is_dead:
		sfx_growl.play()
		sfx_timer.start(randf_range(5.0, 10.0))
