extends CanvasLayer

@onready var health_bar = $Control/HealthBar
@onready var ammo_label = $Control/AmmoLabel
@onready var objective_label = $Control/ObjectiveLabel
@onready var boss_health_bar = $Control/BossHealthBar
@onready var boss_name_label = $Control/BossHealthBar/BossName

func _ready():
	# Connect to relevant signals if any, or let scripts call these methods
	pass

func update_health(value: float):
	health_bar.value = value

func update_ammo(current: int, total: int):
	ammo_label.text = str(current) + " / " + str(total)

func update_objective(text: String):
	objective_label.text = text

func show_boss_health(name: String, max_hp: float):
	boss_health_bar.max_value = max_hp
	boss_health_bar.value = max_hp
	boss_name_label.text = name
	boss_health_bar.show()

func update_boss_health(value: float):
	boss_health_bar.value = value
	if value <= 0:
		boss_health_bar.hide()

func _on_reload_pressed():
	Input.action_press("reload")
	Input.action_release("reload")
