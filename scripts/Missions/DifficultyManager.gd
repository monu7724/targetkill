class_name DifficultyManager
extends RefCounted

enum Level {
	EASY,
	NORMAL,
	HARD
}

static var current_difficulty: Level = Level.NORMAL

static func set_difficulty(diff: Level):
	current_difficulty = diff

static func get_health_multiplier() -> float:
	match current_difficulty:
		Level.EASY: return 0.8
		Level.NORMAL: return 1.0
		Level.HARD: return 1.35
		_: return 1.0

static func get_damage_multiplier() -> float:
	match current_difficulty:
		Level.EASY: return 0.75
		Level.NORMAL: return 1.0
		Level.HARD: return 1.4
		_: return 1.0

static func get_reward_multiplier() -> float:
	match current_difficulty:
		Level.EASY: return 0.85
		Level.NORMAL: return 1.0
		Level.HARD: return 1.5
		_: return 1.0

static func get_spawn_interval_multiplier() -> float:
	match current_difficulty:
		Level.EASY: return 1.25 # Slower spawn cadence
		Level.NORMAL: return 1.0
		Level.HARD: return 0.8  # Aggressive spawn pressure
		_: return 1.0
