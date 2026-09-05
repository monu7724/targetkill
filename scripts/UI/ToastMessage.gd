class_name ToastMessage
extends Control

@export var duration: float = 2.5
var label: Label = null
var panel: PanelContainer = null

func _ready():
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	process_mode = Node.PROCESS_MODE_ALWAYS

func show_toast(text: String):
	if not label:
		panel = PanelContainer.new()
		panel.set_anchors_preset(Control.PRESET_TOP_WIDE)
		panel.offset_top = 20
		panel.offset_left = 200
		panel.offset_right = -200
		panel.offset_bottom = 70
		add_child(panel)
		
		label = Label.new()
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		label.add_theme_font_size_override("font_size", 18)
		label.add_theme_color_override("font_color", Color(1.0, 0.85, 0.3))
		panel.add_child(label)
		
	label.text = text
	visible = true
	modulate.a = 0.0
	position.y = -40
	
	var tween = create_tween()
	tween.tween_property(self, "modulate:a", 1.0, 0.25)
	tween.parallel().tween_property(self, "position:y", 0.0, 0.25).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tween.tween_interval(duration)
	tween.tween_property(self, "modulate:a", 0.0, 0.3)
	await tween.finished
	visible = false
