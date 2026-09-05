extends Node3D

var pools = {}
@export var impact_scenes: Dictionary = {} # Mapping of "type" to PackedScene
@export var pool_size: int = 15

func _ready():
	for type in impact_scenes.keys():
		var pool = []
		for i in range(pool_size):
			var impact = impact_scenes[type].instantiate()
			impact.hide()
			add_child(impact)
			pool.append(impact)
		pools[type] = pool

var audio_flesh = preload("res://audio/impacts/sfx_impact_flesh.wav")
var audio_concrete = preload("res://audio/impacts/sfx_impact_concrete.wav")

func spawn_impact(type: String, pos: Vector3, normal: Vector3):
	_play_impact_audio(type, pos)
	if not pools.has(type):
		type = "concrete" # Fallback
		if not pools.has(type): return
		
	for impact in pools[type]:
		if not impact.visible:
			impact.global_position = pos
			if normal.length() > 0.1:
				impact.look_at(pos + normal, Vector3.UP)
			impact.show()
			if impact.has_method("play_effect"):
				impact.play_effect()
			elif impact.has_method("restart"):
				impact.restart()
			return

func _play_impact_audio(type: String, pos: Vector3):
	var p = AudioStreamPlayer3D.new()
	p.stream = audio_flesh if type == "blood" else audio_concrete
	p.max_distance = 25.0
	p.global_position = pos
	add_child(p)
	p.finished.connect(func(): p.queue_free())
	p.play()
