extends Control

var tap_count: int = 0
var tap_reset_timer: float = 0.0
var bg_cam: Camera3D = null
var bg_time: float = 0.0

func _ready():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MAIN_MENU)
		
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr:
		audio_mgr.play_location_ambience("airport")
		
	bg_cam = find_child("BackgroundCamera", true, false)
	
	var save_mgr = get_node_or_null("/root/SaveManager")
	var cash_label = get_node_or_null("TopBar/CashLabel")
	if save_mgr and cash_label:
		cash_label.text = "CASH: $%d" % save_mgr.data.cash
		
	print("[%d ms] [MAIN_MENU] MainMenu ready." % Time.get_ticks_msec())

func _process(delta):
	if tap_count > 0:
		tap_reset_timer -= delta
		if tap_reset_timer <= 0:
			tap_count = 0
			
	if bg_cam:
		bg_time += delta
		bg_cam.position.x = sin(bg_time * 0.15) * 1.2
		bg_cam.position.y = 2.2 + sin(bg_time * 0.25) * 0.15

func _on_start_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")

func _on_upgrades_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.UPGRADES)
	get_tree().change_scene_to_file("res://scenes/UI/ArmoryUI.tscn")

func _on_settings_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.change_state(game_state_mgr.State.SETTINGS)
	get_tree().change_scene_to_file("res://scenes/UI/SettingsUI.tscn")

func _on_quit_button_pressed():
	var audio_mgr = get_node_or_null("/root/AudioManager")
	if audio_mgr: audio_mgr.play_ui_click()
	get_tree().quit()

# Hidden diagnostics tap trigger (5-tap version label)
func _on_version_label_gui_input(event):
	var pressed = false
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		pressed = true
	elif event is InputEventScreenTouch and event.pressed:
		pressed = true
		
	if pressed:
		tap_count += 1
		tap_reset_timer = 2.0
		if tap_count >= 5:
			tap_count = 0
			var perf_mgr = get_node_or_null("/root/PerformanceManager")
			if perf_mgr:
				perf_mgr.toggle_diagnostics()
