extends CanvasLayer

@onready var health_bar = $Control/TopBar/Margin/HBox/LeftBox/HBoxHP/HealthBar
@onready var hp_label = $Control/TopBar/Margin/HBox/LeftBox/HBoxHP/HPLabel
@onready var wave_label = $Control/TopBar/Margin/HBox/LeftBox/WaveLabel
@onready var mission_name_label = $Control/TopBar/Margin/HBox/CenterBox/MissionName
@onready var objective_label = $Control/TopBar/Margin/HBox/CenterBox/ObjectiveLabel
@onready var coins_label = $Control/TopBar/Margin/HBox/RightBox/CoinsLabel
@onready var ammo_label = $Control/TopBar/Margin/HBox/RightBox/AmmoLabel
@onready var pause_button = $Control/TopBar/Margin/HBox/PauseButton
@onready var boss_health_bar = $Control/BossHealthBar
@onready var boss_name_label = $Control/BossHealthBar/BossName

@onready var crosshair = $Control/Crosshair
@onready var hitmarker = $Control/Crosshair/Hitmarker

@onready var virtual_joystick = $Control/VirtualJoystick
@onready var look_area = $Control/LookArea
@onready var fire_button = $Control/FireButton
@onready var reload_button = $Control/ReloadButton
@onready var switch_button = $Control/SwitchButton

@onready var pause_menu = $PauseMenu
@onready var resume_btn = $PauseMenu/Panel/VBox/ResumeBtn
@onready var restart_btn = $PauseMenu/Panel/VBox/RestartBtn
@onready var settings_btn = $PauseMenu/Panel/VBox/SettingsBtn
@onready var exit_btn = $PauseMenu/Panel/VBox/ExitBtn

var player = null
var look_touch_id: int = -1
var fire_touch_id: int = -1
var is_game_over: bool = false
var hitmarker_timer: SceneTreeTimer = null

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	await get_tree().process_frame
	player = get_tree().get_first_node_in_group("player")
	_connect_controls()
	_connect_pause_menu()
	
	var save_mgr = get_node_or_null("/root/SaveManager")
	if save_mgr and "data" in save_mgr:
		update_coins(save_mgr.data.coins)
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr:
		if not mission_mgr.mission_completed.is_connected(_on_game_over):
			mission_mgr.mission_completed.connect(_on_game_over)
		if not mission_mgr.mission_failed.is_connected(_on_game_over):
			mission_mgr.mission_failed.connect(_on_game_over)
			
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.objective_updated.connect(func(title, _desc, prog, target):
			update_objective(title, "Zombies Remaining: %d" % max(0, target - prog))
		)

func _connect_controls():
	if virtual_joystick and player:
		virtual_joystick.movement_changed.connect(func(vec):
			if player and player.has_method("set_virtual_movement"):
				player.set_virtual_movement(vec)
		)
		
	if fire_button:
		fire_button.gui_input.connect(_on_fire_button_input)
		
	if reload_button:
		reload_button.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			if player and player.has_method("_trigger_reload"):
				player._trigger_reload()
		)
		
	if switch_button:
		switch_button.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			if player and player.has_method("switch_weapon"):
				player.switch_weapon()
		)
		
	if look_area:
		look_area.gui_input.connect(_on_look_area_input)
		
	if pause_button:
		pause_button.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			toggle_pause()
		)

func _on_fire_button_input(event: InputEvent):
	if is_game_over: return
	if event is InputEventScreenTouch:
		if event.pressed:
			if fire_touch_id == -1:
				fire_touch_id = event.index
				if player and player.has_method("start_fire"):
					player.start_fire()
		else:
			if event.index == fire_touch_id or event.is_canceled():
				fire_touch_id = -1
				if player and player.has_method("stop_fire"):
					player.stop_fire()
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				if player and player.has_method("start_fire"):
					player.start_fire()
			else:
				if player and player.has_method("stop_fire"):
					player.stop_fire()
			get_viewport().set_input_as_handled()

func _on_look_area_input(event: InputEvent):
	if is_game_over or not player or not player.has_method("rotate_camera"):
		return
		
	var joy_id = virtual_joystick.touch_index if virtual_joystick else -1
	if event is InputEventScreenTouch:
		# Strictly ignore touches belonging to joystick or fire
		if event.index == fire_touch_id or event.index == joy_id:
			return
		if event.pressed:
			if look_touch_id == -1:
				look_touch_id = event.index
		else:
			if event.index == look_touch_id or event.is_canceled():
				look_touch_id = -1
	elif event is InputEventScreenDrag:
		# Strictly ensure this drag is NOT from fire or joystick
		if event.index == fire_touch_id or event.index == joy_id:
			return
		if look_touch_id == -1:
			look_touch_id = event.index
		if event.index == look_touch_id:
			player.rotate_camera(event.relative.x, event.relative.y)
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		player.rotate_camera(event.relative.x, event.relative.y)

