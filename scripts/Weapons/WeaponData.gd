extends Resource

@export var weapon_id: String
@export var display_name: String
@export var base_damage: float = 25.0
@export var headshot_multiplier: float = 2.0
@export var base_fire_rate: float = 0.2
@export var base_mag_size: int = 30
@export var base_reserve_ammo: int = 120
@export var base_reload_time: float = 2.0
@export var spread: float = 0.0
@export var recoil: float = 1.0
@export var range: float = 100.0
@export var pellet_count: int = 1
@export var is_automatic: bool = false
@export var muzzle_fx: String = "standard"
@export var sound_set: String = "pistol"

@export var upgrade_cost_damage: int = 100
@export var upgrade_cost_mag: int = 100
@export var upgrade_cost_reload: int = 100

func get_damage(level: int) -> float:
	return base_damage + (level * 5.0)

func get_mag_size(level: int) -> int:
	return base_mag_size + (level * 5)

func get_reload_time(level: int) -> float:
	return max(0.5, base_reload_time - (level * 0.2))

func get_headshot_damage(level: int) -> float:
	return get_damage(level) * headshot_multiplier
