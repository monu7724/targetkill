class_name TacticalButton
extends Button

@export var click_sound: String = "ui_click"
@export var press_scale: float = 0.94
@export var tween_duration: float = 0.12

func _ready():
	pivot_offset = size / 2.0
	resized.connect(func(): pivot_offset = size / 2.0)
	button_down.connect(_on_button_down)
	button_up.connect(_on_button_up)

func _on_button_down():
	var tween = create_tween()
	tween.tween_property(self, "scale", Vector2(press_scale, press_scale), tween_duration).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr and audio_mgr.has_method("play_ui_click"):
		audio_mgr.play_ui_click()

func _on_button_up():
	var tween = create_tween()
	tween.tween_property(self, "scale", Vector2.ONE, tween_duration).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
