import json
import os

missions = [
    {
        "m_id": "mission_01", "name": "First Contact", 
        "desc": "Reports of infected civilians at the airport terminal. Eliminate all hostiles and secure the concourse.",
        "obj_type": 0, "target": 15, "waves_count": 3, "cash": 500,
        "scene": "res://scenes/environments/AirportTerminal.tscn",
        "location": "Airport Terminal - Concourse A", "stars": 1,
        "loadout": "USP-45 Tactical", "unlock": "",
        "spawn": [{"type": "normal", "weight": 0.7}, {"type": "fast", "weight": 0.3}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.2}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 2, "spawn_direction": "left", "delay": 1.5}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 1.0}, {"enemy_type": "fast", "count": 2, "spawn_direction": "right", "delay": 1.2}]}
        ]
    },
    {
        "m_id": "mission_02", "name": "Feral Pack",
        "desc": "The infection has spread to animals. Packs of infected dogs roam the airport service road. Neutralize the threat.",
        "obj_type": 0, "target": 32, "waves_count": 3, "cash": 750,
        "scene": "res://scenes/environments/AirportServiceRoad.tscn",
        "location": "Airport Service Road - Gate 7", "stars": 1,
        "loadout": "USP-45 Tactical / M4A1 Sentinel", "unlock": "mission_01",
        "spawn": [{"type": "dog", "weight": 1.0}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "dog", "count": 6, "spawn_direction": "front", "delay": 1.2}]},
            {"wave_num": 2, "groups": [{"enemy_type": "dog", "count": 4, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "dog", "count": 4, "spawn_direction": "left", "delay": 1.0}, {"enemy_type": "dog", "count": 4, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 3, "groups": [{"enemy_type": "dog", "count": 5, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "dog", "count": 5, "spawn_direction": "back", "delay": 0.8}, {"enemy_type": "dog", "count": 4, "spawn_direction": "left", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_03", "name": "Crossfire",
        "desc": "Mixed infected at the railway station. Zombies and dogs attack from multiple platforms. Hold your ground.",
        "obj_type": 0, "target": 22, "waves_count": 3, "cash": 1000,
        "scene": "res://scenes/environments/RailwayStation.tscn",
        "location": "Railway Station - Platform 3", "stars": 2,
        "loadout": "M4A1 Sentinel", "unlock": "mission_02",
        "spawn": [{"type": "normal", "weight": 0.5}, {"type": "dog", "weight": 0.5}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "dog", "count": 2, "spawn_direction": "left", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "dog", "count": 4, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 0.9}, {"enemy_type": "dog", "count": 4, "spawn_direction": "front", "delay": 0.9}]}
        ]
    },
    {
        "m_id": "mission_04", "name": "Rat King",
        "desc": "The abandoned train yard is overrun with infected animals. Dogs and rats swarm from every direction.",
        "obj_type": 1, "target": 0, "waves_count": 3, "cash": 1250,
        "scene": "res://scenes/environments/AbandonedTrain.tscn",
        "location": "Abandoned Train Yard - Track 9", "stars": 2,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_03",
        "spawn": [{"type": "dog", "weight": 0.6}, {"type": "fast", "weight": 0.4}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "dog", "count": 5, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 3, "spawn_direction": "back", "delay": 1.2}]},
            {"wave_num": 2, "groups": [{"enemy_type": "dog", "count": 6, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "fast", "count": 6, "spawn_direction": "back", "delay": 0.9}]},
            {"wave_num": 3, "groups": [{"enemy_type": "dog", "count": 8, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "fast", "count": 6, "spawn_direction": "back", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_05", "name": "Containment Breach",
        "desc": "The industrial zone perimeter has collapsed. Mixed infected flooding through. Eliminate all threats.",
        "obj_type": 0, "target": 30, "waves_count": 3, "cash": 1500,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Industrial Zone - Sector 4", "stars": 3,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_04",
        "spawn": [{"type": "normal", "weight": 0.4}, {"type": "fast", "weight": 0.3}, {"type": "dog", "weight": 0.3}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 2, "spawn_direction": "left", "delay": 1.2}, {"enemy_type": "dog", "count": 2, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 1.0}, {"enemy_type": "fast", "count": 3, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "dog", "count": 3, "spawn_direction": "left", "delay": 1.0}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "fast", "count": 4, "spawn_direction": "back", "delay": 0.8}, {"enemy_type": "dog", "count": 4, "spawn_direction": "right", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_06", "name": "Patient Zero",
        "desc": "The abandoned hospital harbors special infected. Spitters and heavy variants detected. Proceed with caution.",
        "obj_type": 0, "target": 25, "waves_count": 3, "cash": 1800,
        "scene": "res://scenes/environments/RailwayStation.tscn",
        "location": "Abandoned Hospital - Ward C", "stars": 3,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_05",
        "spawn": [{"type": "normal", "weight": 0.4}, {"type": "heavy", "weight": 0.3}, {"type": "spitter", "weight": 0.3}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "spitter", "count": 2, "spawn_direction": "left", "delay": 1.5}, {"enemy_type": "heavy", "count": 1, "spawn_direction": "front", "delay": 2.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 1.0}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "right", "delay": 1.2}, {"enemy_type": "heavy", "count": 2, "spawn_direction": "front", "delay": 1.8}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "left", "delay": 1.0}, {"enemy_type": "heavy", "count": 3, "spawn_direction": "back", "delay": 1.5}]}
        ]
    },
    {
        "m_id": "mission_07", "name": "Dead Mall",
        "desc": "The shopping district is crawling with infected. Dogs hunt in packs through the metro corridors.",
        "obj_type": 0, "target": 30, "waves_count": 3, "cash": 2100,
        "scene": "res://scenes/environments/UrbanStreet.tscn",
        "location": "Metro Shopping Center - Level B2", "stars": 4,
        "loadout": "Remington 870 / M4A1 Sentinel", "unlock": "mission_06",
        "spawn": [{"type": "normal", "weight": 0.3}, {"type": "fast", "weight": 0.3}, {"type": "dog", "weight": 0.4}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 2, "spawn_direction": "left", "delay": 1.2}, {"enemy_type": "dog", "count": 2, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 1.0}, {"enemy_type": "fast", "count": 3, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "dog", "count": 3, "spawn_direction": "left", "delay": 0.9}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "fast", "count": 4, "spawn_direction": "right", "delay": 0.8}, {"enemy_type": "dog", "count": 4, "spawn_direction": "back", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_08", "name": "Blackout",
        "desc": "Night has fallen. Mixed infected emerge from the darkness. Visibility is critical. Survive all waves.",
        "obj_type": 1, "target": 0, "waves_count": 3, "cash": 2500,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Night City Street - Block 12", "stars": 4,
        "loadout": "M4A1 Sentinel / Remington 870", "unlock": "mission_07",
        "spawn": [{"type": "normal", "weight": 0.25}, {"type": "fast", "weight": 0.25}, {"type": "heavy", "weight": 0.25}, {"type": "dog", "weight": 0.25}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 3, "spawn_direction": "left", "delay": 1.0}, {"enemy_type": "heavy", "count": 2, "spawn_direction": "front", "delay": 1.5}, {"enemy_type": "dog", "count": 2, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "back", "delay": 0.9}, {"enemy_type": "fast", "count": 4, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "heavy", "count": 3, "spawn_direction": "back", "delay": 1.4}, {"enemy_type": "dog", "count": 3, "spawn_direction": "left", "delay": 0.9}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "fast", "count": 5, "spawn_direction": "right", "delay": 0.8}, {"enemy_type": "heavy", "count": 5, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "dog", "count": 4, "spawn_direction": "back", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_09", "name": "Fortified",
        "desc": "The military checkpoint has been overrun. Heavy infected and attack dogs patrol the ruins.",
        "obj_type": 0, "target": 35, "waves_count": 3, "cash": 3000,
        "scene": "res://scenes/environments/AirportTerminal.tscn",
        "location": "Military Checkpoint - Sector Alpha", "stars": 4,
        "loadout": "Remington 870 / Heavy Weapons", "unlock": "mission_08",
        "spawn": [{"type": "heavy", "weight": 0.5}, {"type": "dog", "weight": 0.5}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "heavy", "count": 5, "spawn_direction": "front", "delay": 1.5}, {"enemy_type": "dog", "count": 5, "spawn_direction": "left", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "heavy", "count": 6, "spawn_direction": "back", "delay": 1.4}, {"enemy_type": "dog", "count": 6, "spawn_direction": "right", "delay": 0.9}]},
            {"wave_num": 3, "groups": [{"enemy_type": "heavy", "count": 7, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "dog", "count": 6, "spawn_direction": "back", "delay": 0.8}]}
        ]
    },
    {
        "m_id": "mission_10", "name": "Mutation",
        "desc": "Chemical contamination has accelerated mutations. Mutated infected with enhanced abilities detected.",
        "obj_type": 0, "target": 30, "waves_count": 3, "cash": 3500,
        "scene": "res://scenes/environments/AbandonedTrain.tscn",
        "location": "Chemical Facility - Reactor Core", "stars": 5,
        "loadout": "Heavy Weapons / Remington 870", "unlock": "mission_09",
        "spawn": [{"type": "normal", "weight": 0.3}, {"type": "heavy", "weight": 0.4}, {"type": "spitter", "weight": 0.3}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "heavy", "count": 3, "spawn_direction": "front", "delay": 1.5}, {"enemy_type": "spitter", "count": 2, "spawn_direction": "back", "delay": 1.2}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "back", "delay": 0.9}, {"enemy_type": "heavy", "count": 4, "spawn_direction": "front", "delay": 1.4}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "left", "delay": 1.1}]},
            {"wave_num": 3, "groups": [{"enemy_type": "normal", "count": 4, "spawn_direction": "front", "delay": 0.8}, {"enemy_type": "heavy", "count": 5, "spawn_direction": "back", "delay": 1.2}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "right", "delay": 1.0}]}
        ]
    },
    {
        "m_id": "mission_11", "name": "Overrun",
        "desc": "The construction site is the last barrier before the quarantine zone. Maximum infected density. Survive.",
        "obj_type": 1, "target": 0, "waves_count": 3, "cash": 4000,
        "scene": "res://scenes/environments/DarkIndustrial.tscn",
        "location": "Construction Site - Floor 14", "stars": 5,
        "loadout": "Full Arsenal Recommended", "unlock": "mission_10",
        "spawn": [{"type": "heavy", "weight": 0.3}, {"type": "fast", "weight": 0.2}, {"type": "dog", "weight": 0.2}, {"type": "spitter", "weight": 0.3}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "heavy", "count": 4, "spawn_direction": "front", "delay": 1.5}, {"enemy_type": "fast", "count": 3, "spawn_direction": "left", "delay": 1.0}, {"enemy_type": "dog", "count": 2, "spawn_direction": "right", "delay": 1.0}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "front", "delay": 1.2}]},
            {"wave_num": 2, "groups": [{"enemy_type": "heavy", "count": 5, "spawn_direction": "back", "delay": 1.4}, {"enemy_type": "fast", "count": 4, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "dog", "count": 3, "spawn_direction": "left", "delay": 0.9}, {"enemy_type": "spitter", "count": 4, "spawn_direction": "back", "delay": 1.1}]},
            {"wave_num": 3, "groups": [{"enemy_type": "heavy", "count": 6, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "fast", "count": 5, "spawn_direction": "right", "delay": 0.8}, {"enemy_type": "dog", "count": 4, "spawn_direction": "back", "delay": 0.8}, {"enemy_type": "spitter", "count": 5, "spawn_direction": "left", "delay": 1.0}]}
        ]
    },
    {
        "m_id": "mission_12", "name": "Lockdown",
        "desc": "The quarantine zone. All major infected types converge. Eliminate the Alpha to end the outbreak.",
        "obj_type": 2, "target": 1, "waves_count": 3, "cash": 6000,
        "scene": "res://scenes/environments/FinalLockdown.tscn",
        "location": "Quarantine Zone - Sector Zero", "stars": 5,
        "loadout": "Full Arsenal Required", "unlock": "mission_11",
        "spawn": [{"type": "normal", "weight": 0.2}, {"type": "fast", "weight": 0.15}, {"type": "heavy", "weight": 0.2}, {"type": "dog", "weight": 0.15}, {"type": "spitter", "weight": 0.15}, {"type": "boss", "weight": 0.15}],
        "waves": [
            {"wave_num": 1, "groups": [{"enemy_type": "normal", "count": 2, "spawn_direction": "front", "delay": 1.0}, {"enemy_type": "fast", "count": 2, "spawn_direction": "left", "delay": 1.0}, {"enemy_type": "heavy", "count": 2, "spawn_direction": "front", "delay": 1.5}, {"enemy_type": "dog", "count": 2, "spawn_direction": "right", "delay": 1.0}]},
            {"wave_num": 2, "groups": [{"enemy_type": "normal", "count": 3, "spawn_direction": "back", "delay": 0.9}, {"enemy_type": "fast", "count": 3, "spawn_direction": "front", "delay": 0.9}, {"enemy_type": "heavy", "count": 3, "spawn_direction": "back", "delay": 1.4}, {"enemy_type": "spitter", "count": 3, "spawn_direction": "left", "delay": 1.2}]},
            {"wave_num": 3, "groups": [{"enemy_type": "heavy", "count": 5, "spawn_direction": "front", "delay": 1.2}, {"enemy_type": "boss", "count": 1, "spawn_direction": "front", "delay": 2.0}]}
        ]
    }
]

