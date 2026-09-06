extends RigidBody3D

var timer = 2.0
var damage = 400.0
var radius = 8.0

func _ready():
    # Bounce physics
    mass = 1.0
    gravity_scale = 2.0

func _process(delta):
    timer -= delta
    if timer <= 0:
        explode()

func explode():
    var zombies = get_tree().get_nodes_in_group("zombie")
    var has_hit = false
    for z in zombies:
        if z.is_dead: continue
        var dist = global_position.distance_to(z.global_position)
        if dist < radius:
            var dmg = damage * (1.0 - (dist / radius))
            z.take_damage(dmg, false, (z.global_position - global_position).normalized())
            has_hit = true
            
    var imp_pool = get_tree().get_first_node_in_group("impact_pool")
    if imp_pool:
        # Spawn big concrete explosion impact as a placeholder for a real explosion
        imp_pool.spawn_impact("concrete", global_position, Vector3.UP)
        imp_pool.spawn_impact("concrete", global_position + Vector3(1,0,0), Vector3.UP)
        imp_pool.spawn_impact("concrete", global_position + Vector3(-1,0,0), Vector3.UP)
        
    queue_free()
