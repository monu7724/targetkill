import sys

path = "/workspaces/targetkill/scenes/player/Player.gd"
with open(path, "r", encoding="utf-8") as f: content = f.read()

# Fix unlocked_weapons logic: If SaveManager is not found or weapons empty, default to pistol, rifle, shotgun
content = content.replace('var unlocked_ids = save_mgr.data.unlocked_weapons if save_mgr else ["pistol"]', 
'var unlocked_ids = save_mgr.data.unlocked_weapons if save_mgr and save_mgr.data.has("unlocked_weapons") else ["pistol", "rifle", "shotgun"]')

# Also fix move_speed back to 4.8
content = content.replace('@export var move_speed: float = 0.0', '@export var move_speed: float = 4.8')

with open(path, "w", encoding="utf-8") as f: f.write(content)
print("Fixed scenes/player/Player.gd for tests")
