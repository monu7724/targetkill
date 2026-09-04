extends Node

const SAVE_PATH = "user://savegame.json"
const SAVE_VERSION = 1

var data = {
	"version": SAVE_VERSION,
	"coins": 0,
	"completed_missions": [],
	"unlocked_weapons": ["pistol"],
	"is_first_launch": true,
	"weapon_upgrades": {
		"pistol": {"damage": 0, "mag": 0, "reload": 0},
		"rifle": {"damage": 0, "mag": 0, "reload": 0},
		"shotgun": {"damage": 0, "mag": 0, "reload": 0}
	}
}

func _ready():
	load_game()

func save_game():
	var file = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		var json_string = JSON.stringify(data)
		file.store_string(json_string)
		file.close()
	else:
		printerr("Failed to open save file for writing: ", SAVE_PATH)

func load_game():
	if not FileAccess.file_exists(SAVE_PATH):
		save_game()
		return
		
	var file = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		printerr("Failed to open save file for reading: ", SAVE_PATH)
		return
		
	var json_string = file.get_as_text()
	file.close()
	
	var json = JSON.parse_string(json_string)
	if json is Dictionary and json.has("version"):
		# Merge loaded data with defaults to ensure all fields exist
		_merge_data(json)
		data.version = SAVE_VERSION # Update version if needed
	else:
		printerr("Save file is corrupted or invalid format. Resetting to defaults.")
		save_game()

func _merge_data(loaded_data: Dictionary):
	for key in data.keys():
		if loaded_data.has(key):
			if typeof(data[key]) == typeof(loaded_data[key]):
				if key == "weapon_upgrades":
					# Deep merge for upgrades
					for w_id in data[key].keys():
						if loaded_data[key].has(w_id):
							data[key][w_id] = loaded_data[key][w_id]
				else:
					data[key] = loaded_data[key]

func add_coins(amount: int):
	data.coins = max(0, data.coins + amount)
	save_game()

func complete_mission(mission_id: String):
	if not mission_id in data.completed_missions:
		data.completed_missions.append(mission_id)
		save_game()

func is_mission_completed(mission_id: String) -> bool:
	return mission_id in data.completed_missions
