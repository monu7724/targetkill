extends Resource
class_name MissionData

enum ObjectiveType { KILL_COUNT, SURVIVE_WAVES, BOSS_KILL }

@export var mission_id: String
@export var display_name: String
@export_multiline var description: String
@export var objective_type: ObjectiveType = ObjectiveType.KILL_COUNT
@export var target_count: int = 10
@export var wave_count: int = 1
@export var reward_coins: int = 100
@export var unlock_requirement_id: String = "" # ID of mission that must be completed

@export var spawn_config: Array[Dictionary] = [
	{"type": "normal", "weight": 1.0}
]
