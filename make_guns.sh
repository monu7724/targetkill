#!/bin/bash
names=("M134 Minigun" "RPG-7 Launcher" "RPD Machine Gun" "MG42 Buzzsaw" "L86 LSW" "M249 SAW" "PKM Light Machine Gun" "M60 General Purpose" "M2 Browning .50 Cal" "Napalm Flamethrower")
ids=("m134" "rpg7" "rpd" "mg42" "l86" "m249" "pkm" "m60" "m2browning" "flamethrower")
damages=(15 450 25 30 22 18 35 40 85 10)
fire_rates=(0.04 4.0 0.09 0.05 0.08 0.08 0.1 0.12 0.2 0.02)
mags=(500 1 100 250 30 100 100 100 200 100)
reloads=(6.0 4.5 4.0 5.0 2.8 4.5 4.8 5.2 6.5 4.0)

for i in {0..9}; do
  cat << TRESEOF > resources/weapons/heavy_${ids[$i]}.tres
[gd_resource type="Resource" script_class="WeaponData" load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/WeaponData.gd" id="1_w3s4d"]

[resource]
script = ExtResource("1_w3s4d")
weapon_id = "heavy_${ids[$i]}"
display_name = "${names[$i]}"
base_damage = ${damages[$i]}.0
headshot_multiplier = 2.0
base_fire_rate = ${fire_rates[$i]}
base_mag_size = ${mags[$i]}
base_reserve_ammo = 1000
base_reload_time = ${reloads[$i]}
spread = 0.05
recoil = 1.5
range = 100.0
pellet_count = 1
is_automatic = true
muzzle_fx = "rifle"
sound_set = "rifle"
upgrade_cost_damage = 500
upgrade_cost_mag = 400
upgrade_cost_reload = 300
TRESEOF
done
