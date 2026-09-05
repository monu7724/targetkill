class_name ModalPanel
extends Control

signal modal_opened()
signal modal_closed()

@export var backdrop_color: Color = Color(0, 0, 0, 0.65)
@export var animate_duration: float = 0.2

var backdrop: ColorRect = null
var content_panel: Control = null

func _ready():
	mouse_filter = Control.MOUSE_FILTER_STOP
	process_mode = Node.PROCESS_MODE_ALWAYS

func open_modal():
	visible = true
	modulate.a = 0.0
	scale = Vector2(0.95, 0.95)
	pivot_offset = size / 2.0
	
	var tween = create_tween().set_parallel(true)
	tween.tween_property(self, "modulate:a", 1.0, animate_duration)
	tween.tween_property(self, "scale", Vector2.ONE, animate_duration).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	modal_opened.emit()

func close_modal():
	var tween = create_tween().set_parallel(true)
	tween.tween_property(self, "modulate:a", 0.0, animate_duration * 0.75)
	tween.tween_property(self, "scale", Vector2(0.95, 0.95), animate_duration * 0.75)
	await tween.finished
	visible = false
	modal_closed.emit()
