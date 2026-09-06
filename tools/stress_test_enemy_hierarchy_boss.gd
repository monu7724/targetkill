extends SceneTree

var received_boss_spawned = false
var spawned_boss_name = ""
var spawned_boss_max_hp = 0.0

var received_boss_hp_change = false
var last_boss_hp = 0.0
var last_boss_max_hp = 0.0

var received_enemy_killed = false
var killed_enemy_type = ""

func _init():
	print("==================================================")
	print("  STRESS TEST: ENEMY HIERARCHY & BOSS SIGNALS    ")
	print("==================================================")
	await process_frame
	
	var event_bus = root.get_node_or_null("EventBus")
	assert(event_bus != null, "EventBus autoload must exist")
	
	event_bus.boss_spawned.connect(_on_boss_spawned)
	event_bus.boss_health_changed.connect(_on_boss_health_changed)
	event_bus.enemy_killed.connect(_on_enemy_killed)
	
	var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
	assert(zombie_scene != null, "Zombie.tscn must load")
	
	# PART 1: Stress test all 8 enemy variant types
	print("\n--- PART 1: VERIFYING ALL 8 ARCHETYPES IN ZOMBIE.TSCN ---")
	var archetypes = [
		{"type": "normal", "hp": 50.0, "speed": 1.4, "range": 1.7},
		{"type": "fast", "hp": 30.0, "speed": 2.8, "range": 1.7},
		{"type": "heavy", "hp": 160.0, "speed": 0.8, "range": 2.2},
		{"type": "special", "hp": 40.0, "speed": 1.2, "range": 14.0},
		{"type": "dog", "hp": 50.0, "speed": 4.5, "range": 2.0},
		{"type": "rat", "hp": 15.0, "speed": 3.8, "range": 1.2},
		{"type": "bat", "hp": 12.0, "speed": 3.6, "range": 1.5, "fly_height": 2.2},
		{"type": "boss", "hp": 500.0, "speed": 1.1, "range": 2.5}
	]
	
	for arch in archetypes:
		var z = zombie_scene.instantiate()
		z.archetype = arch["type"]
		root.add_child(z)
		await process_frame
		
		assert(z.health_component != null, "HealthComponent missing on %s" % arch["type"])
		assert(z.health_component.max_health == arch["hp"], "HP mismatch on %s" % arch["type"])
		assert(z.move_speed == arch["speed"], "Speed mismatch on %s" % arch["type"])
		assert(z.attack_range == arch["range"], "Range mismatch on %s" % arch["type"])
		if arch.has("fly_height"):
			assert(z.fly_height == arch["fly_height"], "Fly height mismatch on %s" % arch["type"])
			
		# Damage test
		z.take_damage(5.0)
		assert(z.health_component.current_health == arch["hp"] - 5.0, "Damage failure on %s" % arch["type"])
		
		print("[PASS] Variant '%s' validated: HP=%.1f, Speed=%.1f, Range=%.1f" % [
			arch["type"], z.health_component.max_health, z.move_speed, z.attack_range
		])
		z.queue_free()
		await process_frame
		
	# PART 2: Dedicated InfectedDog.tscn verification
	print("\n--- PART 2: DEDICATED INFECTEDDOG.TSCN VERIFICATION ---")
	var dog_scene = load("res://scenes/zombies/InfectedDog.tscn")
	assert(dog_scene != null, "InfectedDog.tscn must load")
	var dog = dog_scene.instantiate()
	root.add_child(dog)
	await process_frame
	
	assert(dog is EnemyBase, "InfectedDog must inherit from EnemyBase")
	assert(dog.archetype == "dog", "InfectedDog archetype must be 'dog'")
	assert(dog.health_component.max_health == 50.0, "Dog HP must be 50.0")
	assert(dog.move_speed == 4.5, "Dog move_speed must be 4.5")
	
	# Verify HitZones
	var head_zone = dog.get_node_or_null("HeadHitZone")
	var body_zone = dog.get_node_or_null("BodyHitZone")
	assert(head_zone != null, "Dog must have HeadHitZone")
	assert(body_zone != null, "Dog must have BodyHitZone")
	assert(head_zone.damage_multiplier == 2.5, "Dog head zone multiplier must be 2.5")
	assert(body_zone.damage_multiplier == 1.0, "Dog body zone multiplier must be 1.0")
	
	print("[PASS] Dedicated InfectedDog.tscn verified with Head(2.5x) and Body(1.0x) HitZones!")
	dog.queue_free()
	await process_frame

	# PART 3: Dedicated BossZombie.tscn Signals & Enrage Stress Test
	print("\n--- PART 3: DEDICATED BOSSZOMBIE.TSCN SIGNALS & ENRAGE ---")
	received_boss_spawned = false
	received_boss_hp_change = false
	
	var boss_scene = load("res://scenes/zombies/BossZombie.tscn")
	assert(boss_scene != null, "BossZombie.tscn must load")
	var boss = boss_scene.instantiate()
	root.add_child(boss)
	await process_frame
	
	assert(received_boss_spawned, "EventBus.boss_spawned MUST be emitted when BossZombie readies")
	assert(spawned_boss_name == "THE ALPHA MUTANT", "Boss name must be 'THE ALPHA MUTANT'")
	assert(spawned_boss_max_hp == 500.0, "Boss max HP must be 500.0")
	print("[PASS] boss_spawned signal caught: Name='%s', MaxHP=%.1f" % [spawned_boss_name, spawned_boss_max_hp])
	
	# Test HP reduction & boss_health_changed signal
	received_boss_hp_change = false
	boss.take_damage(100.0)
	assert(received_boss_hp_change, "EventBus.boss_health_changed MUST be emitted on boss damage")
	assert(last_boss_hp == 400.0, "Boss HP should be 400.0 after 100 dmg, got %.1f" % last_boss_hp)
	assert(last_boss_max_hp == 500.0, "Boss max HP in signal should be 500.0")
	print("[PASS] boss_health_changed signal caught: Current=%.1f, Max=%.1f" % [last_boss_hp, last_boss_max_hp])
	
	# Test enrage threshold at 50% HP (250 HP)
	var initial_boss_speed = boss.move_speed
	boss.take_damage(160.0) # Down to 240 HP (<= 50%)
	boss._physics_process(0.016)
	assert(boss.has_enraged == true, "Boss must enter enrage state at <= 50% HP")
	assert(boss.move_speed > initial_boss_speed, "Boss move_speed must increase when enraged (was %.1f, now %.1f)" % [initial_boss_speed, boss.move_speed])
	print("[PASS] Boss enrage triggered at %.1f HP: Speed escalated from %.1f -> %.1f!" % [
		boss.health_component.current_health, initial_boss_speed, boss.move_speed
	])
	
	# Test lethal damage and death signal
	received_enemy_killed = false
	boss.take_damage(300.0)
	await process_frame
	assert(boss.is_dead == true, "Boss must be dead after lethal damage")
	assert(received_enemy_killed and killed_enemy_type == "boss", "enemy_killed('boss') signal must be emitted")
	assert(last_boss_hp == 0.0, "boss_health_changed should report 0.0 HP on death")
	print("[PASS] Boss death sequence, enemy_killed('boss'), and 0.0 HP signal verified!")
	
	boss.queue_free()
	await process_frame
	
	print("\n==================================================")
	print("  ENEMY HIERARCHY & BOSS SIGNALS STRESS PASSED!   ")
	print("==================================================")
	quit(0)

func _on_boss_spawned(b_name: String, max_hp: float):
	received_boss_spawned = true
	spawned_boss_name = b_name
	spawned_boss_max_hp = max_hp

func _on_boss_health_changed(cur_hp: float, max_hp: float):
	received_boss_hp_change = true
	last_boss_hp = cur_hp
	last_boss_max_hp = max_hp

func _on_enemy_killed(archetype: String, _headshot: bool, _pos: Vector3):
	received_enemy_killed = true
	killed_enemy_type = archetype
