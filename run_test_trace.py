import sys

unlocked = ["pistol", "rifle", "shotgun"]

weapon_configs = [
	{"id": "pistol", "path": "res://resources/weapons/pistol.tres", "model": "res://assets/3d/weapons/pistol.glb"},
	{"id": "rifle", "path": "res://resources/weapons/rifle.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "shotgun", "path": "res://resources/weapons/shotgun.tres", "model": "res://assets/3d/weapons/shotgun.glb"},
	{"id": "heavy_gun", "path": "res://resources/weapons/heavy_gun.tres", "model": "res://assets/3d/weapons/rifle.glb"}
]
all_possible_weapons = list(weapon_configs)
ids = ["m134", "rpg7", "rpd", "mg42", "l86", "m249", "pkm", "m60", "m2browning", "flamethrower"]
for wid in ids:
    all_possible_weapons.append({"id": "heavy_"+wid})

loaded = []
for cfg in all_possible_weapons:
    if cfg["id"] not in unlocked:
        continue
    loaded.append(cfg["id"])
print(loaded)
