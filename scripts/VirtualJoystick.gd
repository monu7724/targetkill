extends Control
class_name VirtualJoystick

signal movement_changed(vector: Vector2)

@export var max_radius: float = 55.0
var touch_index: int = -1
var joystick_center: Vector2 = Vector2.ZERO
var knob_position: Vector2 = Vector2.ZERO
var output_vector: Vector2 = Vector2.ZERO
var is_active: bool = false

func _ready():
	custom_minimum_size = Vector2(150, 150)
	joystick_center = Vector2(75, 75)
	knob_position = joystick_center
	queue_redraw()

func _notification(what):
	if what == NOTIFICATION_RESIZED:
		joystick_center = size / 2.0
		if not is_active:
			knob_position = joystick_center
		queue_redraw()

func _draw():
	# Outer ring
	draw_circle(joystick_center, max_radius + 15.0, Color(0.1, 0.1, 0.12, 0.5))
	draw_arc(joystick_center, max_radius + 15.0, 0, TAU, 32, Color(0.3, 0.7, 1.0, 0.6), 2.0)
	# Center deadzone ring
	draw_arc(joystick_center, 12.0, 0, TAU, 16, Color(1, 1, 1, 0.15), 1.0)
	# Inner knob
	draw_circle(knob_position, 26.0, Color(0.3, 0.7, 1.0, 0.75))
	draw_arc(knob_position, 26.0, 0, TAU, 24, Color(1, 1, 1, 0.9), 2.0)

func _gui_input(event: InputEvent):
	if event is InputEventScreenTouch:
		if event.pressed and touch_index == -1:
			touch_index = event.index
			is_active = true
			_update_joystick(event.position)
			accept_event()
		elif (not event.pressed or event.is_canceled()) and event.index == touch_index:
			_reset_joystick()
			accept_event()
			
	elif event is InputEventScreenDrag and event.index == touch_index:
		_update_joystick(event.position)
		accept_event()
		
	elif event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				is_active = true
				_update_joystick(event.position)
			else:
				_reset_joystick()
				
	elif event is InputEventMouseMotion and is_active:
		_update_joystick(event.position)

func _input(event: InputEvent):
	if touch_index != -1:
		if event is InputEventScreenDrag and event.index == touch_index:
			var local_pos = get_global_transform().affine_inverse() * event.position
			_update_joystick(local_pos)
		elif event is InputEventScreenTouch and (not event.pressed or event.is_canceled()) and event.index == touch_index:
			_reset_joystick()

func _update_joystick(pos: Vector2):
	var diff = pos - joystick_center
	if diff.length() > max_radius:
		diff = diff.normalized() * max_radius
	knob_position = joystick_center + diff
	output_vector = Vector2(diff.x / max_radius, diff.y / max_radius)
	movement_changed.emit(output_vector)
	queue_redraw()

func _reset_joystick():
	touch_index = -1
	is_active = false
	knob_position = joystick_center
	output_vector = Vector2.ZERO
	movement_changed.emit(Vector2.ZERO)
	queue_redraw()
