extends Resource

class_name WaveData

@export var wave_num: int = 1
@export var groups: Array = [] # Array of Dictionaries: {"enemy_type":String, "count":int, "spawn_direction":String, "delay":float}

func _init(_wave_num:=1, _groups:=[]):
    wave_num = _wave_num
    groups = _groups
