extends CharacterBody3D

@onready var camera: Camera3D = $Camera3D
@onready var fps_arms: Node3D = $Camera3D/FPSArms
@onready var weapon_manager: Node3D = $Camera3D/WeaponManager
@onready var aim_raycast: RayCast3D = $Camera3D/RayCast3D
@onready var hud: CanvasLayer = $HUD
@onready var anim_player = get_node_or_null("AnimationPlayer")
@onready var sfx_footstep = get_node_or_null("SfxFootstep")

@export var sensitivity: float = 0.22
@export var min_pitch: float = -65.0
@export var max_pitch: float = 65.0

@export var move_speed: float = 4.8
@export var acceleration: float = 24.0
@export var deceleration: float = 32.0
@export var move_limit: float = 12.0
@export var sway_amount: float = 0.04
@export var bob_speed: float = 8.5
@export var bob_amount: float = 0.022
@export var breathing_speed: float = 1.8
@export var breathing_amount: float = 0.006

var virtual_move: Vector2 = Vector2.ZERO
var shake_intensity: float = 0.0
var shake_fade: float = 5.0
var time: float = 0.0
var step_timer: float = 0.0
var camera_kick: float = 0.0

var max_health: float = 100.0
var current_health: float = 100.0
var is_dead: bool = false
var is_firing: bool = false

var weapon_prefab: PackedScene = preload("res://scenes/weapons/Weapon.tscn")
var weapon_configs = [
	{"id": "pistol", "path": "res://resources/weapons/pistol.tres", "model": "res://assets/3d/weapons/pistol.glb"},
	{"id": "rifle", "path": "res://resources/weapons/rifle.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "shotgun", "path": "res://resources/weapons/shotgun.tres", "model": "res://assets/3d/weapons/shotgun.glb"}
]
var weapons: Array = []
var current_weapon_index: int = 0

func _ready():
	_init_character_models()
	_init_weapons()
	if not anim_player:
		anim_player = find_child("AnimationPlayer", true, false)
	if anim_player and anim_player.has_animation("idle"):
		anim_player.play("idle")
	await get_tree().process_frame
	if not is_inside_tree() or is_queued_for_deletion():
		return
	_update_hud()
	
	var save_mgr = get_node_or_null("/root/SaveManager")
	var mission_mgr = get_node_or_null("/root/MissionManager")
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.GAMEPLAY)
		
	if hud and is_instance_valid(hud):
		hud.update_health(current_health, max_health)
		if save_mgr and save_mgr.data.has("coins"):
			hud.update_coins(save_mgr.data.coins)
			
	if mission_mgr and mission_mgr.current_mission and hud and is_instance_valid(hud):
		hud.update_objective(mission_mgr.current_mission.display_name, "Eliminate " + str(mission_mgr.current_mission.target_count) + " Zombies")
		if not mission_mgr.mission_completed.is_connected(_on_mission_completed):
			mission_mgr.mission_completed.connect(_on_mission_completed)

func _extract_mesh_from_scene(packed_scene: PackedScene) -> Mesh:
	if not packed_scene: return null
	var inst = packed_scene.instantiate()
	var mesh_nodes = inst.find_children("*", "MeshInstance3D", true, false)
	var result_mesh: Mesh = null
	if not mesh_nodes.is_empty() and mesh_nodes[0].mesh:
		result_mesh = mesh_nodes[0].mesh
	inst.free()
	return result_mesh

func _init_character_models():
	if has_node("PlayerBody/MeshInstance3D"):
		var soldier_res = load("res://assets/3d/characters/player_soldier.glb")
		if soldier_res is PackedScene:
			var sm = _extract_mesh_from_scene(soldier_res)
			if sm:
				$PlayerBody/MeshInstance3D.mesh = sm
				$PlayerBody/MeshInstance3D.material_override = null

	if fps_arms and fps_arms.has_node("MeshInstance3D"):
		var arms_res = load("res://assets/3d/weapons/fps_arms.glb")
		if arms_res is PackedScene:
			var am = _extract_mesh_from_scene(arms_res)
			if am:
				fps_arms.get_node("MeshInstance3D").mesh = am
				fps_arms.get_node("MeshInstance3D").material_override = null