func _unhandled_input(event: InputEvent):
	if event is InputEventScreenTouch and (not event.pressed or event.is_canceled()):
		if event.index == look_touch_id:
			look_touch_id = -1
		if event.index == fire_touch_id:
			fire_touch_id = -1
			if player and player.has_method("stop_fire"):
				player.stop_fire()

func show_hitmarker(is_headshot: bool = false):
	if not hitmarker:
		return
	var hit_color = Color(1.0, 0.85, 0.2, 1.0) if is_headshot else Color(1.0, 0.2, 0.2, 1.0)
	for child in hitmarker.get_children():
		if child is ColorRect:
			child.color = hit_color
	hitmarker.show()
	var cur_timer = get_tree().create_timer(0.12)
	hitmarker_timer = cur_timer
	await cur_timer.timeout
	if hitmarker_timer == cur_timer and hitmarker:
		hitmarker.hide()

func _connect_pause_menu():
	if resume_btn:
		resume_btn.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			toggle_pause()
		)
	if restart_btn:
		restart_btn.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			_on_restart_pressed()
		)
	if settings_btn:
		settings_btn.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			_on_settings_pressed()
		)
	if exit_btn:
		exit_btn.pressed.connect(func():
			var audio = get_node_or_null("/root/AudioManager")
			if audio: audio.play_ui_click()
			_on_exit_pressed()
		)

func toggle_pause():
	if is_game_over:
		return
		
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		if game_state_mgr.is_paused():
			game_state_mgr.resume_game()
		else:
			game_state_mgr.pause_game()
		pause_menu.visible = game_state_mgr.is_paused()
	else:
		var is_paused = not get_tree().paused
		get_tree().paused = is_paused
		pause_menu.visible = is_paused
		
	look_touch_id = -1
	fire_touch_id = -1

func _on_game_over(_m = null):
	is_game_over = true
	if pause_menu:
		pause_menu.visible = false
	if pause_button:
		pause_button.disabled = true
	look_touch_id = -1
	fire_touch_id = -1
	if virtual_joystick:
		virtual_joystick.visible = false
	if fire_button:
		fire_button.visible = false
	if reload_button:
		reload_button.visible = false
	if switch_button:
		switch_button.visible = false
	if look_area:
		look_area.visible = false

func _on_restart_pressed():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.resume_game()
	else:
		get_tree().paused = false
		
	var mission_mgr = get_node_or_null("/root/MissionManager")
	if mission_mgr and mission_mgr.current_mission:
		mission_mgr.start_mission(mission_mgr.current_mission)
	else:
		get_tree().reload_current_scene()

func _on_settings_pressed():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.resume_game()
		game_state_mgr.change_state(game_state_mgr.State.SETTINGS)
	else:
		get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/UI/SettingsUI.tscn")

func _on_exit_pressed():
	var game_state_mgr = get_node_or_null("/root/GameStateManager")
	if game_state_mgr:
		game_state_mgr.resume_game()
		game_state_mgr.change_state(game_state_mgr.State.MISSION_SELECT)
	else:
		get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")

func update_health(value: float, max_val: float = 100.0):
	if health_bar:
		health_bar.max_value = max_val
		health_bar.value = value
	if hp_label:
		hp_label.text = " " + str(int(value)) + " HP"

func update_ammo(current: int, total: int, weapon_name: String = "", next_weapon: String = ""):
	if ammo_label:
		if weapon_name != "":
			ammo_label.text = weapon_name.to_upper() + ": " + str(current) + " / " + str(total)
		else:
			ammo_label.text = str(current) + " / " + str(total)
	if switch_button and next_weapon != "":
		switch_button.text = "NEXT:\n" + next_weapon.to_upper()

func update_objective(title: String, detail: String = ""):
	if mission_name_label:
		mission_name_label.text = title.to_upper()
	if objective_label:
		objective_label.text = detail if detail != "" else title

func update_coins(value: int):
	if coins_label:
		coins_label.text = "COINS: " + str(value)

func update_wave(value: int):
	if wave_label:
		wave_label.text = "WAVE: " + str(value)

func show_boss_health(b_name: String, max_hp: float):
	if boss_health_bar:
		boss_health_bar.max_value = max_hp
		boss_health_bar.value = max_hp
		if boss_name_label:
			boss_name_label.text = "BOSS: " + b_name.to_upper()
		boss_health_bar.show()

func update_boss_health(value: float):
	if boss_health_bar:
		boss_health_bar.value = value
		if value <= 0:
			boss_health_bar.hide()
