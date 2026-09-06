#!/usr/bin/env python3
"""Create all 12 mission .tres files for the campaign."""

missions = [
    {
        "id": "mission_01", "name": "First Contact", 
        "desc": "Reports of infected civilians at the airport terminal. Eliminate all hostiles and secure the concourse.",
        "obj_type": 0, "target": 15, "waves": 3, "cash": 500,
        "scene": "res://scenes/environments/AirportTerminal.tscn",
        "location": "Airport Terminal - Concourse A", "stars": 1,
        "loadout": "USP-45 Tactical", "unlock": "",
        "spawn": '[{"type": "normal", "weight": 0.7}, {"type": "fast", "weight": 0.3}]'
    },
    {
        "id": "mission_02", "name": "Feral Pack",
        "desc": "The infection has spread to animals. Packs of infected dogs roam the airport service road. Neutralize the threat.",
        "obj_type": 0, "target": 18, "waves": 3, "cash": 750,
        "scene": "res://scenes/environments/UrbanStreet.tscn",
        "location": "Airport Service Road - Gate 7", "stars": 1,
        "loadout": "USP-45 Tactical / M4A1 Sentinel", "unlock": "mission_01",
        "spawn": '[{"type": "dog", "weight": 1.0}]'
    },
    {
        "id": "mission_03", "name": "Crossfire",
        "desc": "Mixed infected at the railway station. Zombies and dogs attack from multiple platforms. Hold your ground.",
        "obj_type": 0, "target": 22, "waves": 3, "cash": 1000,
        "scene": "res://scenes/environments/RailwayStation.tscn",
        "location": "Railway Station - Platform 3", "stars": 2,
        "loadout": "M4A1 Sentinel", "unlock": "mission_02",
        "spawn": '[{"type": "normal", "weight": 0.5}, {"type": "dog", "weight": 0.5}]'
    },
    {
        "id": "mission_04", "name": "Rat King",
        "desc": "The abandoned train yard is overrun with infected animals. Dogs and rats swarm from every direction.",
        "obj_type": 1, "target": 0, "waves": 3, "cash": 1250,
        "scene": "res://scenes/environments/AbandonedTrain.tscn",
        "location": "Abandoned Train Yard - Track 9", "stars": 2,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_03",
        "spawn": '[{"type": "dog", "weight": 0.6}, {"type": "fast", "weight": 0.4}]'
    },
    {
        "id": "mission_05", "name": "Containment Breach",
        "desc": "The industrial zone perimeter has collapsed. Mixed infected flooding through. Eliminate all threats.",
        "obj_type": 0, "target": 30, "waves": 3, "cash": 1500,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Industrial Zone - Sector 4", "stars": 3,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_04",
        "spawn": '[{"type": "normal", "weight": 0.4}, {"type": "fast", "weight": 0.3}, {"type": "dog", "weight": 0.3}]'
    },
    {
        "id": "mission_06", "name": "Patient Zero",
        "desc": "The abandoned hospital harbors special infected. Spitters and heavy variants detected. Proceed with caution.",
        "obj_type": 0, "target": 25, "waves": 3, "cash": 1800,
        "scene": "res://scenes/environments/RailwayStation.tscn",
        "location": "Abandoned Hospital - Ward C", "stars": 3,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_05",
        "spawn": '[{"type": "normal", "weight": 0.4}, {"type": "heavy", "weight": 0.3}, {"type": "spitter", "weight": 0.3}]'
    },
    {
        "id": "mission_07", "name": "Dead Mall",
        "desc": "The shopping district is crawling with infected. Dogs hunt in packs through the metro corridors.",
        "obj_type": 0, "target": 30, "waves": 3, "cash": 2100,
        "scene": "res://scenes/environments/UrbanStreet.tscn",
        "location": "Metro Shopping Center - Level B2", "stars": 4,
        "loadout": "Remington 870 / M4A1 Sentinel", "unlock": "mission_06",
        "spawn": '[{"type": "normal", "weight": 0.3}, {"type": "fast", "weight": 0.3}, {"type": "dog", "weight": 0.4}]'
    },
    {
        "id": "mission_08", "name": "Blackout",
        "desc": "Night has fallen. Mixed infected emerge from the darkness. Visibility is critical. Survive all waves.",
        "obj_type": 1, "target": 0, "waves": 3, "cash": 2500,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Night City Street - Block 12", "stars": 4,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_07",
        "spawn": '[{"type": "normal", "weight": 0.25}, {"type": "fast", "weight": 0.25}, {"type": "heavy", "weight": 0.25}, {"type": "dog", "weight": 0.25}]'
    },
    {
        "id": "mission_09", "name": "Fortified",
        "desc": "The military checkpoint has been overrun. Heavy infected and attack dogs patrol the ruins.",
        "obj_type": 0, "target": 35, "waves": 3, "cash": 3000,
        "scene": "res://scenes/environments/AirportTerminal.tscn",
        "location": "Military Checkpoint - Sector Alpha", "stars": 4,
        "loadout": "Remington 870 / Heavy Weapons", "unlock": "mission_08",
        "spawn": '[{"type": "heavy", "weight": 0.5}, {"type": "dog", "weight": 0.5}]'
    },
    {
        "id": "mission_10", "name": "Mutation",
        "desc": "Chemical contamination has accelerated mutations. Mutated infected with enhanced abilities detected.",
        "obj_type": 0, "target": 30, "waves": 3, "cash": 3500,
        "scene": "res://scenes/environments/AbandonedTrain.tscn",
        "location": "Chemical Facility - Reactor Core", "stars": 5,
        "loadout": "Heavy Weapons / Remington 870", "unlock": "mission_09",
        "spawn": '[{"type": "normal", "weight": 0.3}, {"type": "heavy", "weight": 0.4}, {"type": "spitter", "weight": 0.3}]'
    },
    {
        "id": "mission_11", "name": "Overrun",
        "desc": "The construction site is the last barrier before the quarantine zone. Maximum infected density. Survive.",
        "obj_type": 1, "target": 0, "waves": 3, "cash": 4000,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Construction Site - Floor 14", "stars": 5,
        "loadout": "Full Arsenal Recommended", "unlock": "mission_10",
        "spawn": '[{"type": "heavy", "weight": 0.3}, {"type": "fast", "weight": 0.2}, {"type": "dog", "weight": 0.2}, {"type": "spitter", "weight": 0.3}]'
    },
    {
        "id": "mission_12", "name": "Lockdown",
        "desc": "The quarantine zone. All major infected types converge. Eliminate the Alpha to end the outbreak.",
        "obj_type": 2, "target": 1, "waves": 3, "cash": 6000,
        "scene": "res://scenes/environments/FinalLockdown.tscn",
        "location": "Quarantine Zone - Sector Zero", "stars": 5,
        "loadout": "Full Arsenal Required", "unlock": "mission_11",
        "spawn": '[{"type": "normal", "weight": 0.2}, {"type": "fast", "weight": 0.15}, {"type": "heavy", "weight": 0.2}, {"type": "dog", "weight": 0.15}, {"type": "spitter", "weight": 0.15}, {"type": "boss", "weight": 0.15}]'
    },
]

TEMPLATE = '''[gd_resource type="Resource" script_class="MissionData" load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/MissionData.gd" id="1_m1s2d"]

[resource]
script = ExtResource("1_m1s2d")
mission_id = "{id}"
display_name = "{name}"
description = "{desc}"
objective_type = {obj_type}
target_count = {target}
wave_count = {waves}
reward_cash = {cash}
scene_path = "{scene}"
location_name = "{location}"
difficulty_stars = {stars}
recommended_loadout = "{loadout}"
unlock_requirement_id = "{unlock}"
spawn_config = {spawn}
'''

import os
out_dir = "/workspaces/targetkill/resources/missions"
os.makedirs(out_dir, exist_ok=True)

for m in missions:
    path = os.path.join(out_dir, f"{m['id']}.tres")
    content = TEMPLATE.format(**m)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

print(f"\nTotal: {len(missions)} missions created")
