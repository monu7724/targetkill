extends Node

enum State {
	BOOT,
	MAIN_MENU,
	MISSION_SELECT,
	MISSION_INTRO,
	LOADING,
	GAMEPLAY,
	PAUSED,
	MISSION_COMPLETE,
	MISSION_FAILED,
	UPGRADES,
	SETTINGS
}

signal state_changed(old_state: State, new_state: State)
signal pause_toggled(is_paused: bool)

var current_state: State = State.BOOT
var previous_state: State = State.BOOT

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS

func change_state(new_state: State) -> bool:
	if current_state == new_state:
		return false
		
	# Prevent invalid transitions (e.g. pausing when mission is over)
	if new_state == State.PAUSED:
		if current_state != State.GAMEPLAY:
			print("[GameStateManager] Cannot pause outside of GAMEPLAY state. Current state: ", state_to_string(current_state))
			return false
	
	var old_state = current_state
	previous_state = old_state
	current_state = new_state
	
	print("[GameStateManager] State transition: ", state_to_string(old_state), " -> ", state_to_string(new_state))
	
	# Handle pause tree state
	if new_state == State.PAUSED:
		get_tree().paused = true
		pause_toggled.emit(true)
	elif old_state == State.PAUSED and new_state == State.GAMEPLAY:
		get_tree().paused = false
		pause_toggled.emit(false)
	elif new_state in [State.MISSION_COMPLETE, State.MISSION_FAILED]:
		# Ensure physics is halted or controlled when mission ends
		get_tree().paused = false
	
	state_changed.emit(old_state, new_state)
	return true

func pause_game() -> bool:
	if current_state == State.GAMEPLAY:
		return change_state(State.PAUSED)
	return false

func resume_game() -> bool:
	if current_state == State.PAUSED:
		return change_state(State.GAMEPLAY)
	return false

func toggle_pause() -> bool:
	if current_state == State.GAMEPLAY:
		return pause_game()
	elif current_state == State.PAUSED:
		return resume_game()
	return false

func is_paused() -> bool:
	return current_state == State.PAUSED

func is_gameplay_active() -> bool:
	return current_state == State.GAMEPLAY

func state_to_string(state: State) -> String:
	match state:
		State.BOOT: return "BOOT"
		State.MAIN_MENU: return "MAIN_MENU"
		State.MISSION_SELECT: return "MISSION_SELECT"
		State.MISSION_INTRO: return "MISSION_INTRO"
		State.LOADING: return "LOADING"
		State.GAMEPLAY: return "GAMEPLAY"
		State.PAUSED: return "PAUSED"
		State.MISSION_COMPLETE: return "MISSION_COMPLETE"
		State.MISSION_FAILED: return "MISSION_FAILED"
		State.UPGRADES: return "UPGRADES"
		State.SETTINGS: return "SETTINGS"
		_: return "UNKNOWN"
