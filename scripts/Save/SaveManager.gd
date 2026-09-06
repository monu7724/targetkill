extends Node

const SAVE_PATH = "user://savegame.json"
const SAVE_TEMP = "user://savegame.json.tmp"
const SAVE_BACKUP = "user://savegame.json.bak"
const SAVE_VERSION = 2

var data = {
	"version": SAVE_VERSION,
	"cash": 0,
	"completed_missions": [],
	"unlocked_weapons": ["pistol", "rifle", "shotgun"],
	"is_first_launch": true,
	"selected_quality": 1, # 0: Low, 1: Medium, 2: High
	"settings": {
		"master_volume": 1.0,
		"music_volume": 0.8,
		"sfx_volume": 1.0,
		"ambience_volume": 0.7,
		"sensitivity": 0.22
	},
	"weapon_upgrades": {
		"pistol": {"damage": 0, "mag": 0, "reload": 0},
		"rifle": {"damage": 0, "mag": 0, "reload": 0},
		"shotgun": {"damage": 0, "mag": 0, "reload": 0}
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
				for w_id in data[key].keys():
					if loaded_data[key].has(w_id):
						data[key][w_id] = loaded_data[key][w_id]
			elif key == "settings" and loaded_data[key] is Dictionary:
				for s_key in data[key].keys():
					if loaded_data[key].has(s_key):
						data[key][s_key] = loaded_data[key][s_key]
			elif typeof(data[key]) == typeof(loaded_data[key]):
				data[key] = loaded_data[key]

func add_cash(amount: int):
	data.cash = max(0, data.cash + amount)
	save_game()
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		event_bus.cash_changed.emit(data.cash)

func complete_mission(mission_id: String):
	if not mission_id in data.completed_missions:
		data.completed_missions.append(mission_id)
		save_game()

func is_mission_completed(mission_id: String) -> bool:
	return mission_id in data.completed_missions
