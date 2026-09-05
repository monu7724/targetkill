class_name WorldStreamer
extends Node

@export var active_distance: float = 30.0
@export var cull_distance: float = 75.0
@export var check_interval: float = 0.5

var player: Node3D = null
var dynamic_props: Array[Node3D] = []
var timer: float = 0.0

func _ready():
	# Collect dynamic props within this environment
	for child in get_parent().find_children("*", "VisualInstance3D", true, false):
		if child is Node3D and child.is_in_group("streamable"):
			dynamic_props.append(child)

func _process(delta):
	timer -= delta
	if timer <= 0.0:
		timer = check_interval
		_update_visibility()

func _update_visibility():
	if not player:
		player = get_tree().get_first_node_in_group("player")
		if not player: return
		
	var player_pos = player.global_position
	for prop in dynamic_props:
		if is_instance_valid(prop):
			var dist = prop.global_position.distance_to(player_pos)
			prop.visible = (dist <= cull_distance)
