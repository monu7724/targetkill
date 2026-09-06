class_name InfectedDog
extends "res://scripts/Zombies/EnemyBase.gd"

@onready var head_hit_zone = $HeadHitZone
@onready var body_hit_zone = $BodyHitZone

func _init():
	super._init()
	archetype = "dog"
	move_speed = 4.5
	attack_range = 2.0
	attack_damage = 12.0
	attack_interval = 1.8
	reward_on_kill = 15

func _ready():
	archetype = "dog"
	super._ready()
	_setup_dog_model()
	_setup_hit_zones()

func _setup_dog_model():
	# If model_instance wasn't already set up by _apply_archetype, ensure infected_dog.glb is wired
	if not model_instance:
		model_instance = get_node_or_null("SkeletalModel")
	if model_instance:
		var anims = model_instance.find_children("*", "AnimationPlayer", true, false)
		if not anims.is_empty():
			active_anim_player = anims[0]
			active_anim_player.speed_scale = randf_range(1.05, 1.25)

func _setup_hit_zones():
	for child in get_children():
		if child is HitZone:
			child.parent_entity = self

func take_damage(amount: float, is_headshot: bool = false, hit_dir: Vector3 = Vector3.ZERO):
	if is_dead:
		return
	last_hit_was_headshot = is_headshot
	if health_component:
		health_component.take_damage(amount)
	if is_dead:
		return
		
	# Dog specific hurt reactions
	if is_headshot:
		if active_anim_player and active_anim_player.has_animation("hit_head"):
			_play_anim("hit_head")
		elif active_anim_player and active_anim_player.has_animation("headshot_reaction"):
			_play_anim("headshot_reaction")
		elif active_anim_player and active_anim_player.has_animation("stagger"):
			_play_anim("stagger")
		ai_state = AIState.STAGGER
		stagger_timer = 0.35
	elif amount >= 20.0:
		if active_anim_player and active_anim_player.has_animation("hit_body"):
			_play_anim("hit_body")
		elif active_anim_player and active_anim_player.has_animation("stagger"):
			_play_anim("stagger")
		ai_state = AIState.STAGGER
		stagger_timer = 0.40

func _on_died():
	if is_dead: return
	is_dead = true
	ai_state = AIState.DEAD
	
	if collision_shape:
		collision_shape.set_deferred("disabled", true)
	for child in get_children():
		if child is HitZone:
			for col in child.find_children("*", "CollisionShape3D", true, false):
				col.set_deferred("disabled", true)
				
	velocity = Vector3.ZERO
	_play_anim("death")
	
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
		mission_mgr.on_zombie_killed()
		
	await get_tree().create_timer(2.5).timeout
	queue_free()
