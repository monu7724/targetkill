extends Node

const ErrorHandler = preload("res://scripts/Core/ErrorHandler.gd")

signal loading_started(scene_path: String)
signal loading_progress(ratio: float)
signal loading_completed(scene_path: String)
signal loading_failed(error_msg: String)

var target_scene_path: String = ""
var is_loading: bool = false
var loading_ui_layer: CanvasLayer = null
var progress_bar: ProgressBar = null
var mission_title_lbl: Label = null
var mission_sub_lbl: Label = null
var location_lbl: Label = null
var tip_lbl: Label = null
var percent_lbl: Label = null

var tips = [
	"Keep moving. They are attracted to noise.",
	"Aim for the head to inflict 2.5x critical damage.",
	"Keep distance from Heavy Workers; their attacks stagger.",
	"Use the Shotgun in tight spaces for massive stopping power.",
	"Reload before engaging a new horde wave.",
	"Upgrade weapon magazine size to reduce reload frequency."
]

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	_create_loading_ui()
	print("[%d ms] [BOOT:07] LoadingManager ready." % Time.get_ticks_msec())

func _create_loading_ui():
	loading_ui_layer = CanvasLayer.new()
	loading_ui_layer.layer = 120
	loading_ui_layer.visible = false
	add_child(loading_ui_layer)
	
	var bg = ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.04, 0.05, 0.07, 0.98)
	loading_ui_layer.add_child(bg)
	
	var container = VBoxContainer.new()
	container.set_anchors_preset(Control.PRESET_CENTER)
	container.custom_minimum_size = Vector2(720, 400)
	container.offset_left = -360
	container.offset_top = -200
	container.alignment = BoxContainer.ALIGNMENT_CENTER
	container.add_theme_constant_override("separation", 14)
	loading_ui_layer.add_child(container)
	
	var brand_lbl = Label.new()
	brand_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	brand_lbl.text = "SECTOR ZERO: LOCKDOWN"
	brand_lbl.add_theme_font_size_override("font_size", 34)
	brand_lbl.add_theme_color_override("font_color", Color(1.0, 0.78, 0.25))
	container.add_child(brand_lbl)
	
	mission_title_lbl = Label.new()
	mission_title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	mission_title_lbl.text = "MISSION 01"
	mission_title_lbl.add_theme_font_size_override("font_size", 22)
	mission_title_lbl.add_theme_color_override("font_color", Color(0.9, 0.95, 1.0))
	container.add_child(mission_title_lbl)
	
	mission_sub_lbl = Label.new()
	mission_sub_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	mission_sub_lbl.text = "FIRST CONTACT"
	mission_sub_lbl.add_theme_font_size_override("font_size", 18)
	mission_sub_lbl.add_theme_color_override("font_color", Color(0.7, 0.8, 0.9))
	container.add_child(mission_sub_lbl)
	
	location_lbl = Label.new()
	location_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	location_lbl.text = "AIRPORT TERMINAL"
	location_lbl.add_theme_font_size_override("font_size", 16)
	location_lbl.add_theme_color_override("font_color", Color(0.55, 0.65, 0.75))
	container.add_child(location_lbl)
	
	var spacer = Control.new()
	spacer.custom_minimum_size = Vector2(0, 16)
	container.add_child(spacer)
	
	progress_bar = ProgressBar.new()
	progress_bar.custom_minimum_size = Vector2(620, 24)
	progress_bar.min_value = 0.0
	progress_bar.max_value = 1.0
	progress_bar.value = 0.0
	progress_bar.show_percentage = false
	container.add_child(progress_bar)
	
	percent_lbl = Label.new()
	percent_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	percent_lbl.text = "Loading... 0%"
	percent_lbl.add_theme_font_size_override("font_size", 14)
	percent_lbl.add_theme_color_override("font_color", Color(0.8, 0.85, 0.9))
	container.add_child(percent_lbl)
	
	tip_lbl = Label.new()
	tip_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tip_lbl.text = "Tip: Keep moving. They are attracted to noise."
	tip_lbl.add_theme_font_size_override("font_size", 14)
	tip_lbl.add_theme_color_override("font_color", Color(0.6, 0.65, 0.7))
	container.add_child(tip_lbl)

