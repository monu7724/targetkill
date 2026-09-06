extends Node3D
class_name AtmosphereEnhancer

@export var fan_rotation_speed: float = 4.0 # radians/sec (~240 rpm)
@export var strobe_pulse_speed: float = 3.5

@onready var dust_particles: CPUParticles3D = get_node_or_null("SunlightDust")
@onready var fan_blades = get_node_or_null("IndustrialFan/Blades")
@onready var alert_strobe = get_node_or_null("AlertStrobe/StrobeLight")

var time: float = 0.0

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	_setup_blood_pool_listener()

func _setup_blood_pool_listener():
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus and event_bus.has_signal("enemy_killed"):
		if not event_bus.enemy_killed.is_connected(_on_enemy_killed):
			event_bus.enemy_killed.connect(_on_enemy_killed)

func _on_enemy_killed(_archetype: String, _is_headshot: bool, death_pos: Vector3):
	spawn_ground_blood_decal(death_pos)

func spawn_ground_blood_decal(pos: Vector3):
	var decal = MeshInstance3D.new()
	var quad = QuadMesh.new()
	var sz = randf_range(1.2, 1.8)
	quad.size = Vector2(sz, sz)
	quad.orientation = PlaneMesh.FACE_Y
	decal.mesh = quad
	
	var mat = StandardMaterial3D.new()
	mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	mat.albedo_texture = preload("res://textures/pbr/tex_blood_decal.png")
	mat.albedo_color = Color(0.9, 0.9, 0.9, 0.85)
	mat.roughness = 0.15
	mat.metallic = 0.0
	decal.material_override = mat
	
	add_child(decal)
	decal.global_position = Vector3(pos.x, 0.02, pos.z)
	decal.rotation.y = randf_range(0, TAU)
	
	# Keep decal alive for 25s, then fade out
	var tw = create_tween()
	tw.tween_interval(25.0)
	tw.tween_property(mat, "albedo_color:a", 0.0, 3.0)
	tw.tween_callback(func(): decal.queue_free())

func _process(delta: float):
	time += delta
	# Rotate ceiling fans
	if fan_blades:
		fan_blades.rotate_y(fan_rotation_speed * delta)
		
	# Pulse emergency alert beacon
	if alert_strobe and alert_strobe is Light3D:
		var pulse = (sin(time * strobe_pulse_speed) * 0.5 + 0.5)
		alert_strobe.light_energy = 0.1 + pulse * 0.4
