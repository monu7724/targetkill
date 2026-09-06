class_name WeaponManager
extends Node

# Canonical registry of all 10 weapons
const WEAPON_REGISTRY: Dictionary = {
	"usp45": {
		"id": "usp45",
		"display_name": "USP-45",
		"subtitle": "Tactical .45 ACP Sidearm - Reliable Critical Headshots",
		"category": "Pistol",
		"resource_path": "res://resources/weapons/usp45.tres",
		"scene_path": "res://scenes/weapons/USP45.tscn",
		"model_path": "res://assets/3d/weapons/usp45.glb",
		"unlock_price": 0,
		"default_unlocked": true,
		"aliases": ["pistol"]
	},
	"m4a1": {
		"id": "m4a1",
		"display_name": "M4A1 Sentinel",
		"subtitle": "5.56 NATO Tactical Carbine - High Cyclic Fire Rate",
		"category": "Assault Rifle",
		"resource_path": "res://resources/weapons/m4a1.tres",
		"scene_path": "res://scenes/weapons/M4A1.tscn",
		"model_path": "res://assets/3d/weapons/m4a1.glb",
		"unlock_price": 0,
		"default_unlocked": true,
		"aliases": ["rifle"]
	},
	"remington870": {
		"id": "remington870",
		"display_name": "Remington 870",
		"subtitle": "12-Gauge Pump Action - Lethal Close-Quarters Spread",
		"category": "Shotgun",
		"resource_path": "res://resources/weapons/remington870.tres",
		"scene_path": "res://scenes/weapons/Remington870.tscn",
		"model_path": "res://assets/3d/weapons/remington870.glb",
		"unlock_price": 0,
		"default_unlocked": true,
		"aliases": ["shotgun"]
	},
	"ak47": {
		"id": "ak47",
		"display_name": "AK-47 Vanguard",
		"subtitle": "7.62x39mm Combat Rifle - Heavy Kinetic Punch",
		"category": "Combat Rifle",
		"resource_path": "res://resources/weapons/ak47.tres",
		"scene_path": "res://scenes/weapons/AK47.tscn",
		"model_path": "res://assets/3d/weapons/ak47.glb",
		"unlock_price": 1500,
		"default_unlocked": false,
		"aliases": []
	},
	"desert_eagle": {
		"id": "desert_eagle",
		"display_name": "Desert Eagle .50 AE",
		"subtitle": ".50 Action Express Hand Cannon - Devastating Stopping Power",
		"category": "Heavy Handgun",
		"resource_path": "res://resources/weapons/desert_eagle.tres",
		"scene_path": "res://scenes/weapons/DesertEagle.tscn",
		"model_path": "res://assets/3d/weapons/desert_eagle.glb",
		"unlock_price": 2200,
		"default_unlocked": false,
		"aliases": ["deagle"]
	},
	"mp5": {
		"id": "mp5",
		"display_name": "MP5 Tactical",
		"subtitle": "9mm Submachine Gun - Ultra Fast Cyclic Fire Rate",
		"category": "Submachine Gun",
		"resource_path": "res://resources/weapons/mp5.tres",
		"scene_path": "res://scenes/weapons/MP5.tscn",
		"model_path": "res://assets/3d/weapons/mp5.glb",
		"unlock_price": 1200,
		"default_unlocked": false,
		"aliases": []
	},
	"awp": {
		"id": "awp",
		"display_name": "AWP Arctic Warfare",
		"subtitle": ".338 Lapua Bolt-Action Sniper - Extreme Range One-Shot Lethality",
		"category": "Sniper Rifle",
		"resource_path": "res://resources/weapons/awp.tres",
		"scene_path": "res://scenes/weapons/AWP.tscn",
		"model_path": "res://assets/3d/weapons/awp.glb",
		"unlock_price": 3500,
		"default_unlocked": false,
		"aliases": []
	},
	"combat_knife": {
		"id": "combat_knife",
		"display_name": "Combat Knife",
		"subtitle": "Serrated Tanto Blade - Silent Rapid Melee Takedowns",
		"category": "Melee",
		"resource_path": "res://resources/weapons/combat_knife.tres",
		"scene_path": "res://scenes/weapons/CombatKnife.tscn",
		"model_path": "res://assets/3d/weapons/combat_knife.glb",
		"unlock_price": 800,
		"default_unlocked": false,
		"aliases": ["knife"]
	},
	"crossbow": {
		"id": "crossbow",
		"display_name": "Silent Hunter Crossbow",
		"subtitle": "Composite Bolt Thrower - High-Tension Silent Piercing",
		"category": "Tactical Special",
		"resource_path": "res://resources/weapons/crossbow.tres",
		"scene_path": "res://scenes/weapons/Crossbow.tscn",
		"model_path": "res://assets/3d/weapons/crossbow.glb",
		"unlock_price": 2800,
		"default_unlocked": false,
		"aliases": []
	},
	"grenade_launcher": {
		"id": "grenade_launcher",
		"display_name": "M79 Grenade Launcher",
		"subtitle": "40mm Area Ordinance - High-Explosive Crowd Annihilation",
		"category": "Heavy Explosive",
		"resource_path": "res://resources/weapons/grenade_launcher.tres",
		"scene_path": "res://scenes/weapons/GrenadeLauncher.tscn",
		"model_path": "res://assets/3d/weapons/grenade_launcher.glb",
		"unlock_price": 4500,
		"default_unlocked": false,
		"aliases": ["m79"]
	}
}

