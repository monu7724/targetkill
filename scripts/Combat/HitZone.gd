class_name HitZone
extends Area3D

enum ZoneType {
	HEAD,
	CHEST,
	ARM,
	LEG
}

@export var zone_type: ZoneType = ZoneType.CHEST
@export var damage_multiplier: float = 1.0
@export var parent_entity: Node = null

func _ready():
	# Ensure default multipliers match combat design
	match zone_type:
		ZoneType.HEAD:
			damage_multiplier = 2.5
		ZoneType.CHEST:
			damage_multiplier = 1.0
		ZoneType.ARM:
			damage_multiplier = 0.7
		ZoneType.LEG:
			damage_multiplier = 0.7

func take_hit(base_damage: float, hit_dir: Vector3 = Vector3.ZERO) -> Dictionary:
	var final_damage = base_damage * damage_multiplier
	var is_headshot = (zone_type == ZoneType.HEAD)
	var zone_name = get_zone_name()
	
	if parent_entity and parent_entity.has_method("take_damage"):
		parent_entity.take_damage(final_damage, is_headshot, hit_dir)
		
	return {
		"final_damage": final_damage,
		"is_headshot": is_headshot,
		"zone": zone_name
	}

func get_zone_name() -> String:
	match zone_type:
		ZoneType.HEAD: return "head"
		ZoneType.CHEST: return "chest"
		ZoneType.ARM: return "arm"
		ZoneType.LEG: return "leg"
		_: return "body"