out_dir = "/workspaces/targetkill/resources/missions"
for m in missions:
    m_id = m["m_id"]
    name = m["name"]
    desc = m["desc"]
    obj_type = m["obj_type"]
    target = m["target"]
    waves_count = m["waves_count"]
    cash = m["cash"]
    scene = m["scene"]
    location = m["location"]
    stars = m["stars"]
    loadout = m["loadout"]
    unlock = m["unlock"]
    spawn_json = json.dumps(m["spawn"])
    waves_json = json.dumps(m["waves"])

    content = f"""[gd_resource type="Resource" script_class="MissionData" load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/MissionData.gd" id="1_m1s2d"]

[resource]
script = ExtResource("1_m1s2d")
mission_id = "{m_id}"
display_name = "{name}"
description = "{desc}"
objective_type = {obj_type}
target_count = {target}
wave_count = {waves_count}
reward_cash = {cash}
scene_path = "{scene}"
location_name = "{location}"
difficulty_stars = {stars}
recommended_loadout = "{loadout}"
unlock_requirement_id = "{unlock}"
spawn_config = {spawn_json}
waves = {waves_json}
"""
    path = os.path.join(out_dir, f"{m_id}.tres")
    with open(path, "w") as f:
        f.write(content)
    print(f"Wrote {path}")
print("Done writing all 12 mission resources.")
