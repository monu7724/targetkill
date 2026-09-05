extends Node

var master_volume: float = 1.0
var music_volume: float = 0.8
var sfx_volume: float = 1.0
var ambience_volume: float = 0.7

var sounds = {
	"ui_click": preload("res://audio/ui/sfx_ui_click.wav"),
	"victory": preload("res://audio/ui/sfx_victory.wav"),
	"defeat": preload("res://audio/ui/sfx_defeat.wav"),
	"footstep": preload("res://audio/player/sfx_footstep.wav")
}

var ambience_paths = {
	"ambience_airport": "res://audio/ambience/sfx_ambience_airport.wav",
	"ambience_metro": "res://audio/ambience/sfx_ambience_metro.wav"
}

var bg_player: AudioStreamPlayer = null
var current_ambience_key: String = ""

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	apply_volumes()
	bg_player = AudioStreamPlayer.new()
	bg_player.bus = "Master"
	add_child(bg_player)
	print("[%d ms] [BOOT:03] AudioManager ready." % Time.get_ticks_msec())

func play_sfx(sound_name: String):
	if sounds.has(sound_name):
		var p = AudioStreamPlayer.new()
		p.stream = sounds[sound_name]
		p.bus = "Master"
		add_child(p)
		p.finished.connect(func(): p.queue_free())
		p.play()

func play_sound_3d(stream: AudioStream, pos: Vector3, max_dist: float = 25.0):
	if not stream: return
	var p = AudioStreamPlayer3D.new()
	p.stream = stream
	p.max_distance = max_dist
	p.global_position = pos
	get_tree().root.add_child(p)
	p.finished.connect(func(): p.queue_free())
	p.play()

func play_ui_click():
	play_sfx("ui_click")

func play_victory():
	play_sfx("victory")
	duck_ambience(0.2, 3.0)

func play_defeat():
	play_sfx("defeat")
	duck_ambience(0.2, 3.0)

func play_ambience(stream_path: String):
	if bg_player:
		var s = load(stream_path)
		if s:
			bg_player.stream = s
			bg_player.volume_db = linear_to_db(ambience_volume)
			bg_player.play()

func play_location_ambience(location_name: String):
	var key = "ambience_airport"
	if "metro" in location_name.to_lower() or "railway" in location_name.to_lower():
		key = "ambience_metro"
	elif "train" in location_name.to_lower():
		key = "ambience_metro"
		
	if current_ambience_key != key and ambience_paths.has(key):
		current_ambience_key = key
		if not bg_player:
			bg_player = AudioStreamPlayer.new()
			bg_player.bus = "Master"
			add_child(bg_player)
		var s = load(ambience_paths[key])
		if s:
			bg_player.stream = s
			bg_player.volume_db = linear_to_db(ambience_volume)
			bg_player.play()

func duck_ambience(factor: float, duration: float):
	if not bg_player: return
	var base_db = linear_to_db(ambience_volume)
	var ducked_db = linear_to_db(ambience_volume * factor)
	var tween = create_tween()
	tween.tween_property(bg_player, "volume_db", ducked_db, 0.2)
	tween.tween_interval(duration)
	tween.tween_property(bg_player, "volume_db", base_db, 0.5)

func set_master_volume(value: float):
	master_volume = clamp(value, 0.0, 1.0)
	AudioServer.set_bus_volume_db(AudioServer.get_bus_index("Master"), linear_to_db(master_volume))

func set_music_volume(value: float):
	music_volume = clamp(value, 0.0, 1.0)
	var idx = AudioServer.get_bus_index("Music")
	if idx != -1:
		AudioServer.set_bus_volume_db(idx, linear_to_db(music_volume))

func set_sfx_volume(value: float):
	sfx_volume = clamp(value, 0.0, 1.0)
	var idx = AudioServer.get_bus_index("SFX")
	if idx != -1:
		AudioServer.set_bus_volume_db(idx, linear_to_db(sfx_volume))

func set_ambience_volume(value: float):
	ambience_volume = clamp(value, 0.0, 1.0)
	var idx = AudioServer.get_bus_index("Ambience")
	if idx != -1:
		AudioServer.set_bus_volume_db(idx, linear_to_db(ambience_volume))
	if bg_player:
		bg_player.volume_db = linear_to_db(ambience_volume)

func apply_volumes():
	set_master_volume(master_volume)
	set_music_volume(music_volume)
	set_sfx_volume(sfx_volume)
	set_ambience_volume(ambience_volume)
