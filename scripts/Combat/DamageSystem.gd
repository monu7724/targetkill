class_name DamageSystem
extends RefCounted

static func calculate_damage(base_damage: float, distance: float, max_range: float, falloff_factor: float = 0.5) -> float:
	if max_range <= 0.0 or distance <= 0.0:
		return base_damage
	var normalized_dist = clamp(distance / max_range, 0.0, 1.0)
	var falloff = lerp(1.0, falloff_factor, normalized_dist)
	return base_damage * falloff

static func process_hit(target: Node, base_damage: float, hit_point: Vector3, shooter_pos: Vector3, is_headshot_override: bool = false) -> Dictionary:
	var hit_dir = (hit_point - shooter_pos).normalized()
	var final_damage = base_damage
	var is_headshot = is_headshot_override
	var hit_zone = "body"
	
	if target is HitZone:
		var res = target.take_hit(base_damage, hit_dir)
		final_damage = res.final_damage
		is_headshot = res.is_headshot
		hit_zone = res.zone
	elif target.has_method("take_damage"):
		# Vertical head check fallback if target is directly a CharacterBody3D
		if is_headshot_override or hit_point.y > target.global_position.y + 1.2:
			final_damage *= 2.0
			is_headshot = true
			hit_zone = "head"
		target.take_damage(final_damage, is_headshot, hit_dir)
	
	return {
		"final_damage": final_damage,
		"is_headshot": is_headshot,
		"hit_zone": hit_zone,
		"hit_point": hit_point,
		"hit_dir": hit_dir
	}
