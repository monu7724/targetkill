path = "/workspaces/targetkill/scenes/player/Player.gd"
with open(path, "r") as f:
    content = f.read()

import re

old_configs_match = re.search(r"var weapon_configs = \[.*?\]\n", content, re.DOTALL)
if old_configs_match:
    new_configs = """var weapon_configs = [
	{"id": "pistol", "path": "res://resources/weapons/pistol.tres", "model": "res://assets/3d/weapons/pistol.glb"},
	{"id": "rifle", "path": "res://resources/weapons/rifle.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "shotgun", "path": "res://resources/weapons/shotgun.tres", "model": "res://assets/3d/weapons/shotgun.glb"},
	{"id": "m4a1", "path": "res://resources/weapons/m4a1.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "ak47", "path": "res://resources/weapons/ak47.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "scar_l", "path": "res://resources/weapons/scar_l.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "g36", "path": "res://resources/weapons/g36.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "famas", "path": "res://resources/weapons/famas.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "aug", "path": "res://resources/weapons/aug.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "mp5", "path": "res://resources/weapons/mp5.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "spas12", "path": "res://resources/weapons/spas12.tres", "model": "res://assets/3d/weapons/shotgun.glb"},
	{"id": "svd", "path": "res://resources/weapons/svd.tres", "model": "res://assets/3d/weapons/rifle.glb"},
	{"id": "m249", "path": "res://resources/weapons/m249.tres", "model": "res://assets/3d/weapons/rifle.glb"}
]
"""
    content = content.replace(old_configs_match.group(0), new_configs)
    
    # Wait, there's a hardcoded list in _init_weapons for test/old weapons too.
    # Let's remove the heavy weapons loop
    heavy_loop = """	# Add the 10 heavy weapons to the possible list so we can find them
	var ids = ["m134", "rpg7", "rpd", "mg42", "l86", "m249", "pkm", "m60", "m2browning", "flamethrower"]
	for wid in ids:
		all_possible_weapons.append({"id": "heavy_"+wid, "path": "res://resources/weapons/heavy_"+wid+".tres", "model": "res://assets/3d/weapons/rifle.glb"})"""
    if heavy_loop in content:
        content = content.replace(heavy_loop, "")
    else:
        print("heavy loop not found")

    with open(path, "w") as f:
        f.write(content)
    print("Fixed Player.gd weapon configs")
else:
    print("weapon_configs not found")
