extends Node3D

@onready var camera = $Camera3D
@onready var weapon_manager = $Camera3D/WeaponManager
@onready var hud = $HUD

@export var sensitivity: float = 0.2
@export var min_pitch: float = -60.0
@export var max_pitch: float = 60.0

@export var sway_amount: float = 0.05
@export var bob_amount: float = 0.02
@export var bob_speed: float = 8.0

var mouse_captured: bool = false
var shake_intensity: float = 0.0
var shake_fade: float = 5.0
var time: float = 0.0

func _input(event):
	var rot_y = 0.0
	var rot_x = 0.0
	
	if event is InputEventMouseMotion:
		rot_y = -event.relative.x * sensitivity
		rot_x = -event.relative.y * sensitivity
		
	if event is InputEventScreenDrag:
		rot_y = -event.relative.x * sensitivity
		rot_x = -event.relative.y * sensitivity
		
	if rot_y != 0.0 or rot_x != 0.0:
		rotate_y(deg_to_rad(rot_y))
		camera.rotate_x(deg_to_rad(rot_x))
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
		
		# Apply sway to weapon manager
		weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, deg_to_rad(rot_y * sway_amount), 0.1)
		weapon_manager.rotation.x = lerp(weapon_manager.rotation.x, deg_to_rad(rot_x * sway_amount), 0.1)

func _process(delta):
	time += delta
	if Input.is_action_just_pressed("shoot"):
		_trigger_shoot()
	
	if Input.is_action_just_pressed("reload"):
		_trigger_reload()
	
	# Reset weapon sway
	weapon_manager.rotation.x = lerp(weapon_manager.rotation.x, 0.0, 0.1)
	weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, 0.0, 0.1)
	
	# Apply camera shake
	if shake_intensity > 0:
		camera.h_offset = randf_range(-shake_intensity, shake_intensity)
		camera.v_offset = randf_range(-shake_intensity, shake_intensity)
		shake_intensity = lerp(shake_intensity, 0.0, shake_fade * delta)
	else:
		camera.h_offset = 0
		camera.v_offset = 0
		
	# Simple weapon bobbing (simulated since stationary)
	var bob = sin(time * bob_speed) * bob_amount
	weapon_manager.position.y = lerp(weapon_manager.position.y, -0.3 + bob, 0.1)

func _trigger_shoot():
	if weapon_manager.get_child_count() > 0:
		var weapon = weapon_manager.get_child(0)
		weapon.shoot()
		apply_shake(0.2)
		_update_hud()

func _trigger_reload():
	if weapon_manager.get_child_count() > 0:
		var weapon = weapon_manager.get_child(0)
		weapon.reload()
		_update_hud()

func _update_hud():
	if hud and weapon_manager.get_child_count() > 0:
		var weapon = weapon_manager.get_child(0)
		hud.update_ammo(weapon.current_ammo, weapon.max_ammo)

func apply_shake(intensity: float):
	shake_intensity = intensity

func _ready():
	# Update HUD initially
	await get_tree().process_frame
	_update_hud()
	if MissionManager.current_mission:
		hud.update_objective(MissionManager.current_mission.display_name)
