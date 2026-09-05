class_name CameraController
extends Node

@export var camera: Camera3D
@export var fps_arms: Node3D
@export var weapon_manager: Node3D

@export var sensitivity: float = 0.22
@export var min_pitch: float = -65.0
@export var max_pitch: float = 65.0

# Sway & Bob Parameters
@export var sway_amount: float = 0.04
@export var bob_speed: float = 8.5
@export var bob_amount: float = 0.022
@export var breathing_speed: float = 1.8
@export var breathing_amount: float = 0.006

var camera_kick: float = 0.0
var shake_intensity: float = 0.0
var shake_fade: float = 5.0
var time: float = 0.0

func _ready():
	if not camera:
		camera = get_parent().find_child("Camera3D", true, false)

func rotate_camera(rot_x: float, rot_y: float, parent_body: Node3D):
	if not parent_body or not camera: return
	
	# Horizontal rotation applied to body (yaw)
	parent_body.rotate_y(deg_to_rad(-rot_x * sensitivity))
	
	# Vertical rotation applied to camera (pitch)
	camera.rotate_x(deg_to_rad(rot_y * sensitivity))
	camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
	
	# Weapon sway
	var sway = deg_to_rad(-rot_x * sensitivity * sway_amount)
	if weapon_manager:
		weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, sway, 0.15)
	if fps_arms:
		fps_arms.rotation.y = lerp(fps_arms.rotation.y, sway, 0.15)

func apply_kick(amount: float):
	camera_kick += amount
	if camera:
		camera.rotate_x(deg_to_rad(amount))
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))

func apply_shake(intensity: float):
	shake_intensity = max(shake_intensity, intensity)

func update_bob_and_sway(delta: float, is_moving: bool, move_speed_ratio: float):
	time += delta
	if not camera: return
	
	# Subtle breathing sway
	var breath_y = sin(time * breathing_speed) * breathing_amount
	var breath_x = cos(time * breathing_speed * 0.5) * (breathing_amount * 0.5)
	
	# Movement bobbing
	var bob_factor = 1.5 * move_speed_ratio if is_moving else 0.2
	var bob_y = sin(time * bob_speed) * bob_amount * bob_factor
	var bob_x = cos(time * bob_speed * 0.5) * (bob_amount * 0.6) * (1.0 if is_moving else 0.0)
	
	var target_y = -0.18 + breath_y + bob_y
	var target_x = breath_x + bob_x
	
	if weapon_manager:
		weapon_manager.position.y = lerp(weapon_manager.position.y, target_y, 0.12)
		weapon_manager.position.x = lerp(weapon_manager.position.x, target_x, 0.12)
		weapon_manager.rotation.x = lerp(weapon_manager.rotation.x, 0.0, 5.0 * delta)
		weapon_manager.rotation.y = lerp(weapon_manager.rotation.y, 0.0, 5.0 * delta)
		
	if fps_arms:
		fps_arms.position.y = lerp(fps_arms.position.y, target_y, 0.12)
		fps_arms.position.x = lerp(fps_arms.position.x, target_x, 0.12)
		fps_arms.position.z = lerp(fps_arms.position.z, -0.42, 5.0 * delta)
		fps_arms.rotation.x = lerp(fps_arms.rotation.x, 0.0, 5.0 * delta)
		fps_arms.rotation.y = lerp(fps_arms.rotation.y, 0.0, 5.0 * delta)
		
	# Camera shake
	if shake_intensity > 0.001:
		camera.h_offset = randf_range(-shake_intensity, shake_intensity)
		camera.v_offset = randf_range(-shake_intensity, shake_intensity)
		shake_intensity = lerp(shake_intensity, 0.0, shake_fade * delta)
	else:
		camera.h_offset = 0.0
		camera.v_offset = 0.0
		shake_intensity = 0.0

	# Smooth recoil recovery
	if abs(camera_kick) > 0.005:
		var recover = camera_kick * 12.0 * delta
		camera.rotate_x(deg_to_rad(-recover))
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(min_pitch), deg_to_rad(max_pitch))
		camera_kick -= recover
	else:
		camera_kick = 0.0
