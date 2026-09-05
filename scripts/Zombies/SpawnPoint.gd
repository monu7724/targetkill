class_name SpawnPoint
extends Marker3D

enum DirectionZone {
	FRONT,
	LEFT,
	RIGHT,
	REAR,
	DISTANT
}

@export var zone: DirectionZone = DirectionZone.FRONT
@export var min_player_distance: float = 12.0
@export var max_player_distance: float = 45.0
@export var is_active: bool = true

func is_valid_for_spawn(player_pos: Vector3) -> bool:
	if not is_active:
		return false
	var dist = global_position.distance_to(player_pos)
	if dist < min_player_distance or dist > max_player_distance:
		return false
	return true
