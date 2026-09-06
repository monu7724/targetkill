#!/usr/bin/env python3

weapons = [
    {"id": "m4a1", "name": "M4A1 Sentinel", "dmg": 22.0, "hs": 2.0, "fr": 0.11, "mag": 30, "res": 180, "rel": 2.8, "spr": 0.02, "rec": 0.85, "range": 120.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 120, "uc_m": 100, "uc_r": 110},
    {"id": "ak47", "name": "AK-47 Vanguard", "dmg": 28.0, "hs": 2.0, "fr": 0.13, "mag": 30, "res": 150, "rel": 3.1, "spr": 0.035, "rec": 1.2, "range": 100.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 140, "uc_m": 110, "uc_r": 120},
    {"id": "scar_l", "name": "SCAR-L Operator", "dmg": 25.0, "hs": 2.0, "fr": 0.12, "mag": 30, "res": 180, "rel": 2.9, "spr": 0.015, "rec": 0.75, "range": 130.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 130, "uc_m": 105, "uc_r": 115},
    {"id": "g36", "name": "G36 Tactical", "dmg": 23.0, "hs": 2.0, "fr": 0.10, "mag": 30, "res": 210, "rel": 2.7, "spr": 0.025, "rec": 0.8, "range": 110.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 125, "uc_m": 95, "uc_r": 105},
    {"id": "famas", "name": "FAMAS F1", "dmg": 20.0, "hs": 2.0, "fr": 0.08, "mag": 25, "res": 200, "rel": 2.5, "spr": 0.02, "rec": 0.9, "range": 100.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 110, "uc_m": 120, "uc_r": 90},
    {"id": "aug", "name": "AUG A3", "dmg": 24.0, "hs": 2.0, "fr": 0.11, "mag": 30, "res": 180, "rel": 3.0, "spr": 0.018, "rec": 0.7, "range": 140.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 135, "uc_m": 100, "uc_r": 120},
    {"id": "mp5", "name": "MP5 Spec Ops", "dmg": 18.0, "hs": 2.0, "fr": 0.07, "mag": 40, "res": 240, "rel": 2.2, "spr": 0.04, "rec": 0.5, "range": 70.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 100, "uc_m": 90, "uc_r": 80},
    {"id": "spas12", "name": "SPAS-12 Combat", "dmg": 85.0, "hs": 1.8, "fr": 0.7, "mag": 8, "res": 40, "rel": 4.0, "spr": 0.06, "rec": 2.5, "range": 45.0, "pellets": 8, "auto": "false", "fx": "shotgun", "snd": "shotgun", "uc_d": 180, "uc_m": 160, "uc_r": 150},
    {"id": "svd", "name": "SVD Dragunov", "dmg": 95.0, "hs": 3.0, "fr": 0.8, "mag": 10, "res": 50, "rel": 3.5, "spr": 0.005, "rec": 3.0, "range": 300.0, "pellets": 1, "auto": "false", "fx": "rifle", "snd": "rifle", "uc_d": 200, "uc_m": 150, "uc_r": 140},
    {"id": "m249", "name": "M249 SAW", "dmg": 26.0, "hs": 2.0, "fr": 0.09, "mag": 100, "res": 300, "rel": 5.5, "spr": 0.05, "rec": 1.5, "range": 150.0, "pellets": 1, "auto": "true", "fx": "rifle", "snd": "rifle", "uc_d": 160, "uc_m": 250, "uc_r": 200},
]

TEMPLATE = '''[gd_resource type="Resource" script_class="WeaponData" load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/WeaponData.gd" id="1_w3s4d"]

[resource]
script = ExtResource("1_w3s4d")
weapon_id = "{id}"
display_name = "{name}"
base_damage = {dmg}
headshot_multiplier = {hs}
base_fire_rate = {fr}
base_mag_size = {mag}
base_reserve_ammo = {res}
base_reload_time = {rel}
spread = {spr}
recoil = {rec}
range = {range}
pellet_count = {pellets}
is_automatic = {auto}
muzzle_fx = "{fx}"
sound_set = "{snd}"
upgrade_cost_damage = {uc_d}
upgrade_cost_mag = {uc_m}
upgrade_cost_reload = {uc_r}
'''

import os
for w in weapons:
    path = f"/workspaces/targetkill/resources/weapons/{w['id']}.tres"
    with open(path, "w") as f:
        f.write(TEMPLATE.format(**w))
    print(f"Created {path}")

print("Done")