func _init_weapons():
	for child in weapon_manager.get_children():
		child.queue_free()
	weapons.clear()

	for cfg in weapon_configs:
		var w = weapon_prefab.instantiate()
		w.weapon_data = load(cfg.path)
		w.aim_raycast = aim_raycast
		weapon_manager.add_child(w)
		
		# Set 3D model on weapon
		if w.has_node("MeshInstance3D"):
			var model_res = load(cfg.model)
			if model_res is PackedScene:
				var wm = _extract_mesh_from_scene(model_res)
				if wm:
					w.get_node("MeshInstance3D").mesh = wm
					w.get_node("MeshInstance3D").material_override = null
			elif model_res is Mesh:
				w.get_node("MeshInstance3D").mesh = model_res
			
		w.ammo_changed.connect(func(_c, _m): _update_hud())
		weapons.append(w)

	current_weapon_index = 0
	_apply_active_weapon()

func _apply_active_weapon():
	for i in range(weapons.size()):
		var is_active = (i == current_weapon_index)
		weapons[i].visible = is_active
		if not is_active:
			if weapons[i].has_method("cancel_reload"):
				weapons[i].cancel_reload()
		else:
			weapons[i].apply_upgrades()
			if weapons[i].current_ammo > 0 and not weapons[i].is_reloading:
				weapons[i].can_shoot = true
	if fps_arms:
		fps_arms.position.y -= 0.035
	_update_hud()

func switch_weapon():
	if weapons.is_empty() or is_dead:
		return
	current_weapon_index = (current_weapon_index + 1) % weapons.size()
	_apply_active_weapon()

func switch_to_weapon(index: int):
	if index >= 0 and index < weapons.size() and not is_dead:
		current_weapon_index = index
		_apply_active_weapon()

func get_current_weapon():
	if current_weapon_index >= 0 and current_weapon_index < weapons.size():
		return weapons[current_weapon_index]
	return null

func set_virtual_movement(vec: Vector2):
	virtual_move = vec

func rotate_camera(rot_x: float, rot_y: float):
	if is_dead: return
	rotate_y(deg_to_rad(-rot_x * sensitivity))
	camera.rotate_x(deg_to_rad(rot_y * sensitivity))
	camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
	
	# Responsive weapon sway
	var sway = deg_to_rad(-rot_x * sensitivity * sway_amount)
	weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, sway, 0.15)
	if fps_arms:
		fps_arms.rotation.y = lerp(fps_arms.rotation.y, sway, 0.15)

func apply_kick(amount: float):
	camera_kick += amount
	camera.rotate_x(deg_to_rad(amount))
	camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))

func _input(event):
	if is_dead: return
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		rotate_camera(event.relative.x, event.relative.y)
	
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_1:
			switch_to_weapon(0)
		elif event.keycode == KEY_2:
			switch_to_weapon(1)
		elif event.keycode == KEY_3:
			switch_to_weapon(2)

func start_fire():
	is_firing = true
	_trigger_shoot()

func stop_fire():
	is_firing = false

func _trigger_shoot():
	if is_dead: return
	var weapon = get_current_weapon()
	if weapon and weapon.can_shoot and not weapon.is_reloading:
		weapon.shoot()
		var kick_factor = weapon.weapon_data.recoil if weapon.weapon_data else 1.0
		apply_shake(0.20 * kick_factor)
		apply_kick(-1.3 * kick_factor)
		_recoil_arms(kick_factor)
		_update_hud()

func _trigger_reload():
	if is_dead: return
	var weapon = get_current_weapon()
	if weapon and not weapon.is_reloading:
		weapon.reload()
		_reload_arms()
		_update_hud()

func _recoil_arms(factor: float = 1.0):
	if fps_arms:
		fps_arms.position.z += 0.04 * factor
		fps_arms.rotation.x += deg_to_rad(3.0 * factor)

func _reload_arms():
	if fps_arms:
		fps_arms.position.y -= 0.05

