extends Control

@onready var master_slider = $Panel/VBoxContainer/AudioSettings/MasterSlider
@onready var quality_option = $Panel/VBoxContainer/GraphicsSettings/QualityOption

func _ready():
	# Sync UI with current settings
	master_slider.value = AudioManager.master_volume
	quality_option.selected = QualityManager.current_quality
	show()

func _on_master_slider_value_changed(value: float):
	AudioManager.set_master_volume(value)

func _on_quality_option_item_selected(index: int):
	QualityManager.apply_quality(index)

func _on_back_button_pressed():
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