# Alias resolution mapping
static func resolve_weapon_id(id: String) -> String:
	match id:
		"pistol": return "usp45"
		"rifle": return "m4a1"
		"shotgun": return "remington870"
		"deagle": return "desert_eagle"
		"knife": return "combat_knife"
		"m79": return "grenade_launcher"
		_: return id

static func get_all_weapon_ids() -> Array[String]:
	return [
		"usp45", "m4a1", "remington870", "ak47", "desert_eagle",
		"mp5", "awp", "combat_knife", "crossbow", "grenade_launcher"
	]

static func get_weapon_entry(id: String) -> Dictionary:
	var canonical = resolve_weapon_id(id)
	return WEAPON_REGISTRY.get(canonical, {})

static func get_weapon_data(id: String) -> WeaponData:
	var entry = get_weapon_entry(id)
	if entry.is_empty():
		return null
	var path = entry.get("resource_path", "")
	if ResourceLoader.exists(path):
		return load(path) as WeaponData
	return null

static func get_weapon_scene(id: String) -> PackedScene:
	var entry = get_weapon_entry(id)
	if entry.is_empty():
		return null
	var path = entry.get("scene_path", "")
	if ResourceLoader.exists(path):
		return load(path) as PackedScene
	return null

static func is_weapon_unlocked(id: String, save_mgr = null) -> bool:
	if not save_mgr:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root.has_node("SaveManager"):
			save_mgr = tree.root.get_node("SaveManager")
	if not save_mgr:
		var entry = get_weapon_entry(id)
		return entry.get("default_unlocked", false)
	
	var canonical = resolve_weapon_id(id)
	var unlocked = save_mgr.data.get("unlocked_weapons", [])
	if canonical in unlocked:
		return true
	# Check aliases
	var entry = get_weapon_entry(canonical)
	for alias in entry.get("aliases", []):
		if alias in unlocked:
			return true
	return false

static func unlock_weapon(id: String, save_mgr = null) -> bool:
	if not save_mgr:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root.has_node("SaveManager"):
			save_mgr = tree.root.get_node("SaveManager")
	if not save_mgr:
		return false
		
	var canonical = resolve_weapon_id(id)
	var unlocked = save_mgr.data.get("unlocked_weapons", [])
	if not canonical in unlocked:
		unlocked.append(canonical)
		var entry = get_weapon_entry(canonical)
		for alias in entry.get("aliases", []):
			if not alias in unlocked:
				unlocked.append(alias)
		save_mgr.data["unlocked_weapons"] = unlocked
		save_mgr.save_game()
		return true
	return false

static func get_upgrade_levels(id: String, save_mgr = null) -> Dictionary:
	var defaults = {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
	if not save_mgr:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root.has_node("SaveManager"):
			save_mgr = tree.root.get_node("SaveManager")
	if not save_mgr:
		return defaults
		
	var canonical = resolve_weapon_id(id)
	var upgrades = save_mgr.data.get("weapon_upgrades", {})
	if upgrades.has(canonical):
		var u = upgrades[canonical]
		for k in defaults.keys():
			if not u.has(k):
				u[k] = 0
		return u
	# Check alias
	var entry = get_weapon_entry(canonical)
	for alias in entry.get("aliases", []):
		if upgrades.has(alias):
			var u = upgrades[alias]
			for k in defaults.keys():
				if not u.has(k):
					u[k] = 0
			return u
	return defaults

static func get_upgrade_level(id: String, stat_name: String, save_mgr = null) -> int:
	var lvls = get_upgrade_levels(id, save_mgr)
	return lvls.get(stat_name, 0)

static func get_upgrade_cost(id: String, stat_name: String, save_mgr = null) -> int:
	var cur_lvl = get_upgrade_level(id, stat_name, save_mgr)
	var wdata = get_weapon_data(id)
	if not wdata:
		return -1
	return wdata.get_upgrade_cost(stat_name, cur_lvl)

static func purchase_upgrade(id: String, stat_name: String, save_mgr = null) -> bool:
	if not save_mgr:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root.has_node("SaveManager"):
			save_mgr = tree.root.get_node("SaveManager")
	if not save_mgr:
		return false
		
	var canonical = resolve_weapon_id(id)
	var cost = get_upgrade_cost(canonical, stat_name, save_mgr)
	if cost <= 0 or save_mgr.data.cash < cost:
		return false
		
	var cur_lvl = get_upgrade_level(canonical, stat_name, save_mgr)
	if cur_lvl >= WeaponData.MAX_UPGRADE_LEVEL:
		return false
		
	save_mgr.add_cash(-cost)
	var lvls = get_upgrade_levels(canonical, save_mgr)
	lvls[stat_name] = cur_lvl + 1
	save_mgr.data.weapon_upgrades[canonical] = lvls
	
	# Sync alias
	var entry = get_weapon_entry(canonical)
	for alias in entry.get("aliases", []):
		save_mgr.data.weapon_upgrades[alias] = lvls
		
	save_mgr.save_game()
	return true

static func purchase_weapon(id: String, save_mgr = null) -> bool:
	if not save_mgr:
		var tree = Engine.get_main_loop() as SceneTree
		if tree and tree.root.has_node("SaveManager"):
			save_mgr = tree.root.get_node("SaveManager")
	if not save_mgr:
		return false
		
	var canonical = resolve_weapon_id(id)
	if is_weapon_unlocked(canonical, save_mgr):
		return true
		
	var entry = get_weapon_entry(canonical)
	var price = entry.get("unlock_price", 0)
	if save_mgr.data.cash < price:
		return false
		
	save_mgr.add_cash(-price)
	unlock_weapon(canonical, save_mgr)
	return true
