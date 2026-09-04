extends Node

var master_volume: float = 1.0
var music_volume: float = 0.8
var sfx_volume: float = 1.0
var ambience_volume: float = 0.7

func _ready():
	# Ensure buses exist (Master is default, others need to be created in Audio Mixer)
	# For simplicity in this script, we'll just set bus volumes
	apply_volumes()

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
