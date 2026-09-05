extends Node

signal loading_started(scene_path: String)
signal loading_progress(ratio: float)
signal loading_completed(scene_path: String)
signal loading_failed(error_msg: String)

var target_scene_path: String = ""
var is_loading: bool = false
var loading_ui_layer: CanvasLayer = null
var progress_bar: ProgressBar = null
var mission_title_lbl: Label = null
var location_lbl: Label = null
var objective_lbl: Label = null
var tip_lbl: Label = null

var tips = [
	"Aim for the head to inflict 2.5x critical damage.",
	"Keep distance from Heavy Workers; their attacks stagger.",
	"Use the Shotgun in tight spaces for massive stopping power.",
	"Reload before engaging a new horde wave.",
	"Upgrade weapon magazine size to reduce downtime."
]

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	_create_loading_ui()

func _create_loading_ui():
	loading_ui_layer = CanvasLayer.new()
	loading_ui_layer.layer = 120
	loading_ui_layer.visible = false
	add_child(loading_ui_layer)
	
	var bg = ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.04, 0.06, 0.09, 0.98)
	loading_ui_layer.add_child(bg)
	
	var container = VBoxContainer.new()
	container.set_anchors_preset(Control.PRESET_CENTER)
	container.custom_minimum_size = Vector2(700, 360)
	container.offset_left = -350
	container.offset_top = -180
	container.alignment = BoxContainer.ALIGNMENT_CENTER
	container.add_theme_constant_override("separation", 16)
	loading_ui_layer.add_child(container)
	
	mission_title_lbl = Label.new()
	mission_title_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	mission_title_lbl.text = "OPERATION: SECTOR ZERO"
	mission_title_lbl.add_theme_font_size_override("font_size", 32)
	mission_title_lbl.add_theme_color_override("font_color", Color(1.0, 0.78, 0.28))
	container.add_child(mission_title_lbl)
	
	location_lbl = Label.new()
	location_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	location_lbl.text = "LOCATION: DEPLOYMENT ZONE"
	location_lbl.add_theme_font_size_override("font_size", 18)
	location_lbl.add_theme_color_override("font_color", Color(0.65, 0.75, 0.85))
	container.add_child(location_lbl)
	
	objective_lbl = Label.new()
	objective_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	objective_lbl.text = "OBJECTIVE: SECURE PERIMETER"
	objective_lbl.add_theme_font_size_override("font_size", 20)
	objective_lbl.add_theme_color_override("font_color", Color(0.9, 0.95, 1.0))
	container.add_child(objective_lbl)
	
	var spacer = Control.new()
	spacer.custom_minimum_size = Vector2(0, 20)
	container.add_child(spacer)
	
	progress_bar = ProgressBar.new()
	progress_bar.custom_minimum_size = Vector2(600, 24)
	progress_bar.min_value = 0.0
	progress_bar.max_value = 1.0
	progress_bar.value = 0.0
	progress_bar.show_percentage = true
	container.add_child(progress_bar)
	
	tip_lbl = Label.new()
	tip_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	tip_lbl.text = "TIP: Aim for the head to inflict 2.5x critical damage."
	tip_lbl.add_theme_font_size_override("font_size", 15)
	tip_lbl.add_theme_color_override("font_color", Color(0.55, 0.62, 0.7))
	container.add_child(tip_lbl)

func load_scene_async(scene_path: String, mission_data: MissionData = null):
	if is_loading:
		printerr("[LoadingManager] Load already in progress")
		return
		
	# Save game progress before transition (Section 32)
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
		mission_title_lbl.text = mission_data.display_name.to_upper()
		location_lbl.text = "LOCATION: " + mission_data.scene_path.get_file().get_basename().to_upper()
		objective_lbl.text = "OBJECTIVE: " + mission_data.description
	else:
		mission_title_lbl.text = "SECTOR ZERO: LOCKDOWN"
		location_lbl.text = "LOCATION: " + scene_path.get_file().get_basename().to_upper()
		objective_lbl.text = "OBJECTIVE: SURVIVE"
		
	tip_lbl.text = "TIP: " + tips.pick_random()
	progress_bar.value = 0.0
	loading_ui_layer.visible = true
	
	loading_started.emit(scene_path)
	
	# Request threaded load
	var err = ResourceLoader.load_threaded_request(scene_path)
	if err != OK:
		_handle_load_failure("ResourceLoader request failed with code: " + str(err))
		return
		
	_poll_loading()

func _poll_loading():
	var progress_arr = []
	var status = ResourceLoader.load_threaded_get_status(target_scene_path, progress_arr)
	
	match status:
		ResourceLoader.THREAD_LOAD_IN_PROGRESS:
			var p = progress_arr[0] if not progress_arr.is_empty() else 0.5
			progress_bar.value = p
			loading_progress.emit(p)
			await get_tree().create_timer(0.04).timeout
			_poll_loading()
			
		ResourceLoader.THREAD_LOAD_LOADED:
			progress_bar.value = 1.0
			loading_progress.emit(1.0)
			await get_tree().create_timer(0.15).timeout # Brief smooth finish
			
			var packed_scene = ResourceLoader.load_threaded_get(target_scene_path)
			if packed_scene:
				get_tree().change_scene_to_packed(packed_scene)
				loading_completed.emit(target_scene_path)
			else:
				_handle_load_failure("Loaded resource is null or corrupted")
				return
				
			loading_ui_layer.visible = false
			is_loading = false
			
		ResourceLoader.THREAD_LOAD_FAILED, ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
			_handle_load_failure("Threaded load failed for: " + target_scene_path)

func _handle_load_failure(reason: String):
	printerr("[LoadingManager Error] ", reason)
	is_loading = false
	loading_failed.emit(reason)
	
	# Display error feedback to user (Section 32)
	mission_title_lbl.text = "UNABLE TO LOAD MISSION"
	objective_lbl.text = "Error encountered. Returning to Mission Select..."
	progress_bar.value = 0.0
	
	await get_tree().create_timer(1.8).timeout
	loading_ui_layer.visible = false
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
		
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")
