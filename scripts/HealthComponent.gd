extends Node
class_name HealthComponent

signal health_changed(current_health)
signal died

@export var max_health: float = 100.0
var current_health: float

func _ready():
	current_health = max_health

func take_damage(amount: float):
	current_health -= amount
	health_changed.emit(current_health)
	
	if current_health <= 0:
		died.emit()
