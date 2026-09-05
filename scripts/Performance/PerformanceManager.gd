extends Node

enum Profile {
	LOW = 0,
	MEDIUM = 1,
	HIGH = 2
}

var current_profile: int = Profile.MEDIUM
var current_fps: float = 60.0
var frame_time_ms: float = 16.6
var low_fps_timer: float = 0.0
var is_adaptive_throttling: bool = false
var last_load_time_ms: int = 0

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
		set_profile(save_mgr.data.selected_quality)
	else:
		set_profile(Profile.MEDIUM)

func set_profile(profile_idx: int):
	current_profile = clamp(profile_idx, 0, 2)
	var q_mgr = get_node_or_null("/root/QualityManager")
	if q_mgr and q_mgr.has_method("apply_quality"):
		q_mgr.apply_quality(current_profile)

func set_last_load_time(time_ms: int):
	last_load_time_ms = time_ms

func _process(delta):
	current_fps = Performance.get_monitor(Performance.TIME_FPS)
	frame_time_ms = delta * 1000.0
	
	# Adaptive performance & frame pacing protection
	if current_fps < 28.0 and not is_adaptive_throttling:
		low_fps_timer += delta
		if low_fps_timer >= 3.0:
			is_adaptive_throttling = true
			if current_profile > Profile.LOW:
				set_profile(Profile.LOW)
				print("[%d ms] [PERF:ADAPTIVE] Frame pacing dip detected (%.1f ms). Throttling to LOW." % [Time.get_ticks_msec(), frame_time_ms])
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
	panel.offset_left = 14
	panel.offset_top = 14
	panel.custom_minimum_size = Vector2(340, 240)
	diagnostics_layer.add_child(panel)
	
	diagnostics_label = Label.new()
	diagnostics_label.add_theme_font_size_override("font_size", 11)
	panel.add_child(diagnostics_label)

func toggle_diagnostics():
	is_diagnostics_visible = not is_diagnostics_visible
	if diagnostics_layer:
		diagnostics_layer.visible = is_diagnostics_visible

func _update_diagnostics_display():
	var os_name = OS.get_name()
	var os_ver = OS.get_version()
	var adapter = RenderingServer.get_video_adapter_name()
	var is_vulkan = (RenderingServer.get_rendering_device() != null)
	var renderer_str = "Vulkan" if is_vulkan else "GLES3 (gl_compat)"
	var mem_static = Performance.get_monitor(Performance.MEMORY_STATIC) / (1024.0 * 1024.0)
	var objects = Performance.get_monitor(Performance.OBJECT_COUNT)
	var draw_calls = Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)
	
	var screen_sz = DisplayServer.screen_get_size()
	var hz = DisplayServer.screen_get_refresh_rate()
	
	var q_mgr = get_node_or_null("/root/QualityManager")
	var profile_str = q_mgr.get_profile_name(current_profile) if q_mgr and q_mgr.has_method("get_profile_name") else str(current_profile)
	
	# Active zombies count
	var active_zombies = get_tree().get_nodes_in_group("zombies").size()
	
	# VFX count in scene
	var vfx_count = get_tree().get_nodes_in_group("vfx").size()
	
	var mission_mgr = get_node_or_null("/root/MissionManager")
	var cur_mission_str = mission_mgr.current_mission.display_name if (mission_mgr and mission_mgr.current_mission) else "None / Menu"
	
	diagnostics_label.text = """=== SECTOR ZERO DIAGNOSTICS ===
OS: %s (v%s) | Renderer: %s
GPU: %s
Res: %dx%d @ %.0fHz
Profile: %s | Throttling: %s
FPS: %d | Frame Time: %.1f ms
Active Zombies: %d | VFX Count: %d
Mission: %s
Load Time: %d ms | RAM: %.1f MB
Objects: %d | Draw Calls: %d
""" % [
		os_name, str(os_ver), renderer_str,
		adapter.substr(0, 24),
		screen_sz.x, screen_sz.y, hz,
		profile_str, str(is_adaptive_throttling),
		int(current_fps), frame_time_ms,
		active_zombies, vfx_count,
		cur_mission_str,
		last_load_time_ms, mem_static,
		int(objects), int(draw_calls)
	]
