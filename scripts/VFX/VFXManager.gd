class_name VFXManager
extends Node3D

var pools = {}
@export var impact_scenes: Dictionary = {}
@export var pool_size: int = 16

var audio_flesh = preload("res://audio/impacts/sfx_impact_flesh.wav")
var audio_concrete = preload("res://audio/impacts/sfx_impact_concrete.wav")

func _ready():
	add_to_group("impact_pool")
	_init_pools()

func _init_pools():
	if impact_scenes.is_empty():
		impact_scenes = {
			"blood": preload("res://scenes/weapons/BloodEffect.tscn"),
			"concrete": preload("res://scenes/weapons/ImpactEffect.tscn")
		}
		
	for type in impact_scenes.keys():
		var pool = []
		for i in range(pool_size):
			var effect = impact_scenes[type].instantiate()
			effect.hide()
			add_child(effect)
			pool.append(effect)
		pools[type] = pool

func spawn_impact(type: String, pos: Vector3, normal: Vector3):
	_play_impact_audio(type, pos)
	
	if not pools.has(type):
		type = "concrete"
		if not pools.has(type):
			return
			
	for effect in pools[type]:
		if not effect.visible:
			effect.global_position = pos
			if normal.length() > 0.1:
				effect.look_at(pos + normal, Vector3.UP)
			effect.show()
			
			if effect.has_method("play_effect"):
				effect.play_effect()
			elif effect.has_method("restart"):
				effect.restart()
				
			_schedule_auto_hide(effect, 1.2)
			return

func _schedule_auto_hide(node: Node3D, delay: float):
	await get_tree().create_timer(delay).timeout
	if is_instance_valid(node):
		node.hide()

func _play_impact_audio(type: String, pos: Vector3):
	var p = AudioStreamPlayer3D.new()
	p.stream = audio_flesh if type == "blood" else audio_concrete
	p.max_distance = 25.0
	p.global_position = pos
	add_child(p)
	p.finished.connect(func(): p.queue_free())
	p.play()
