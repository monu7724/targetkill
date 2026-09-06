class_name WeaponDataController
extends Resource

const MAX_UPGRADE_LEVEL: int = 5

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
@export var unlock_price: int = 0

# Upgrade Base Costs ($200 to $3,000 range)
@export var upgrade_cost_damage: int = 200
@export var upgrade_cost_mag: int = 200
@export var upgrade_cost_reload: int = 200
@export var upgrade_cost_accuracy: int = 200

# 4 Upgrade Paths
func get_damage(level: int) -> float:
	var lvl = clampi(level, 0, MAX_UPGRADE_LEVEL)
	return base_damage * (1.0 + (lvl * 0.18))

func get_mag_size(level: int) -> int:
	var lvl = clampi(level, 0, MAX_UPGRADE_LEVEL)
	if base_mag_size <= 1:
		return base_mag_size
	var inc = max(1, int(round(float(base_mag_size) * 0.20)))
	return base_mag_size + (lvl * inc)

func get_reload_time(level: int) -> float:
	var lvl = clampi(level, 0, MAX_UPGRADE_LEVEL)
	return max(0.4, base_reload_time * max(0.4, 1.0 - (lvl * 0.12)))

func get_spread(level: int) -> float:
	var lvl = clampi(level, 0, MAX_UPGRADE_LEVEL)
	if spread <= 0.0001:
		return 0.0
	return max(0.0005, spread * max(0.3, 1.0 - (lvl * 0.15)))

func get_accuracy(level: int) -> float:
	var sp = get_spread(level)
	return clampf((1.0 - (sp / 0.1)) * 100.0, 10.0, 100.0)

func get_headshot_damage(level: int) -> float:
	return get_damage(level) * headshot_multiplier

# Cost curves ($200 to $3,000)
func get_upgrade_cost(stat_name: String, current_level: int) -> int:
	if current_level >= MAX_UPGRADE_LEVEL:
		return -1
	var base_cost: int = 200
	match stat_name:
		"damage": base_cost = upgrade_cost_damage
		"mag", "magazine": base_cost = upgrade_cost_mag
		"reload": base_cost = upgrade_cost_reload
		"accuracy", "spread": base_cost = upgrade_cost_accuracy
		_: base_cost = upgrade_cost_damage
	var cost = int(round(float(base_cost) * pow(1.4, current_level) / 10.0)) * 10
	return clampi(cost, 200, 3000)

func can_upgrade(stat_name: String, current_level: int, current_cash: int) -> bool:
	if current_level >= MAX_UPGRADE_LEVEL:
		return false
	var cost = get_upgrade_cost(stat_name, current_level)
	return current_cash >= cost and cost > 0
