path = "/workspaces/targetkill/scripts/UI/ArmoryUI.gd"
with open(path, "r") as f:
    content = f.read()

import re

old_meshes = re.search(r"var meshes = \{.*?\}", content, re.DOTALL)
if old_meshes:
    new_meshes = """var meshes = {
    "pistol": "res://assets/3d/weapons/pistol.glb",
    "rifle": "res://assets/3d/weapons/rifle.glb",
    "shotgun": "res://assets/3d/weapons/shotgun.glb",
    "m4a1": "res://assets/3d/weapons/rifle.glb",
    "ak47": "res://assets/3d/weapons/rifle.glb",
    "scar_l": "res://assets/3d/weapons/rifle.glb",
    "g36": "res://assets/3d/weapons/rifle.glb",
    "famas": "res://assets/3d/weapons/rifle.glb",
    "aug": "res://assets/3d/weapons/rifle.glb",
    "mp5": "res://assets/3d/weapons/rifle.glb",
    "spas12": "res://assets/3d/weapons/shotgun.glb",
    "svd": "res://assets/3d/weapons/rifle.glb",
    "m249": "res://assets/3d/weapons/rifle.glb"
}"""
    content = content.replace(old_meshes.group(0), new_meshes)
    with open(path, "w") as f:
        f.write(content)
    print("Fixed ArmoryUI.gd meshes")
else:
    print("meshes not found")

