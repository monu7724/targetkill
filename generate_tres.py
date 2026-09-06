import os

weapons_data = {
    "m4a1": {"name": "M4A1", "dmg": 25.0, "rate": 0.11, "mag": 30, "rel": 2.5, "cost": 1500},
    "ak47": {"name": "AK-47", "dmg": 32.0, "rate": 0.15, "mag": 30, "rel": 2.8, "cost": 1800},
    "scar_l": {"name": "SCAR-L", "dmg": 28.0, "rate": 0.13, "mag": 30, "rel": 2.6, "cost": 2200},
    "g36": {"name": "G36", "dmg": 26.0, "rate": 0.12, "mag": 30, "rel": 2.4, "cost": 2000},
    "famas": {"name": "FAMAS", "dmg": 22.0, "rate": 0.08, "mag": 25, "rel": 3.0, "cost": 2500},
    "aug": {"name": "AUG", "dmg": 27.0, "rate": 0.12, "mag": 30, "rel": 2.5, "cost": 2300},
    "mp5": {"name": "MP5", "dmg": 18.0, "rate": 0.07, "mag": 30, "rel": 2.0, "cost": 1200},
    "spas12": {"name": "SPAS-12", "dmg": 18.0, "rate": 0.8, "mag": 8, "rel": 4.0, "cost": 2800, "pellets": 8, "auto": "false"},
    "svd": {"name": "SVD", "dmg": 85.0, "rate": 0.5, "mag": 10, "rel": 3.5, "cost": 4000, "auto": "false"},
    "m249": {"name": "M249", "dmg": 30.0, "rate": 0.1, "mag": 100, "rel": 5.0, "cost": 5000}
}

out_dir = "/workspaces/targetkill/resources/weapons"
os.makedirs(out_dir, exist_ok=True)

for wid, data in weapons_data.items():
    pellets = data.get("pellets", 1)
    auto = data.get("auto", "true")
    content = f"""[gd_resource type="Resource" script_class="WeaponData" load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/WeaponData.gd" id="1_w3s4d"]

[resource]
script = ExtResource("1_w3s4d")
weapon_id = "{wid}"
display_name = "{data['name']}"
base_damage = {data['dmg']}
headshot_multiplier = 2.0
base_fire_rate = {data['rate']}
base_mag_size = {data['mag']}
base_reserve_ammo = {data['mag'] * 5}
base_reload_time = {data['rel']}
spread = 0.02
recoil = 0.85
range = 120.0
pellet_count = {pellets}
is_automatic = {auto}
muzzle_fx = "rifle"
sound_set = "rifle"
upgrade_cost_damage = {data['cost']}
upgrade_cost_mag = {data['cost']}
upgrade_cost_reload = {data['cost']}
"""
    with open(os.path.join(out_dir, f"{wid}.tres"), "w") as f:
        f.write(content)

print("Generated 10 weapon resources")
