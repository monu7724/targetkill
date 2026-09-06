class_name RealisticZombie
extends "res://scenes/zombies/Zombie.gd"

func _ready():
	archetype = "realistic"
	super._ready()
	_setup_animation_aliases()
	_setup_hitzones()

func _apply_archetype():
	if not model_instance:
		model_instance = get_node_or_null("SkeletalModel")
	if model_instance:
		var anims = model_instance.find_children("*", "AnimationPlayer", true, false)
		if not anims.is_empty():
			active_anim_player = anims[0]
			active_anim_player.speed_scale = randf_range(0.95, 1.05)
			
	if mesh_instance:
		mesh_instance.visible = false
		
	scale = Vector3.ONE
	move_speed = 1.35
	attack_range = 1.6
	attack_interval = 1.5
	attack_damage = 15.0
	reward_on_kill = 15
	if health_component:
		health_component.max_health = 60.0
		health_component.current_health = 60.0

func _setup_animation_aliases():
	if not active_anim_player:
		return
	var lib = active_anim_player.get_animation_library("")
	if not lib:
		return
	var alias_map = {
		"walk": ["Walk", "walk"],
		"idle": ["Idle", "idle", "HappyIdle"],
		"attack": ["Attack_mixamo_vitruvian", "Attack", "attack"],
		"death": ["Death_mixamo_vitruvian", "Death", "death"],
		"headshot_reaction": ["HitReaction_mixamo_vitruvian", "HitReaction", "headshot_reaction"],
		"stagger": ["HitReaction_mixamo_vitruvian", "stagger"]
	}
	for target_name in alias_map:
		if not lib.has_animation(target_name):
			for candidate in alias_map[target_name]:
				if lib.has_animation(candidate):
					lib.add_animation(target_name, lib.get_animation(candidate))
					break

func _setup_hitzones():
	for child in get_children():
		if child is HitZone:
			child.parent_entity = self

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
		save_mgr.add_coins(reward_on_kill)
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		mission_mgr.on_zombie_killed()
			
	await get_tree().create_timer(3.0).timeout
	queue_free()
