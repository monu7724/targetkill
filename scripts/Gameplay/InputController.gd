extends Node

signal move_input(vector: Vector2)
signal look_input(relative: Vector2)
signal fire_pressed()
signal fire_released()
signal reload_pressed()
signal switch_weapon_pressed()
signal pause_pressed()

var is_firing: bool = false
var virtual_move: Vector2 = Vector2.ZERO
var look_sensitivity: float = 1.0
var touch_deadzone: float = 4.0

var move_finger_index: int = -1
var look_finger_index: int = -1

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS

func set_virtual_movement(vec: Vector2):
	virtual_move = vec
	move_input.emit(virtual_move)

func feed_look_delta(relative: Vector2):
	if relative.length() < touch_deadzone:
		return
	look_input.emit(relative * look_sensitivity)

func start_fire():
	if not is_firing:
		is_firing = true
		fire_pressed.emit()

func stop_fire():
	if is_firing:
		is_firing = false
		fire_released.emit()

func trigger_reload():
	reload_pressed.emit()

func trigger_switch_weapon():
	switch_weapon_pressed.emit()

func trigger_pause():
	pause_pressed.emit()

func get_combined_movement() -> Vector2:
	var move = virtual_move
	
	if Input.is_action_pressed("move_forward"):
		move.y -= 1.0
	if Input.is_action_pressed("move_backward"):
		move.y += 1.0
	if Input.is_action_pressed("move_left"):
		move.x -= 1.0
	if Input.is_action_pressed("move_right"):
		move.x += 1.0
		
	if move.length() > 1.0:
		move = move.normalized()
		
	return move

func _unhandled_input(event):
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_R:
				trigger_reload()
			KEY_Q, KEY_E:
				trigger_switch_weapon()
			KEY_ESCAPE:
				trigger_pause()
			KEY_1, KEY_2, KEY_3:
				trigger_switch_weapon()
