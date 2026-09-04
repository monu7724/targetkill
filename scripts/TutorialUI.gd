extends Control

@onready var label = $Panel/Label
@onready var next_btn = $Panel/NextButton

var steps = [
	"Welcome to Sector Zero. Drag anywhere to aim.",
	"Tap the screen to shoot. Aim for the head for extra damage.",
	"Your ammo is limited. Tap RELOAD when empty.",
	"Zombies are approaching. Clear the sector to earn coins.",
	"Use coins in the UPGRADE HUB to improve your weapons."
]
var current_step = 0

func _ready():
	if not SaveManager.data.is_first_launch:
		queue_free()
		return
	update_step()

func _on_next_button_pressed():
	current_step += 1
	if current_step >= steps.size():
		SaveManager.data.is_first_launch = false
		SaveManager.save_game()
		queue_free()
	else:
		update_step()

func update_step():
	label.text = steps[current_step]
