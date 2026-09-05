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

@onready var virtual_joystick = $Control/VirtualJoystick
@onready var look_area = $Control/LookArea
@onready var fire_button = $Control/FireButton
@onready var reload_button = $Control/ReloadButton
@onready var switch_button = $Control/SwitchButton

@onready var pause_menu = $PauseMenu
@onready var resume_btn = $PauseMenu/Panel/VBox/ResumeBtn
@onready var restart_btn = $PauseMenu/Panel/VBox/RestartBtn
@onready var exit_btn = $PauseMenu/Panel/VBox/ExitBtn

var player = null
var look_touch_id: int = -1

func _ready():
	await get_tree().process_frame
	player = get_tree().get_first_node_in_group("player")
	_connect_controls()
	_connect_pause_menu()
	if SaveManager:
		update_coins(SaveManager.data.coins)

func _connect_controls():
	if virtual_joystick and player:
		virtual_joystick.movement_changed.connect(func(vec):
			if player and player.has_method("set_virtual_movement"):
				player.set_virtual_movement(vec)
		)
		
	if fire_button:
		fire_button.button_down.connect(func():
			if player and player.has_method("start_fire"):
				player.start_fire()
		)
		fire_button.button_up.connect(func():
			if player and player.has_method("stop_fire"):
				player.stop_fire()
		)
		
	if reload_button:
		reload_button.pressed.connect(func():
			if player and player.has_method("_trigger_reload"):
				player._trigger_reload()
		)
		
	if switch_button:
		switch_button.pressed.connect(func():
			if player and player.has_method("switch_weapon"):
				player.switch_weapon()
		)
		
	if look_area:
		look_area.gui_input.connect(_on_look_area_input)
		
	if pause_button:
		pause_button.pressed.connect(toggle_pause)

func _on_look_area_input(event: InputEvent):
	if not player or not player.has_method("rotate_camera"):
		return
		
	if event is InputEventScreenTouch:
		if event.pressed and look_touch_id == -1:
			look_touch_id = event.index
		elif not event.pressed and event.index == look_touch_id:
			look_touch_id = -1
	elif event is InputEventScreenDrag and event.index == look_touch_id:
		player.rotate_camera(event.relative.x, event.relative.y)
	elif event is InputEventMouseMotion and Input.is_mouse_button_pressed(MOUSE_BUTTON_LEFT):
		player.rotate_camera(event.relative.x, event.relative.y)

func _connect_pause_menu():
	if resume_btn:
		resume_btn.pressed.connect(toggle_pause)
	if restart_btn:
		restart_btn.pressed.connect(_on_restart_pressed)
	if exit_btn:
		exit_btn.pressed.connect(_on_exit_pressed)

func toggle_pause():
	var is_paused = not get_tree().paused
	get_tree().paused = is_paused
	pause_menu.visible = is_paused

func _on_restart_pressed():
	get_tree().paused = false
	if MissionManager and MissionManager.current_mission:
		MissionManager.start_mission(MissionManager.current_mission)
	else:
		get_tree().reload_current_scene()

func _on_exit_pressed():
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/UI/MissionSelect.tscn")

func update_health(value: float, max_val: float = 100.0):
	if health_bar:
		health_bar.max_value = max_val
		health_bar.value = value
	if hp_label:
		hp_label.text = " " + str(int(value)) + " HP"

func update_ammo(current: int, total: int, weapon_name: String = ""):
	if ammo_label:
		if weapon_name != "":
			ammo_label.text = weapon_name + ": " + str(current) + " / " + str(total)
		else:
			ammo_label.text = str(current) + " / " + str(total)

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
