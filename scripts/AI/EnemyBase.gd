extends CharacterBody3D

class_name EnemyBase

enum AIState { IDLE, SPAWN, APPROACH, ATTACK_PREPARE, ATTACK, HIT, STAGGER, DEATH }

var ai_state: int = AIState.IDLE
var health: float = 50.0

func _ready():
    pass

func take_damage(amount: float):
    health = max(0.0, health - amount)
    if health <= 0:
        ai_state = AIState.DEATH
    elif amount > 20.0:
        ai_state = AIState.STAGGER