func load_scene_async(scene_path: String, mission_data: MissionData = null):
	if is_loading:
		print("[%d ms] [LOADING] Warning: Load already in progress for %s" % [Time.get_ticks_msec(), target_scene_path])
		return
		
	var start_time = Time.get_ticks_msec()
	print("[%d ms] [LOADING] Starting async load for: %s" % [start_time, scene_path])
	
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and save_mgr.has_method("save_game"):
		save_mgr.save_game()
		
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.LOADING)
		
	target_scene_path = scene_path
	is_loading = true
	
	# Update Loading Screen UI
	if mission_data:
		mission_title_lbl.text = mission_data.mission_id.to_upper().replace("_", " ")
		mission_sub_lbl.text = mission_data.display_name.to_upper()
		location_lbl.text = mission_data.scene_path.get_file().get_basename().to_upper().replace("_", " ")
	else:
		mission_title_lbl.text = "SECTOR ZERO"
		mission_sub_lbl.text = "TACTICAL DEPLOYMENT"
		location_lbl.text = scene_path.get_file().get_basename().to_upper().replace("_", " ")
		
	tip_lbl.text = "Tip: " + tips.pick_random()
	progress_bar.value = 0.0
	percent_lbl.text = "Loading... 0%"
	loading_ui_layer.visible = true
	
	loading_started.emit(scene_path)
	
	# Request threaded load
	var err = ResourceLoader.load_threaded_request(scene_path)
	if err != OK:
		print("[%d ms] [LOADING] Threaded request failed (%d), falling back to synchronous load" % [Time.get_ticks_msec(), err])
		_fallback_synchronous_load(scene_path, start_time)
		return
		
	_run_poll_loop(start_time)

func _run_poll_loop(start_time: int):
	var poll_elapsed: float = 0.0
	var timeout_limit: float = 8.0 # Strict 8-second safety timeout
	
	while is_loading:
		var progress_arr = []
		var status = ResourceLoader.load_threaded_get_status(target_scene_path, progress_arr)
		
		match status:
			ResourceLoader.THREAD_LOAD_IN_PROGRESS:
				var p = progress_arr[0] if not progress_arr.is_empty() else 0.5
				progress_bar.value = p
				percent_lbl.text = "Loading: %d%%" % int(p * 100)
				loading_progress.emit(p)
				
				# Wait 1 frame (with process_always=true so pause state never hangs this!)
				await get_tree().create_timer(0.04, true).timeout
				poll_elapsed += 0.04
				
				if poll_elapsed >= timeout_limit:
					print("[%d ms] [LOADING] Threaded load timeout reached (%.1fs). Triggering synchronous fallback..." % [Time.get_ticks_msec(), poll_elapsed])
					_fallback_synchronous_load(target_scene_path, start_time)
					return
					
			ResourceLoader.THREAD_LOAD_LOADED:
				progress_bar.value = 1.0
				percent_lbl.text = "Loading: 100%"
				loading_progress.emit(1.0)
				
				# Brief smooth transition delay (with process_always=true)
				await get_tree().create_timer(0.12, true).timeout
				
				var packed_scene = ResourceLoader.load_threaded_get(target_scene_path)
				if packed_scene is PackedScene:
					get_tree().change_scene_to_packed(packed_scene)
					var elapsed = Time.get_ticks_msec() - start_time
					print("[%d ms] [LOADING] SUCCESS: Loaded %s in %d ms." % [Time.get_ticks_msec(), target_scene_path, elapsed])
					var perf_mgr = get_node_or_null("/root/PerformanceManager")
					if perf_mgr and perf_mgr.has_method("set_last_load_time"):
						perf_mgr.set_last_load_time(elapsed)
					loading_completed.emit(target_scene_path)
				else:
					_fallback_synchronous_load(target_scene_path, start_time)
					return
					
				loading_ui_layer.visible = false
				is_loading = false
				return
				
			ResourceLoader.THREAD_LOAD_FAILED, ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
				print("[%d ms] [LOADING] Threaded load error (%d). Triggering fallback..." % [Time.get_ticks_msec(), status])
				_fallback_synchronous_load(target_scene_path, start_time)
				return

func _fallback_synchronous_load(scene_path: String, start_time: int):
	print("[%d ms] [LOADING] Executing synchronous fallback for: %s" % [Time.get_ticks_msec(), scene_path])
	progress_bar.value = 0.95
	percent_lbl.text = "Finalizing..."
	
	var scene = load(scene_path)
	if scene is PackedScene:
		get_tree().change_scene_to_packed(scene)
		var elapsed = Time.get_ticks_msec() - start_time
		print("[%d ms] [LOADING] SUCCESS (Fallback): Loaded in %d ms." % [Time.get_ticks_msec(), elapsed])
		var perf_mgr = get_node_or_null("/root/PerformanceManager")
		if perf_mgr and perf_mgr.has_method("set_last_load_time"):
			perf_mgr.set_last_load_time(elapsed)
		loading_completed.emit(scene_path)
		loading_ui_layer.visible = false
		is_loading = false
	else:
		_handle_load_failure("Unable to load scene resource: " + scene_path)

func _handle_load_failure(reason: String):
	ErrorHandler.report_error(ErrorHandler.Category.LOAD_ERROR, reason, {"scene": target_scene_path})
	is_loading = false
	loading_failed.emit(reason)
	
	mission_title_lbl.text = "MISSION COULD NOT BE LOADED"
	mission_sub_lbl.text = "RETURNING TO MISSION SELECT"
	location_lbl.text = reason
	progress_bar.value = 0.0
	percent_lbl.text = "Error"
	
	await get_tree().create_timer(1.8, true).timeout
	loading_ui_layer.visible = false
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
		
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
