extends Node

# Combat & Damage Signals
signal damage_dealt(amount: float, is_headshot: bool, hit_zone: String, target: Node)
signal enemy_killed(archetype: String, is_headshot: bool, death_position: Vector3)
signal player_health_changed(current: float, max_val: float)
signal player_died()

# Weapon Signals
signal weapon_fired(weapon_id: String, current_ammo: int, max_ammo: int)
signal weapon_reloaded(weapon_id: String)
signal weapon_switched(weapon_id: String, display_name: String)

# Mission & Progression Signals
signal wave_started(wave_number: int, total_waves: int)
signal wave_completed(wave_number: int)
signal objective_updated(title: String, description: String, progress: int, target: int)
signal coins_changed(new_total: int)
signal mission_finished(mission_id: String, success: bool)

# Performance & Settings Signals
signal quality_changed(quality_name: String)
signal performance_warning(fps: float, reason: String)

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
