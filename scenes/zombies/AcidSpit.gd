extends Area3D

var speed = 12.0
var damage = 8.0
var direction = Vector3.FORWARD
var life_time = 3.0

func _ready():
    body_entered.connect(_on_body_entered)

func _process(delta):
    global_position += direction * speed * delta
    life_time -= delta
    if life_time <= 0:
        queue_free()

func _on_body_entered(body):
    if body.is_in_group("player") and body.has_method("take_damage"):
        body.take_damage(damage)
    queue_free()
