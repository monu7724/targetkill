class_name ErrorHandler
extends RefCounted

enum Category {
	LOAD_ERROR,
	RESOURCE_ERROR,
	SAVE_ERROR,
	GRAPHICS_FALLBACK
}

static var error_history: Array[Dictionary] = []
const MAX_HISTORY = 50

static func report_error(cat: Category, message: String, context: Dictionary = {}):
	var cat_str = "UNKNOWN"
	match cat:
		Category.LOAD_ERROR: cat_str = "LOAD_ERROR"
		Category.RESOURCE_ERROR: cat_str = "RESOURCE_ERROR"
		Category.SAVE_ERROR: cat_str = "SAVE_ERROR"
		Category.GRAPHICS_FALLBACK: cat_str = "GRAPHICS_FALLBACK"
		
	var entry = {
		"timestamp_ms": Time.get_ticks_msec(),
		"category": cat_str,
		"message": message,
		"context": context
	}
	error_history.append(entry)
	if error_history.size() > MAX_HISTORY:
		error_history.pop_front()
		
	print("[%d ms] [ERROR:%s] %s %s" % [entry.timestamp_ms, cat_str, message, str(context) if not context.is_empty() else ""])

static func get_recent_errors() -> Array[Dictionary]:
	return error_history

static func clear_history():
	error_history.clear()
