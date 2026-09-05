extends Node3D

@onready var raycast = $RayCast3D
@onready var anim_player = $AnimationPlayer
@onready var muzzle_flash = $MuzzleFlash
@onready var muzzle_light = get_node_or_null("MuzzleLight")
@onready var fire_timer = $FireTimer
@onready var sfx_shoot = $SfxShoot
@onready var sfx_empty = $SfxEmpty
@onready var sfx_reload = $SfxReload
@onready var impact_pool = get_tree().get_first_node_in_group("impact_pool")

@export var weapon_data: WeaponData
@export var recoil_rotation: float = 5.0

var damage: float
var fire_rate: float
var max_ammo: int
var reload_time: float
var current_ammo: int

var can_shoot: bool = true
var is_reloading: bool = false

func _ready():
	apply_upgrades()
	current_ammo = max_ammo
	fire_timer.wait_time = fire_rate
	fire_timer.one_shot = true
	muzzle_flash.hide()
	
	if weapon_data:
		match weapon_data.weapon_id:
			"pistol":
				sfx_shoot.stream = preload("res://audio/weapons/sfx_pistol_shoot.wav")
			"rifle":
				sfx_shoot.stream = preload("res://audio/weapons/sfx_rifle_shoot.wav")
			"shotgun":
				sfx_shoot.stream = preload("res://audio/weapons/sfx_shotgun_shoot.wav")
		sfx_empty.stream = preload("res://audio/weapons/sfx_empty.wav")
		sfx_reload.stream = preload("res://audio/weapons/sfx_reload.wav")

func apply_upgrades():
	if not weapon_data: return
	
	var levels = SaveManager.data.weapon_upgrades.get(weapon_data.weapon_id, {"damage": 0, "mag": 0, "reload": 0})
	damage = weapon_data.get_damage(levels.damage)
	fire_rate = weapon_data.base_fire_rate
	max_ammo = weapon_data.get_mag_size(levels.mag)
	reload_time = weapon_data.get_reload_time(levels.reload)

signal ammo_changed(current_ammo, max_ammo)
signal weapon_reloaded

var aim_raycast: RayCast3D = null

func shoot():
	if not can_shoot or is_reloading:
		return
	
	if current_ammo <= 0:
		sfx_empty.play()
		return
		
	current_ammo -= 1
	can_shoot = false
	fire_timer.wait_time = fire_rate
	fire_timer.start()
	ammo_changed.emit(current_ammo, max_ammo)
	
	# Visuals & Sound
	muzzle_flash_fx()
	sfx_shoot.play()
	apply_recoil()
	
	# Hit Detection using camera aim raycast if available, else local raycast
	var target_ray = aim_raycast if aim_raycast else raycast
	if target_ray and target_ray.is_colliding():
		var collider = target_ray.get_collider()
		var point = target_ray.get_collision_point()
		var normal = target_ray.get_collision_normal()
		
		var type = "concrete"
		if collider and collider.has_method("take_damage"):
			var final_damage = damage
			var is_headshot = false
			# Headshot detection: top of zombie mesh
			if point.y > collider.global_position.y + 1.2:
				final_damage *= 2.0
				is_headshot = true
			collider.take_damage(final_damage)
			type = "blood"
			
			var hud_node = get_tree().get_first_node_in_group("hud")
			if hud_node and hud_node.has_method("show_hitmarker"):
				hud_node.show_hitmarker(is_headshot)
		
		if not impact_pool:
			impact_pool = get_tree().get_first_node_in_group("impact_pool")
		if impact_pool:
			impact_pool.spawn_impact(type, point, normal)

func reload():
	if is_reloading or current_ammo == max_ammo:
		return
		
	is_reloading = true
	sfx_reload.play()
	await get_tree().create_timer(reload_time).timeout
	current_ammo = max_ammo
	is_reloading = false
	ammo_changed.emit(current_ammo, max_ammo)
	weapon_reloaded.emit()

func muzzle_flash_fx():
	if muzzle_light:
		muzzle_light.visible = true
	if muzzle_flash:
		muzzle_flash.show()
		if muzzle_flash is GPUParticles3D:
			muzzle_flash.restart()
			muzzle_flash.emitting = true
	await get_tree().create_timer(0.06).timeout
	if muzzle_light:
		muzzle_light.visible = false
	if muzzle_flash:
		muzzle_flash.hide()

func apply_recoil():
	position.z = 0.08
	position.y = 0.015
	rotation.x = deg_to_rad(recoil_rotation)
	
func _process(delta):
	position.z = lerp(position.z, 0.0, 10.0 * delta)
	position.y = lerp(position.y, 0.0, 10.0 * delta)
	rotation.x = lerp(rotation.x, 0.0, 10.0 * delta)

func _on_fire_timer_timeout():
	can_shoot = true
