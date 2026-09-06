extends Node

const SAVE_PATH = "user://savegame.json"
const SAVE_TEMP = "user://savegame.json.tmp"
const SAVE_BACKUP = "user://savegame.json.bak"
const SAVE_VERSION = 2

var data = {
	"version": SAVE_VERSION,
	"cash": 0,
	"completed_missions": [],
	"unlocked_weapons": ["pistol", "rifle", "shotgun", "usp45", "m4a1", "remington870"],
	"is_first_launch": true,
	"selected_quality": 1, # 0: Low, 1: Medium, 2: High
	"settings": {
		"master_volume": 1.0,
		"music_volume": 0.8,
		"sfx_volume": 1.0,
		"ambience_volume": 0.7,
		"sensitivity": 0.22,
		"aim_sensitivity": 0.16,
		"invert_y": false
	},
	"weapon_upgrades": {
		"pistol": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"usp45": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"rifle": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"m4a1": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"shotgun": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"remington870": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"ak47": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"desert_eagle": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"mp5": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"awp": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"combat_knife": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"crossbow": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0},
		"grenade_launcher": {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
	}
}

func _ready():
	var t0 = Time.get_ticks_msec()
	load_game()
	print("[%d ms] [BOOT:01] SaveManager initialized in %d ms (Cash: %d, Completed: %s)" % [Time.get_ticks_msec(), Time.get_ticks_msec() - t0, data.cash, str(data.completed_missions)])

func save_game():
	# Atomic Save Process: Write to .tmp first, then atomically replace
	var file = FileAccess.open(SAVE_TEMP, FileAccess.WRITE)
	if not file:
		printerr("[SaveManager Error] Cannot open temp save file: ", SAVE_TEMP)
		return
		
	data.version = SAVE_VERSION
	var json_string = JSON.stringify(data, "\t")
	file.store_string(json_string)
	file.flush()
	file.close()
	
	# Create backup of current valid save
	if FileAccess.file_exists(SAVE_PATH):
		DirAccess.copy_absolute(SAVE_PATH, SAVE_BACKUP)
		
	# Replace main save with temp
	var err = DirAccess.rename_absolute(SAVE_TEMP, SAVE_PATH)
	if err != OK:
		# Fallback if rename across filesystems fails
		DirAccess.copy_absolute(SAVE_TEMP, SAVE_PATH)
		DirAccess.remove_absolute(SAVE_TEMP)

func load_game():
	if not FileAccess.file_exists(SAVE_PATH):
		if FileAccess.file_exists(SAVE_BACKUP):
			_load_from_path(SAVE_BACKUP)
		else:
			save_game()
		return
		
	if not _load_from_path(SAVE_PATH):
		if FileAccess.file_exists(SAVE_BACKUP):
			print("[SaveManager] Main save corrupted. Recovering from backup...")
			_load_from_path(SAVE_BACKUP)
		else:
			printerr("[SaveManager] Save corrupted. Resetting to defaults.")
			save_game()

func _load_from_path(path: String) -> bool:
	var file = FileAccess.open(path, FileAccess.READ)
	if not file:
		return false
		
	var json_string = file.get_as_text()
	file.close()
	
	var json = JSON.parse_string(json_string)
	if json is Dictionary and json.has("version"):
		_merge_data(json)
		return true
	return false

