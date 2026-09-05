extends Node

var master_volume: float = 1.0
var music_volume: float = 0.8
var sfx_volume: float = 1.0
var ambience_volume: float = 0.7

var sounds = {
	"ui_click": preload("res://audio/ui/sfx_ui_click.wav"),
	"victory": preload("res://audio/ui/sfx_victory.wav"),
	"defeat": preload("res://audio/ui/sfx_defeat.wav"),
	"footstep": preload("res://audio/player/sfx_footstep.wav"),
	"ambience_airport": preload("res://audio/ambience/sfx_ambience_airport.wav"),
	"ambience_metro": preload("res://audio/ambience/sfx_ambience_metro.wav")
}

var bg_player: AudioStreamPlayer = null

func _ready():
	apply_volumes()
	bg_player = AudioStreamPlayer.new()
	bg_player.bus = "Master"
	add_child(bg_player)

func play_sfx(sound_name: String):
	if sounds.has(sound_name):
		var p = AudioStreamPlayer.new()
		p.stream = sounds[sound_name]
		p.bus = "Master"
		add_child(p)
		p.finished.connect(func(): p.queue_free())
		p.play()

func play_ui_click():
	play_sfx("ui_click")

func play_victory():
	play_sfx("victory")

func play_defeat():
	play_sfx("defeat")

func play_ambience(stream_path: String):
	if bg_player:
		var s = load(stream_path)
		if s:
			bg_player.stream = s
			bg_player.play()

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

func apply_volumes():
	set_master_volume(master_volume)
	set_music_volume(music_volume)
	set_sfx_volume(sfx_volume)
	set_ambience_volume(ambience_volume)
