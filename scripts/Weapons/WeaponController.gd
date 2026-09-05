extends Node3D

@onready var raycast: RayCast3D = $RayCast3D
@onready var anim_player: AnimationPlayer = $AnimationPlayer
@onready var muzzle_flash = $MuzzleFlash
@onready var muzzle_light = get_node_or_null("MuzzleLight")
@onready var fire_timer: Timer = $FireTimer
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
var spread: float = 0.0
var pellet_count: int = 1
var recoil_kick: float = 1.0

var can_shoot: bool = true
var is_reloading: bool = false
var aim_raycast: RayCast3D = null

signal ammo_changed(current_ammo, max_ammo)
signal weapon_reloaded
signal fired(weapon_id)

func _ready():
	apply_upgrades()
	current_ammo = max_ammo
	fire_timer.wait_time = fire_rate
	fire_timer.one_shot = true
	if muzzle_flash:
		muzzle_flash.hide()
	if muzzle_light:
		muzzle_light.visible = false
	
	_load_sound_set()

func _load_sound_set():
	if not weapon_data: return
	match weapon_data.weapon_id:
		"pistol":
			sfx_shoot.stream = preload("res://audio/weapons/sfx_pistol_shoot.wav")
		"rifle":
			sfx_shoot.stream = preload("res://audio/weapons/sfx_rifle_shoot.wav")
		"shotgun":
			sfx_shoot.stream = preload("res://audio/weapons/sfx_shotgun_shoot.wav")
		_:
			sfx_shoot.stream = preload("res://audio/weapons/sfx_pistol_shoot.wav")
			
	sfx_empty.stream = preload("res://audio/weapons/sfx_empty.wav")
	sfx_reload.stream = preload("res://audio/weapons/sfx_reload.wav")

func apply_upgrades():
	if not weapon_data: return
	
	var save_mgr = get_node_or_null("/root/SaveManager")
	var levels = {"damage": 0, "mag": 0, "reload": 0}
	if save_mgr and save_mgr.data.has("weapon_upgrades"):
		levels = save_mgr.data.weapon_upgrades.get(weapon_data.weapon_id, levels)
		
	damage = weapon_data.get_damage(levels.damage)
	fire_rate = weapon_data.base_fire_rate
	max_ammo = weapon_data.get_mag_size(levels.mag)
	reload_time = weapon_data.get_reload_time(levels.reload)
	spread = weapon_data.spread
	pellet_count = max(1, weapon_data.pellet_count)
	recoil_kick = weapon_data.recoil

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
	fired.emit(weapon_data.weapon_id if weapon_data else "")
	
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.weapon_fired.emit(weapon_data.weapon_id if weapon_data else "", current_ammo, max_ammo)
	
	# Synchronized Pipeline Execution:
	# 1. Visual & Audio Flash in lockstep
	muzzle_flash_fx()
	sfx_shoot.play()
	
	# 2. Viewmodel Recoil
	apply_recoil()
	
	# 3. Physics Raycast & Hit Resolution
	_fire_projectiles()

func _fire_projectiles():
	var target_ray = aim_raycast if aim_raycast else raycast
	if not target_ray:
		return
		
	var space_state = get_world_3d().direct_space_state
	var ray_origin = target_ray.global_position
	var base_forward = -target_ray.global_transform.basis.z.normalized()
	var ray_range = weapon_data.range if weapon_data else 100.0
	var damage_per_pellet = damage / float(pellet_count) if pellet_count > 1 else damage
	
	var total_hit_enemy = false
	var had_headshot = false

	for p in range(pellet_count):
		# Apply spread cone
		var spread_offset = Vector3.ZERO
		if spread > 0.0001:
			spread_offset = (target_ray.global_transform.basis.x * randf_range(-spread, spread) +
							 target_ray.global_transform.basis.y * randf_range(-spread, spread))
		
		var ray_dir = (base_forward + spread_offset).normalized()
		var ray_target = ray_origin + (ray_dir * ray_range)
		
		var query = PhysicsRayQueryParameters3D.create(ray_origin, ray_target)
		query.exclude = [self, get_parent()]
		query.collide_with_areas = true
		query.collide_with_bodies = true
		
		var result = space_state.intersect_ray(query)
		if result:
			var hit_collider = result.collider
			var hit_point = result.position
			var hit_normal = result.normal
			
			var impact_type = "concrete"
			
			# Check HitZone first
			if hit_collider is HitZone:
				var res = hit_collider.take_hit(damage_per_pellet, ray_dir)
				total_hit_enemy = true
				if res.is_headshot:
					had_headshot = true
				impact_type = "blood"
			elif hit_collider and hit_collider.has_method("take_damage"):
				var is_head = false
				var final_dmg = damage_per_pellet
				var mult = weapon_data.headshot_multiplier if weapon_data else 2.0
				# Head detection: top segment
				if hit_point.y > hit_collider.global_position.y + 1.2:
					final_dmg *= mult
					is_head = true
					had_headshot = true
				hit_collider.take_damage(final_dmg, is_head, ray_dir)
				total_hit_enemy = true
				impact_type = "blood"
			
			_spawn_impact(impact_type, hit_point, hit_normal)
		elif p == 0 and target_ray.is_colliding():
			# Target raycast fallback
			var col = target_ray.get_collider()
			var pt = target_ray.get_collision_point()
			var norm = target_ray.get_collision_normal()
			var impact_type = "concrete"
			if col and col.has_method("take_damage"):
				var is_head = (pt.y > col.global_position.y + 1.2)
				var final_dmg = damage * (weapon_data.headshot_multiplier if (is_head and weapon_data) else 1.0)
				col.take_damage(final_dmg, is_head, base_forward)
				total_hit_enemy = true
				if is_head: had_headshot = true
				impact_type = "blood"
			_spawn_impact(impact_type, pt, norm)
	
	if total_hit_enemy:
		var hud_node = get_tree().get_first_node_in_group("hud")
		if hud_node and hud_node.has_method("show_hitmarker"):
			hud_node.show_hitmarker(had_headshot)

func _spawn_impact(type: String, pos: Vector3, normal: Vector3):
	if not impact_pool:
		impact_pool = get_tree().get_first_node_in_group("impact_pool")
	if impact_pool:
		impact_pool.spawn_impact(type, pos, normal)

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
	
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.weapon_reloaded.emit(weapon_data.weapon_id if weapon_data else "")

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
	position.z = 0.08 * recoil_kick
	position.y = 0.015 * recoil_kick
	rotation.x = deg_to_rad(recoil_rotation * recoil_kick)
	
func _process(delta):
	position.z = lerp(position.z, 0.0, 10.0 * delta)
	position.y = lerp(position.y, 0.0, 10.0 * delta)
	rotation.x = lerp(rotation.x, 0.0, 10.0 * delta)

func _on_fire_timer_timeout():
	can_shoot = true