func _merge_data(loaded_data: Dictionary):
	for key in data.keys():
		if loaded_data.has(key):
			if key in ["cash", "version", "selected_quality"]:
				data[key] = int(loaded_data[key])
			elif key == "weapon_upgrades" and loaded_data[key] is Dictionary:
				for w_id in loaded_data[key].keys():
					if not data[key].has(w_id):
						data[key][w_id] = {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
					var stats = loaded_data[key][w_id]
					if stats is Dictionary:
						for s in stats.keys():
							data[key][w_id][s] = int(stats[s])
			elif key == "settings" and loaded_data[key] is Dictionary:
				for s_key in data[key].keys():
					if loaded_data[key].has(s_key):
						data[key][s_key] = loaded_data[key][s_key]
			elif typeof(data[key]) == typeof(loaded_data[key]):
				data[key] = loaded_data[key]

func add_cash(amount: int):
	data.cash = max(0, data.cash + amount)
	save_game()
	if is_inside_tree():
		var event_bus = get_node_or_null("/root/EventBus")
		if event_bus:
			event_bus.cash_changed.emit(data.cash)

func complete_mission(mission_id: String):
	if not mission_id in data.completed_missions:
		data.completed_missions.append(mission_id)
		save_game()

func is_mission_completed(mission_id: String) -> bool:
	return mission_id in data.completed_missions

func is_weapon_unlocked(weapon_id: String) -> bool:
	var unlocked = data.get("unlocked_weapons", [])
	if weapon_id in unlocked:
		return true
	match weapon_id:
		"usp45": return "pistol" in unlocked
		"pistol": return "usp45" in unlocked
		"m4a1": return "rifle" in unlocked
		"rifle": return "m4a1" in unlocked
		"remington870": return "shotgun" in unlocked
		"shotgun": return "remington870" in unlocked
		"deagle": return "desert_eagle" in unlocked
		"knife": return "combat_knife" in unlocked
		"m79": return "grenade_launcher" in unlocked
	return false

func unlock_weapon(weapon_id: String) -> bool:
	var unlocked = data.get("unlocked_weapons", [])
	var changed = false
	if not weapon_id in unlocked:
		unlocked.append(weapon_id)
		changed = true
	var alias = ""
	match weapon_id:
		"usp45": alias = "pistol"
		"pistol": alias = "usp45"
		"m4a1": alias = "rifle"
		"rifle": alias = "m4a1"
		"remington870": alias = "shotgun"
		"shotgun": alias = "remington870"
		"desert_eagle": alias = "deagle"
		"deagle": alias = "desert_eagle"
		"combat_knife": alias = "knife"
		"knife": alias = "combat_knife"
		"grenade_launcher": alias = "m79"
		"m79": alias = "grenade_launcher"
	if alias != "" and not alias in unlocked:
		unlocked.append(alias)
		changed = true
	if changed:
		data["unlocked_weapons"] = unlocked
		save_game()
	return changed

func get_weapon_upgrade(weapon_id: String, stat_name: String) -> int:
	var upgrades = data.get("weapon_upgrades", {})
	var w = upgrades.get(weapon_id, {})
	if w.is_empty():
		match weapon_id:
			"usp45": w = upgrades.get("pistol", {})
			"pistol": w = upgrades.get("usp45", {})
			"m4a1": w = upgrades.get("rifle", {})
			"rifle": w = upgrades.get("m4a1", {})
			"remington870": w = upgrades.get("shotgun", {})
			"shotgun": w = upgrades.get("remington870", {})
	return w.get(stat_name, 0)

func set_weapon_upgrade(weapon_id: String, stat_name: String, level: int):
	var upgrades = data.get("weapon_upgrades", {})
	if not upgrades.has(weapon_id):
		upgrades[weapon_id] = {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
	upgrades[weapon_id][stat_name] = level
	var alias = ""
	match weapon_id:
		"usp45": alias = "pistol"
		"pistol": alias = "usp45"
		"m4a1": alias = "rifle"
		"rifle": alias = "m4a1"
		"remington870": alias = "shotgun"
		"shotgun": alias = "remington870"
	if alias != "":
		if not upgrades.has(alias):
			upgrades[alias] = {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
		upgrades[alias][stat_name] = level
	save_game()

func upgrade_weapon(weapon_id: String, stat_name: String, cost: int) -> bool:
	if data.cash < cost:
		return false
	var cur_lvl = get_weapon_upgrade(weapon_id, stat_name)
	add_cash(-cost)
	set_weapon_upgrade(weapon_id, stat_name, cur_lvl + 1)
	return true