func _physics_process(delta):
	if is_dead: return
	time += delta
	
	# Auto fire for automatic weapons or held fire button
	if is_firing:
		var weapon = get_current_weapon()
		if weapon and weapon.can_shoot and not weapon.is_reloading:
			if weapon.weapon_data and weapon.weapon_data.is_automatic:
				_trigger_shoot()
	
	# Movement calculation combining input axes and virtual joystick
	var move_input = Vector3.ZERO
	if Input.is_action_pressed("move_forward"):
		move_input.z -= 1
	if Input.is_action_pressed("move_backward"):
		move_input.z += 1
	if Input.is_action_pressed("move_left"):
		move_input.x -= 1
	if Input.is_action_pressed("move_right"):
		move_input.x += 1
		
	move_input.x += virtual_move.x
	move_input.z += virtual_move.y
	
	var is_moving = move_input.length() > 0.05
	if is_moving:
		if move_input.length() > 1.0:
			move_input = move_input.normalized()
		var move_dir = (global_transform.basis * move_input)
		move_dir.y = 0.0
		var target_vel = move_dir * move_speed
		# Smooth acceleration
		velocity.x = move_toward(velocity.x, target_vel.x, acceleration * delta)
		velocity.z = move_toward(velocity.z, target_vel.z, acceleration * delta)
		
		# Footstep sound
		step_timer -= delta
		if step_timer <= 0.0:
			if sfx_footstep:
				sfx_footstep.play()
			step_timer = 0.42
			
		if anim_player and anim_player.current_animation != "walk":
			anim_player.play("walk")
	else:
		# Smooth deceleration
		velocity.x = move_toward(velocity.x, 0, deceleration * delta)
		velocity.z = move_toward(velocity.z, 0, deceleration * delta)
		if anim_player and anim_player.current_animation != "idle":
			anim_player.play("idle")
			
	move_and_slide()
	
	# Boundary Clamping
	global_position.x = clamp(global_position.x, -move_limit, move_limit)
	global_position.z = clamp(global_position.z, -move_limit, move_limit)
	
	# Subtle breathing & movement bobbing
	var vel_ratio = clamp(velocity.length() / move_speed, 0.0, 1.0)
	var breath = sin(time * breathing_speed) * breathing_amount
	var bob = sin(time * bob_speed) * bob_amount * (1.5 * vel_ratio if is_moving else 0.25)
	var target_bob_y = -0.18 + breath + bob
	
	weapon_manager.position.y = lerp(weapon_manager.position.y, target_bob_y, 0.12)
	weapon_manager.rotation.x = lerp(weapon_manager.rotation.x, 0.0, 5.0 * delta)
	weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, 0.0, 5.0 * delta)
	
	if fps_arms:
		fps_arms.position.y = lerp(fps_arms.position.y, target_bob_y, 0.12)
		fps_arms.position.z = lerp(fps_arms.position.z, -0.42, 5.0 * delta)
		fps_arms.rotation.x = lerp(fps_arms.rotation.x, 0.0, 5.0 * delta)
		fps_arms.rotation.y = lerp(fps_arms.rotation.y, 0.0, 5.0 * delta)
	
	# Camera shake recovery
	if shake_intensity > 0:
		camera.h_offset = randf_range(-shake_intensity, shake_intensity)
		camera.v_offset = randf_range(-shake_intensity, shake_intensity)
		shake_intensity = lerp(shake_intensity, 0.0, shake_fade * delta)
	else:
		camera.h_offset = 0
		camera.v_offset = 0

	# Smooth camera recoil recovery
	if abs(camera_kick) > 0.005:
		var recover = camera_kick * 12.0 * delta
		camera.rotate_x(deg_to_rad(-recover))
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
		camera_kick -= recover
	else:
		camera_kick = 0.0

func apply_shake(intensity: float):
	shake_intensity = max(shake_intensity, intensity)

func _update_hud():
	if not hud: return
	var weapon = get_current_weapon()
	if weapon and weapon.weapon_data:
		var next_name = ""
		if weapons.size() > 1:
			var next_w = weapons[(current_weapon_index + 1) % weapons.size()]
			if next_w and next_w.weapon_data:
				next_name = next_w.weapon_data.display_name
		hud.update_ammo(weapon.current_ammo, weapon.max_ammo, weapon.weapon_data.display_name, next_name)
	hud.update_health(current_health, max_health)
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and save_mgr.data.has("coins"):
		hud.update_coins(save_mgr.data.coins)

func take_damage(amount: float):
	if is_dead: return
	current_health = max(0.0, current_health - amount)
	apply_shake(0.4)
	_update_hud()
	
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.player_health_changed.emit(current_health, max_health)
	
	if current_health <= 0:
		is_dead = true
		if anim_player and anim_player.has_animation("death"):
			anim_player.play("death")
		var audio_mgr = get_node_or_null("/root/AudioManager")
		if audio_mgr:
			audio_mgr.play_defeat()
		var mission_mgr = get_node_or_null("/root/MissionManager")
		if mission_mgr and mission_mgr.current_mission:
			mission_mgr.finish_mission(false)
		else:
			if hud:
				hud.update_objective("OUTCOME", "You were overrun")

func _on_mission_completed(_m):
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.play_victory()
