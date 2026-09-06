extends Node

var results = {}
var test_player: CharacterBody3D = null

func record_test(name: String, passed: bool, detail: String = ""):
	results[name] = {"passed": passed, "detail": detail}
	var tag = "[PASS]" if passed else "[FAIL]"
	print(tag + " " + name + (" - " + detail if detail != "" else ""))

func _ready():
	print("\n==================================================")
	print("INFECTED DOG TEST SUITE")
	print("==================================================\n")
	await _run_tests()
	_print_summary()
	await get_tree().create_timer(0.5).timeout
	get_tree().quit()

func _run_tests():
	await _test_dog_loading()
	await _test_dog_approach()
	await _test_dog_attack()
	await _test_dog_damage()
	await _test_dog_headshot()
	await _test_dog_death()
	await _test_dog_multi_direction_spawn()

func _test_dog_loading():
	print("--- DOG LOADING ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	add_child(dog)
	await get_tree().process_frame
	
	var model_ok = dog.mesh_instance != null or dog.model_instance != null
	record_test("Dog model loads", model_ok, "MeshInstance: %s, ModelInstance: %s" % [dog.mesh_instance != null, dog.model_instance != null])
	
	var hp_ok = dog.health_component.max_health == 50.0
	record_test("Dog HP correct", hp_ok, "HP: %f (expected 50)" % dog.health_component.max_health)
	
	var speed_ok = dog.move_speed == 4.5
	record_test("Dog speed correct", speed_ok, "Speed: %f (expected 4.5)" % dog.move_speed)
	
	var range_ok = dog.attack_range == 2.0
	record_test("Dog attack range", range_ok, "Range: %f (expected 2.0)" % dog.attack_range)
	
	var damage_ok = dog.attack_damage == 12.0
	record_test("Dog attack damage", damage_ok, "Damage: %f (expected 12.0)" % dog.attack_damage)
	
	var interval_ok = dog.attack_interval == 1.8
	record_test("Dog attack cooldown", interval_ok, "Interval: %f (expected 1.8)" % dog.attack_interval)
	
	dog.queue_free()
	await get_tree().process_frame

func _test_dog_approach():
	print("\n--- DOG APPROACH ---")
	# Create a fake player target
	var player_node = CharacterBody3D.new()
	player_node.add_to_group("player")
	player_node.global_position = Vector3(0, 0, 0)
	add_child(player_node)
	test_player = player_node
	
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	dog.global_position = Vector3(0, 0, 15)
	add_child(dog)
	await get_tree().process_frame
	await get_tree().process_frame
	
	var initial_dist = dog.global_position.distance_to(player_node.global_position)
	
	# Simulate several physics frames
	for i in range(10):
		dog._physics_process(0.016)
		await get_tree().process_frame
	
	var new_dist = dog.global_position.distance_to(player_node.global_position)
	var approached = new_dist < initial_dist
	record_test("Dog approaches player", approached, "Start: %f, After: %f" % [initial_dist, new_dist])
	
	var velocity_ok = dog.velocity.length() > 0.0
	record_test("Dog has velocity", velocity_ok, "Velocity: %s" % dog.velocity)
	
	dog.queue_free()
	player_node.queue_free()
	test_player = null
	await get_tree().process_frame

func _test_dog_attack():
	print("\n--- DOG ATTACK ---")
	var player_node = CharacterBody3D.new()
	player_node.add_to_group("player")
	player_node.global_position = Vector3(0, 0, 0)
	add_child(player_node)
	
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	dog.global_position = Vector3(0, 0, 1.5) # Within attack range
	add_child(dog)
	await get_tree().process_frame
	await get_tree().process_frame
	
	# Dog should enter attack state when within range
	dog.attack_timer = 0 # Reset timer so it can attack
	dog._physics_process(0.016)
	
	var in_attack = dog.ai_state == dog.AIState.ATTACK
	record_test("Dog enters attack state", in_attack, "AI State: %s (expected ATTACK)" % dog.AIState.keys()[dog.ai_state])
	
	dog.queue_free()
	player_node.queue_free()
	await get_tree().process_frame

func _test_dog_damage():
	print("\n--- DOG DAMAGE ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	add_child(dog)
	await get_tree().process_frame
	
	var init_hp = dog.health_component.current_health
	dog.take_damage(26.0)
	var took_damage = dog.health_component.current_health < init_hp
	record_test("Dog takes damage", took_damage, "HP: %f -> %f" % [init_hp, dog.health_component.current_health])
	
	# Hit reaction
	var hit_reacted = dog.ai_state == dog.AIState.STAGGER
	record_test("Dog hit reaction", hit_reacted, "State after 26 dmg: %s" % dog.AIState.keys()[dog.ai_state])
	
	dog.queue_free()
	await get_tree().process_frame

func _test_dog_headshot():
	print("\n--- DOG HEADSHOT ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	add_child(dog)
	await get_tree().process_frame
	
	var init_hp = dog.health_component.current_health
	dog.take_damage(20.0, true) # headshot
	var remaining = dog.health_component.current_health
	# Headshot just passes the flag, damage is already multiplied by hitzone
	var headshot_ok = remaining < init_hp
	record_test("Dog headshot damage", headshot_ok, "HP: %f -> %f (20 dmg headshot)" % [init_hp, remaining])
	
	dog.queue_free()
	await get_tree().process_frame

func _test_dog_death():
	print("\n--- DOG DEATH ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	var dog = zombie_scene.instantiate()
	dog.archetype = "dog"
	add_child(dog)
	await get_tree().process_frame
	
	dog.take_damage(100.0)
	await get_tree().create_timer(0.3).timeout
	
	var dead = dog.is_dead
	record_test("Dog death", dead, "is_dead: %s" % dead)
	
	var collision_disabled = dog.collision_shape.disabled
	record_test("Dog collision disabled on death", collision_disabled, "CollisionShape disabled: %s" % collision_disabled)
	
	dog.queue_free()
	await get_tree().process_frame

func _test_dog_multi_direction_spawn():
	print("\n--- DOG MULTI-DIRECTION SPAWN ---")
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	
	var directions = {
		"FRONT": Vector3(0, 0, 15),
		"BACK": Vector3(0, 0, -15),
		"LEFT": Vector3(-15, 0, 0),
		"RIGHT": Vector3(15, 0, 0),
	}
	
	var all_spawned = true
	for dir_name in directions:
		var dog = zombie_scene.instantiate()
		dog.archetype = "dog"
		dog.global_position = directions[dir_name]
		add_child(dog)
		await get_tree().process_frame
		
		var spawned_ok = dog.is_inside_tree() and not dog.is_dead
		if not spawned_ok:
			all_spawned = false
		dog.queue_free()
	
	record_test("Four-direction spawning", all_spawned, "FRONT/BACK/LEFT/RIGHT all spawned")
	await get_tree().process_frame

func _print_summary():
	print("\n==================================================")
	print("INFECTED DOG TEST SUMMARY")
	print("==================================================")
	var pass_count = 0
	var total = results.size()
	for k in results.keys():
		var p = results[k].passed
		if p: pass_count += 1
		print("%-35s : %s" % [k, "PASS" if p else "FAIL"])
	print("==================================================")
	print("TOTAL: %d / %d PASSED" % [pass_count, total])
	print("==================================================")
