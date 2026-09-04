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

func spawn_impact(type: String, pos: Vector3, normal: Vector3):
	if not pools.has(type):
		type = "concrete" # Fallback
		if not pools.has(type): return
		
	for impact in pools[type]:
		if not impact.visible:
			impact.global_position = pos
			if normal.length() > 0.1:
				impact.look_at(pos + normal, Vector3.UP)
			impact.show()
			if impact.has_method("restart"):
				impact.restart()
			return
