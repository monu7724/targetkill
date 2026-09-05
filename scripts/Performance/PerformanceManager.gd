extends Node

enum Profile {
	LOW,
	MEDIUM,
	HIGH
}

var current_profile: Profile = Profile.MEDIUM
var current_fps: float = 60.0
var frame_time_ms: float = 16.6
var low_fps_timer: float = 0.0
var is_adaptive_throttling: bool = false

var diagnostics_layer: CanvasLayer = null
var diagnostics_label: Label = null
var is_diagnostics_visible: bool = false

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	_create_diagnostics_overlay()
	_apply_initial_profile()

func _apply_initial_profile():
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and save_mgr.data.has("selected_quality"):
		set_profile(save_mgr.data.selected_quality as Profile)
	else:
		set_profile(Profile.MEDIUM)

func set_profile(profile: Profile):
	current_profile = profile
	
	var q_mgr = get_node_or_null("/root/QualityManager")
	if q_mgr and q_mgr.has_method("apply_quality"):
		q_mgr.apply_quality(profile as int)

func _process(delta):
	current_fps = Performance.get_monitor(Performance.TIME_FPS)
	frame_time_ms = delta * 1000.0
	
	# Adaptive performance monitoring
	if current_fps < 28.0 and not is_adaptive_throttling:
		low_fps_timer += delta
		if low_fps_timer >= 3.5:
			is_adaptive_throttling = true
			if current_profile > Profile.LOW:
				set_profile(Profile.LOW)
				print("[PerformanceManager] Adaptive throttling triggered: Switched to LOW profile.")
	else:
		low_fps_timer = max(0.0, low_fps_timer - delta)
		
	if is_diagnostics_visible and diagnostics_label:
		_update_diagnostics_display()

func _create_diagnostics_overlay():
	diagnostics_layer = CanvasLayer.new()
	diagnostics_layer.layer = 128
	diagnostics_layer.visible = false
	add_child(diagnostics_layer)
	
	var panel = PanelContainer.new()
	panel.offset_left = 12
	panel.offset_top = 12
	panel.custom_minimum_size = Vector2(280, 180)
	diagnostics_layer.add_child(panel)
	
	diagnostics_label = Label.new()
	diagnostics_label.add_theme_font_size_override("font_size", 12)
	panel.add_child(diagnostics_label)

func toggle_diagnostics():
	is_diagnostics_visible = not is_diagnostics_visible
	if diagnostics_layer:
		diagnostics_layer.visible = is_diagnostics_visible

func _update_diagnostics_display():
	var os_name = OS.get_name()
	var adapter = RenderingServer.get_video_adapter_name()
	var mem_static = Performance.get_monitor(Performance.MEMORY_STATIC) / (1024.0 * 1024.0)
	var objects = Performance.get_monitor(Performance.OBJECT_COUNT)
	var draw_calls = Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	
	var profile_str = "LOW" if current_profile == Profile.LOW else ("MEDIUM" if current_profile == Profile.MEDIUM else "HIGH")
	
	diagnostics_label.text = """[SECTOR ZERO DIAGNOSTICS]
FPS: %d (%.1f ms)
OS: %s | GPU: %s
Profile: %s | Throttling: %s
Static RAM: %.1f MB | Objects: %d
Draw Calls: %d
""" % [int(current_fps), frame_time_ms, os_name, adapter.substr(0, 18), profile_str, str(is_adaptive_throttling), mem_static, int(objects), int(draw_calls)]
