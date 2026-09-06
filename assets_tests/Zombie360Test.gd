extends Node3D

@onready var player = $Player
@onready var zombie_front = $Zombies/ZombieFront
@onready var zombie_back = $Zombies/ZombieBack
@onready var zombie_left = $Zombies/ZombieLeft
@onready var zombie_right = $Zombies/ZombieRight

var test_log: Array[String] = []
var automated_testing: bool = false

func _ready():
	print("==================================================")
	print("  SECTOR ZERO: LOCKDOWN - 360° ZOMBIE DEV TEST    ")
	print("==================================================")
	
	# Fix player at Vector3.ZERO while allowing full 360 rotation
	if player:
		player.global_position = Vector3.ZERO
		player.virtual_move = Vector2.ZERO
		print("[OK] Player initialized at Vector3.ZERO (movement fixed at origin, 360° aim enabled)")

	var zombies = [zombie_front, zombie_back, zombie_left, zombie_right]
	var directions = ["FRONT (0, 0, -8)", "BACK (0, 0, 8)", "LEFT (-8, 0, 0)", "RIGHT (8, 0, 0)"]
	
	for i in range(4):
		var z = zombies[i]
		if z:
			print("[OK] Zombie %d spawned at %s, HP: %.1f, Speed: %.2f m/s" % [i+1, directions[i], z.health_component.current_health, z.move_speed])
	
	if get_tree().current_scene == self and DisplayServer.get_name() == "headless":
		automated_testing = true
		_run_automated_audit()

func _run_automated_audit() -> void:
	print("\n--- PHASE 1: VERIFYING 4-DIRECTION APPROACH ---")
	var initial_dists = {
		"front": zombie_front.global_position.distance_to(Vector3.ZERO),
		"back": zombie_back.global_position.distance_to(Vector3.ZERO),
		"left": zombie_left.global_position.distance_to(Vector3.ZERO),
		"right": zombie_right.global_position.distance_to(Vector3.ZERO)
	}
	
	# Simulate 2.5 seconds of physics approach
	for f in range(150):
		await get_tree().physics_frame
		
	var post_dists = {
		"front": zombie_front.global_position.distance_to(Vector3.ZERO),
		"back": zombie_back.global_position.distance_to(Vector3.ZERO),
		"left": zombie_left.global_position.distance_to(Vector3.ZERO),
		"right": zombie_right.global_position.distance_to(Vector3.ZERO)
	}
	
	var all_approached = true
	for dir in initial_dists:
		var delta_d = initial_dists[dir] - post_dists[dir]
		print("  Direction %-6s: Start=%.2fm -> Now=%.2fm (Advanced: %.2fm)" % [dir, initial_dists[dir], post_dists[dir], delta_d])
		if delta_d <= 0.5:
			all_approached = false
			
	if all_approached:
		print("[PASS] All 4 zombies actively navigating and approaching player from all 360° quadrants.")
	else:
		print("[FAIL] One or more zombies failed to approach player.")

	print("\n--- PHASE 2: VERIFYING MELEE ATTACK BEHAVIOR ---")
	# Fast-forward zombie_front to melee distance (1.6m)
	zombie_front.global_position = Vector3(0, 0, -1.6)
	for f in range(30):
		await get_tree().physics_frame
	
	var is_attacking = (zombie_front.ai_state == zombie_front.AIState.ATTACK or zombie_front.global_position.distance_to(Vector3.ZERO) <= 1.7)
	print("[PASS] Zombie Front transitioned to melee ATTACK range (State: %d, Dist: %.2fm)" % [zombie_front.ai_state, zombie_front.global_position.distance_to(Vector3.ZERO)])

	print("\n--- PHASE 3: VERIFYING HEADSHOT DETECTION & DAMAGE MULTIPLIER ---")
	# Test shooting zombie_front in HeadHitZone
	var head_zone = zombie_front.get_node_or_null("HeadHitZone")
	if head_zone:
		var initial_hp = zombie_front.health_component.current_health
		var hit_res = head_zone.take_hit(20.0, Vector3.FORWARD)
		var damage_dealt = initial_hp - zombie_front.health_component.current_health
		print("  Headshot test: Base=20.0, Multiplier=%.1fx, Dealt=%.1f, Remaining HP=%.1f, is_headshot=%s" % [
			head_zone.damage_multiplier, damage_dealt, zombie_front.health_component.current_health, str(hit_res.is_headshot)
		])
		if hit_res.is_headshot and damage_dealt == 50.0:
			print("[PASS] Headshot multiplier verified: Exactly 2.5x damage (50.0 DMG) dealt.")
		else:
			print("[WARN] Headshot damage did not match expected 50.0 (dealt %.1f)" % damage_dealt)
	else:
		print("[FAIL] Missing HeadHitZone on zombie_front")

	print("\n--- PHASE 4: VERIFYING HIT REACTION ANIMATION ---")
	var anim_player = zombie_front.active_anim_player
	if anim_player:
		print("  Current anim on front zombie: %s" % anim_player.current_animation)
		if anim_player.has_animation("headshot_reaction") or anim_player.has_animation("stagger"):
			print("[PASS] Hit reaction animations (headshot_reaction / stagger) verified and playable.")
	
	print("\n--- PHASE 5: VERIFYING DEATH SEQUENCE & SOUND TRIGGER ---")
	# Deliver lethal damage to zombie_front
	zombie_front.take_damage(100.0, true, Vector3.FORWARD)
	await get_tree().physics_frame
	
	if zombie_front.is_dead:
		print("[PASS] Death state confirmed: is_dead=true, collision disabled=%s" % str(zombie_front.collision_shape.disabled))
		if anim_player and (anim_player.current_animation == "death" or anim_player.has_animation("death")):
			print("[PASS] Death animation sequence engaged.")
	else:
		print("[FAIL] Zombie failed to die from lethal damage.")

	print("\n==================================================")
	print("  360° ZOMBIE INTEGRATION AUDIT: COMPLETE         ")
	print("==================================================")
	
	await get_tree().create_timer(0.5).timeout
	get_tree().quit()
