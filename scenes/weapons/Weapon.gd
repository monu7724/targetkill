extends Node3D

@onready var raycast = $RayCast3D
@onready var anim_player = $AnimationPlayer
@onready var muzzle_flash = $MuzzleFlash
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

func apply_upgrades():
	if not weapon_data: return
	
	var levels = SaveManager.data.weapon_upgrades.get(weapon_data.weapon_id, {"damage": 0, "mag": 0, "reload": 0})
	damage = weapon_data.get_damage(levels.damage)
	fire_rate = weapon_data.base_fire_rate
	max_ammo = weapon_data.get_mag_size(levels.mag)
	reload_time = weapon_data.get_reload_time(levels.reload)

func shoot():
	if not can_shoot or is_reloading:
		return
	
	if current_ammo <= 0:
		sfx_empty.play()
		return
		
	current_ammo -= 1
	can_shoot = false
	fire_timer.start()
	
	# Visuals & Sound
	muzzle_flash_fx()
	sfx_shoot.play()
	apply_recoil()
	
	# Hit Detection
	if raycast.is_colliding():
		var collider = raycast.get_collider()
		var point = raycast.get_collision_point()
		var normal = raycast.get_collision_normal()
		
		var type = "concrete"
		if collider.has_method("take_damage"):
			collider.take_damage(damage)
			type = "blood"
		
		if impact_pool:
			impact_pool.spawn_impact(type, point, normal)

func reload():
	if is_reloading or current_ammo == max_ammo:
		return
		
	is_reloading = true
	sfx_reload.play()
	# Play reload animation
	await get_tree().create_timer(reload_time).timeout
	current_ammo = max_ammo
	is_reloading = false

func muzzle_flash_fx():
	muzzle_flash.show()
	await get_tree().create_timer(0.05).timeout
	muzzle_flash.hide()

func apply_recoil():
	position.z = lerp(position.z, 0.1, 0.5)
	rotation.x = lerp(rotation.x, deg_to_rad(recoil_rotation), 0.5)
	
func _process(delta):
	position.z = lerp(position.z, 0.0, 5.0 * delta)
	rotation.x = lerp(rotation.x, 0.0, 5.0 * delta)

func _on_fire_timer_timeout():
	can_shoot = true
