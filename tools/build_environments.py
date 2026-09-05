import os

def create_airport_terminal():
    content = """[gd_scene load_steps=18 format=3 uid="uid://airport001terminal"]

[ext_resource type="PackedScene" path="res://scenes/player/Player.tscn" id="1_p001"]
[ext_resource type="Script" path="res://scripts/GameManager.gd" id="2_g001"]
[ext_resource type="PackedScene" path="res://scenes/zombies/Zombie.tscn" id="3_z001"]
[ext_resource type="Script" path="res://scripts/ImpactPool.gd" id="4_i001"]
[ext_resource type="PackedScene" path="res://scenes/weapons/ImpactEffect.tscn" id="5_ie01"]
[ext_resource type="PackedScene" path="res://scenes/weapons/BloodEffect.tscn" id="6_be01"]
[ext_resource type="PackedScene" path="res://scenes/UI/ResultUI.tscn" id="7_r001"]
[ext_resource type="Material" path="res://resources/materials/mat_airport_floor.tres" id="8_mflr"]
[ext_resource type="ArrayMesh" path="res://models/environment/airport/checkin_counter.obj" id="9_mchk"]
[ext_resource type="ArrayMesh" path="res://models/environment/airport/airport_seats.obj" id="10_mseat"]
[ext_resource type="ArrayMesh" path="res://models/environment/airport/luggage_trolley.obj" id="11_mtrly"]
[ext_resource type="ArrayMesh" path="res://models/environment/airport/terminal_pillar.obj" id="12_mpil"]
[ext_resource type="AudioStream" path="res://audio/ambience/sfx_ambience_airport.wav" id="13_samb"]

[sub_resource type="NavigationMesh" id="NavigationMesh_air"]
vertices = PackedVector3Array(-18, 0, -18, -18, 0, 18, 18, 0, 18, 18, 0, -18)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]

[sub_resource type="BoxShape3D" id="BoxShape3D_flr"]
size = Vector3(36, 0.2, 36)

[sub_resource type="PlaneMesh" id="PlaneMesh_flr"]
size = Vector2(36, 36)

[sub_resource type="Environment" id="Environment_air"]
background_mode = 1
background_color = Color(0.06, 0.08, 0.12, 1)
ambient_light_source = 2
ambient_light_color = Color(0.25, 0.28, 0.35, 1)
ambient_light_energy = 0.6
fog_enabled = true
fog_light_color = Color(0.12, 0.16, 0.22, 1)
fog_density = 0.015

[node name="AirportTerminal" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_air")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866, -0.353, 0.353, 0, 0.707, 0.707, -0.5, -0.612, 0.612, 0, 15, 0)
light_color = Color(0.85, 0.9, 1, 1)
light_energy = 0.55
shadow_enabled = true

[node name="EmergencyLight1" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6, 3.5, -6)
light_color = Color(1, 0.15, 0.1, 1)
light_energy = 2.0
omni_range = 10.0

[node name="EmergencyLight2" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6, 3.5, 6)
light_color = Color(1, 0.15, 0.1, 1)
light_energy = 2.0
omni_range = 10.0

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_air")

[node name="Ground" type="StaticBody3D" parent="NavigationRegion3D"]

[node name="CollisionShape3D" type="CollisionShape3D" parent="NavigationRegion3D/Ground"]
shape = SubResource("BoxShape3D_flr")

[node name="MeshInstance3D" type="MeshInstance3D" parent="NavigationRegion3D/Ground"]
mesh = SubResource("PlaneMesh_flr")
surface_material_override/0 = ExtResource("8_mflr")

[node name="Props" type="Node3D" parent="."]

[node name="Pillar1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6, 0, -6)
mesh = ExtResource("12_mpil")

[node name="Pillar2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0, -6)
mesh = ExtResource("12_mpil")

[node name="Pillar3" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6, 0, 6)
mesh = ExtResource("12_mpil")

[node name="Pillar4" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0, 6)
mesh = ExtResource("12_mpil")

[node name="Counter1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -10)
mesh = ExtResource("9_mchk")

[node name="Counter2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -5, 0, -10)
mesh = ExtResource("9_mchk")

[node name="Seats1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3, 0, 3)
mesh = ExtResource("10_mseat")

[node name="Seats2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0, 3)
mesh = ExtResource("10_mseat")

[node name="LuggageTrolley" type="MeshInstance3D" parent="Props"]
transform = Transform3D(0.866, 0, 0.5, 0, 1, 0, -0.5, 0, 0.866, 2, 0, -2)
mesh = ExtResource("11_mtrly")

[node name="Player" parent="." instance=ExtResource("1_p001")]

[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]
script = ExtResource("2_g001")
zombie_scene = ExtResource("3_z001")
spawn_points = [NodePath("Spawn1"), NodePath("Spawn2"), NodePath("Spawn3")]

[node name="Spawn1" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -11, 0, -11)

[node name="Spawn2" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 11, 0, -11)

[node name="Spawn3" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -13)

[node name="ImpactPool" type="Node3D" parent="." groups=["impact_pool"]]
script = ExtResource("4_i001")
impact_scenes = {
"blood": ExtResource("6_be01"),
"concrete": ExtResource("5_ie01")
}

[node name="ResultUI" parent="." instance=ExtResource("7_r001")]

[node name="AmbiencePlayer" type="AudioStreamPlayer" parent="."]
stream = ExtResource("13_samb")
volume_db = -6.0
autoplay = true
"""
    with open('scenes/environments/AirportTerminal.tscn', 'w') as f:
        f.write(content.strip() + '\n')
    print("Created AirportTerminal.tscn")

def create_dark_industrial():
    content = """[gd_scene load_steps=16 format=3 uid="uid://darkind001street"]

[ext_resource type="PackedScene" path="res://scenes/player/Player.tscn" id="1_p001"]
[ext_resource type="Script" path="res://scripts/GameManager.gd" id="2_g001"]
[ext_resource type="PackedScene" path="res://scenes/zombies/Zombie.tscn" id="3_z001"]
[ext_resource type="Script" path="res://scripts/ImpactPool.gd" id="4_i001"]
[ext_resource type="PackedScene" path="res://scenes/weapons/ImpactEffect.tscn" id="5_ie01"]
[ext_resource type="PackedScene" path="res://scenes/weapons/BloodEffect.tscn" id="6_be01"]
[ext_resource type="PackedScene" path="res://scenes/UI/ResultUI.tscn" id="7_r001"]
[ext_resource type="Material" path="res://resources/materials/mat_industrial_road.tres" id="8_masph"]
[ext_resource type="ArrayMesh" path="res://models/environment/industrial/dumpster.obj" id="9_mdump"]
[ext_resource type="ArrayMesh" path="res://models/environment/industrial/street_lamp.obj" id="10_mlamp"]

[sub_resource type="NavigationMesh" id="NavigationMesh_ind"]
vertices = PackedVector3Array(-20, 0, -20, -20, 0, 20, 20, 0, 20, 20, 0, -20)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]

[sub_resource type="BoxShape3D" id="BoxShape3D_flr"]
size = Vector3(40, 0.2, 40)

[sub_resource type="PlaneMesh" id="PlaneMesh_flr"]
size = Vector2(40, 40)

[sub_resource type="Environment" id="Environment_ind"]
background_mode = 1
background_color = Color(0.04, 0.05, 0.07, 1)
ambient_light_source = 2
ambient_light_color = Color(0.18, 0.20, 0.25, 1)
ambient_light_energy = 0.5
fog_enabled = true
fog_light_color = Color(0.08, 0.10, 0.14, 1)
fog_density = 0.02

[node name="DarkIndustrial" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_ind")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.707, -0.5, 0.5, 0, 0.707, 0.707, -0.707, -0.5, 0.5, 0, 15, 0)
light_color = Color(0.7, 0.8, 0.95, 1)
light_energy = 0.4
shadow_enabled = true

[node name="StreetLight1" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.85, 4.8, -5)
light_color = Color(1, 0.85, 0.5, 1)
light_energy = 3.0
omni_range = 14.0

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_ind")

[node name="Ground" type="StaticBody3D" parent="NavigationRegion3D"]

[node name="CollisionShape3D" type="CollisionShape3D" parent="NavigationRegion3D/Ground"]
shape = SubResource("BoxShape3D_flr")

[node name="MeshInstance3D" type="MeshInstance3D" parent="NavigationRegion3D/Ground"]
mesh = SubResource("PlaneMesh_flr")
surface_material_override/0 = ExtResource("8_masph")

[node name="Props" type="Node3D" parent="."]

[node name="LampPost1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4, 0, -5)
mesh = ExtResource("10_mlamp")

[node name="LampPost2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(-1, 0, 0, 0, 1, 0, 0, 0, -1, -4, 0, 5)
mesh = ExtResource("10_mlamp")

[node name="Dumpster1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(0.966, 0, -0.259, 0, 1, 0, 0.259, 0, 0.966, -5, 0, -6)
mesh = ExtResource("9_mdump")

[node name="Dumpster2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(0.866, 0, 0.5, 0, 1, 0, -0.5, 0, 0.866, 5, 0, 3)
mesh = ExtResource("9_mdump")

[node name="Player" parent="." instance=ExtResource("1_p001")]

[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]
script = ExtResource("2_g001")
zombie_scene = ExtResource("3_z001")
spawn_points = [NodePath("Spawn1"), NodePath("Spawn2"), NodePath("Spawn3")]

[node name="Spawn1" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -12, 0, -12)

[node name="Spawn2" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 12, 0, -12)

[node name="Spawn3" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10, 0, 10)

[node name="ImpactPool" type="Node3D" parent="." groups=["impact_pool"]]
script = ExtResource("4_i001")
impact_scenes = {
"blood": ExtResource("6_be01"),
"concrete": ExtResource("5_ie01")
}

[node name="ResultUI" parent="." instance=ExtResource("7_r001")]
"""
    with open('scenes/environments/DarkIndustrial.tscn', 'w') as f:
        f.write(content.strip() + '\n')
    print("Created DarkIndustrial.tscn")

def create_railway_station():
    content = """[gd_scene load_steps=17 format=3 uid="uid://railway001station"]

[ext_resource type="PackedScene" path="res://scenes/player/Player.tscn" id="1_p001"]
[ext_resource type="Script" path="res://scripts/GameManager.gd" id="2_g001"]
[ext_resource type="PackedScene" path="res://scenes/zombies/Zombie.tscn" id="3_z001"]
[ext_resource type="Script" path="res://scripts/ImpactPool.gd" id="4_i001"]
[ext_resource type="PackedScene" path="res://scenes/weapons/ImpactEffect.tscn" id="5_ie01"]
[ext_resource type="PackedScene" path="res://scenes/weapons/BloodEffect.tscn" id="6_be01"]
[ext_resource type="PackedScene" path="res://scenes/UI/ResultUI.tscn" id="7_r001"]
[ext_resource type="Material" path="res://resources/materials/mat_station_platform.tres" id="8_mplat"]
[ext_resource type="ArrayMesh" path="res://models/environment/station/train_tracks.obj" id="9_mtrk"]
[ext_resource type="ArrayMesh" path="res://models/environment/station/station_bench.obj" id="10_mbch"]
[ext_resource type="AudioStream" path="res://audio/ambience/sfx_ambience_metro.wav" id="11_samb"]

[sub_resource type="NavigationMesh" id="NavigationMesh_stn"]
vertices = PackedVector3Array(-16, 0, -16, -16, 0, 16, 16, 0, 16, 16, 0, -16)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]

[sub_resource type="BoxShape3D" id="BoxShape3D_flr"]
size = Vector3(32, 0.2, 32)

[sub_resource type="PlaneMesh" id="PlaneMesh_flr"]
size = Vector2(32, 32)

[sub_resource type="Environment" id="Environment_stn"]
background_mode = 1
background_color = Color(0.05, 0.06, 0.08, 1)
ambient_light_source = 2
ambient_light_color = Color(0.2, 0.22, 0.28, 1)
ambient_light_energy = 0.55
fog_enabled = true
fog_light_color = Color(0.08, 0.12, 0.16, 1)
fog_density = 0.018

[node name="RailwayStation" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_stn")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866, -0.433, 0.25, 0, 0.5, 0.866, -0.5, -0.75, 0.433, 0, 12, 0)
light_color = Color(0.8, 0.88, 1, 1)
light_energy = 0.45
shadow_enabled = true

[node name="PlatformLight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.5, 0)
light_color = Color(0.9, 0.95, 1, 1)
light_energy = 2.0
omni_range = 14.0

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_stn")

[node name="Ground" type="StaticBody3D" parent="NavigationRegion3D"]

[node name="CollisionShape3D" type="CollisionShape3D" parent="NavigationRegion3D/Ground"]
shape = SubResource("BoxShape3D_flr")

[node name="MeshInstance3D" type="MeshInstance3D" parent="NavigationRegion3D/Ground"]
mesh = SubResource("PlaneMesh_flr")
surface_material_override/0 = ExtResource("8_mplat")

[node name="Props" type="Node3D" parent="."]

[node name="Tracks1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 0, 0)
mesh = ExtResource("9_mtrk")

[node name="Tracks2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 0, -8)
mesh = ExtResource("9_mtrk")

[node name="Bench1" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2, 0, -4)
mesh = ExtResource("10_mbch")

[node name="Bench2" type="MeshInstance3D" parent="Props"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2, 0, 4)
mesh = ExtResource("10_mbch")

[node name="Player" parent="." instance=ExtResource("1_p001")]

[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]
script = ExtResource("2_g001")
zombie_scene = ExtResource("3_z001")
spawn_points = [NodePath("Spawn1"), NodePath("Spawn2")]

[node name="Spawn1" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10, 0, -10)

[node name="Spawn2" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 0, -10)

[node name="ImpactPool" type="Node3D" parent="." groups=["impact_pool"]]
script = ExtResource("4_i001")
impact_scenes = {
"blood": ExtResource("6_be01"),
"concrete": ExtResource("5_ie01")
}

[node name="ResultUI" parent="." instance=ExtResource("7_r001")]

[node name="AmbiencePlayer" type="AudioStreamPlayer" parent="."]
stream = ExtResource("11_samb")
volume_db = -6.0
autoplay = true
"""
    with open('scenes/environments/RailwayStation.tscn', 'w') as f:
        f.write(content.strip() + '\n')
    print("Created RailwayStation.tscn")

def create_abandoned_train():
    content = """[gd_scene load_steps=16 format=3 uid="uid://train001abandoned"]

[ext_resource type="PackedScene" path="res://scenes/player/Player.tscn" id="1_p001"]
[ext_resource type="Script" path="res://scripts/GameManager.gd" id="2_g001"]
[ext_resource type="PackedScene" path="res://scenes/zombies/Zombie.tscn" id="3_z001"]
[ext_resource type="Script" path="res://scripts/ImpactPool.gd" id="4_i001"]
[ext_resource type="PackedScene" path="res://scenes/weapons/ImpactEffect.tscn" id="5_ie01"]
[ext_resource type="PackedScene" path="res://scenes/weapons/BloodEffect.tscn" id="6_be01"]
[ext_resource type="PackedScene" path="res://scenes/UI/ResultUI.tscn" id="7_r001"]
[ext_resource type="Material" path="res://resources/materials/mat_train.tres" id="8_mtrn"]
[ext_resource type="ArrayMesh" path="res://models/environment/train/train_carriage.obj" id="9_mcar"]
[ext_resource type="AudioStream" path="res://audio/ambience/sfx_ambience_metro.wav" id="10_samb"]

[sub_resource type="NavigationMesh" id="NavigationMesh_trn"]
vertices = PackedVector3Array(-12, 0, -14, -12, 0, 14, 12, 0, 14, 12, 0, -14)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]

[sub_resource type="BoxShape3D" id="BoxShape3D_flr"]
size = Vector3(24, 0.2, 28)

[sub_resource type="PlaneMesh" id="PlaneMesh_flr"]
size = Vector2(24, 28)

[sub_resource type="Environment" id="Environment_trn"]
background_mode = 1
background_color = Color(0.04, 0.05, 0.08, 1)
ambient_light_source = 2
ambient_light_color = Color(0.22, 0.22, 0.28, 1)
ambient_light_energy = 0.6
fog_enabled = true
fog_light_color = Color(0.06, 0.08, 0.12, 1)
fog_density = 0.022

[node name="AbandonedTrain" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_trn")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866, -0.353, 0.353, 0, 0.707, 0.707, -0.5, -0.612, 0.612, 0, 12, 0)
light_color = Color(0.75, 0.85, 1, 1)
light_energy = 0.4
shadow_enabled = true

[node name="CabinLight1" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.6, -4)
light_color = Color(1, 0.9, 0.7, 1)
light_energy = 1.8
omni_range = 8.0

[node name="CabinLight2" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.6, 4)
light_color = Color(1, 0.3, 0.2, 1)
light_energy = 1.5
omni_range = 8.0

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_trn")

[node name="Ground" type="StaticBody3D" parent="NavigationRegion3D"]

[node name="CollisionShape3D" type="CollisionShape3D" parent="NavigationRegion3D/Ground"]
shape = SubResource("BoxShape3D_flr")

[node name="MeshInstance3D" type="MeshInstance3D" parent="NavigationRegion3D/Ground"]
mesh = SubResource("PlaneMesh_flr")
surface_material_override/0 = ExtResource("8_mtrn")

[node name="TrainCar" type="MeshInstance3D" parent="."]
mesh = ExtResource("9_mcar")
surface_material_override/0 = ExtResource("8_mtrn")

[node name="Player" parent="." instance=ExtResource("1_p001")]

[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]
script = ExtResource("2_g001")
zombie_scene = ExtResource("3_z001")
spawn_points = [NodePath("SpawnFront"), NodePath("SpawnBack")]

[node name="SpawnFront" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -8)

[node name="SpawnBack" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 8)

[node name="ImpactPool" type="Node3D" parent="." groups=["impact_pool"]]
script = ExtResource("4_i001")
impact_scenes = {
"blood": ExtResource("6_be01"),
"concrete": ExtResource("5_ie01")
}

[node name="ResultUI" parent="." instance=ExtResource("7_r001")]

[node name="AmbiencePlayer" type="AudioStreamPlayer" parent="."]
stream = ExtResource("10_samb")
volume_db = -6.0
autoplay = true
"""
    with open('scenes/environments/AbandonedTrain.tscn', 'w') as f:
        f.write(content.strip() + '\n')
    print("Created AbandonedTrain.tscn")

def create_final_lockdown():
    content = """[gd_scene load_steps=18 format=3 uid="uid://final001lockdown"]

[ext_resource type="PackedScene" path="res://scenes/player/Player.tscn" id="1_p001"]
[ext_resource type="Script" path="res://scripts/GameManager.gd" id="2_g001"]
[ext_resource type="PackedScene" path="res://scenes/zombies/Zombie.tscn" id="3_z001"]
[ext_resource type="Script" path="res://scripts/ImpactPool.gd" id="4_i001"]
[ext_resource type="PackedScene" path="res://scenes/weapons/ImpactEffect.tscn" id="5_ie01"]
[ext_resource type="PackedScene" path="res://scenes/weapons/BloodEffect.tscn" id="6_be01"]
[ext_resource type="PackedScene" path="res://scenes/UI/ResultUI.tscn" id="7_r001"]
[ext_resource type="Material" path="res://resources/materials/mat_airport_floor.tres" id="8_mflr"]
[ext_resource type="ArrayMesh" path="res://models/environment/airport/terminal_pillar.obj" id="9_mpil"]
[ext_resource type="AudioStream" path="res://audio/ambience/sfx_ambience_airport.wav" id="10_samb"]

[sub_resource type="NavigationMesh" id="NavigationMesh_lck"]
vertices = PackedVector3Array(-22, 0, -22, -22, 0, 22, 22, 0, 22, 22, 0, -22)
polygons = [PackedInt32Array(0, 1, 2), PackedInt32Array(0, 2, 3)]

[sub_resource type="BoxShape3D" id="BoxShape3D_flr"]
size = Vector3(44, 0.2, 44)

[sub_resource type="PlaneMesh" id="PlaneMesh_flr"]
size = Vector2(44, 44)

[sub_resource type="Environment" id="Environment_lck"]
background_mode = 1
background_color = Color(0.08, 0.04, 0.04, 1)
ambient_light_source = 2
ambient_light_color = Color(0.35, 0.15, 0.15, 1)
ambient_light_energy = 0.7
fog_enabled = true
fog_light_color = Color(0.25, 0.08, 0.08, 1)
fog_density = 0.02

[node name="FinalLockdown" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_lck")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866, -0.433, 0.25, 0, 0.5, 0.866, -0.5, -0.75, 0.433, 0, 15, 0)
light_color = Color(1, 0.3, 0.2, 1)
light_energy = 0.7
shadow_enabled = true

[node name="AlarmStrobe" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5, 0)
light_color = Color(1, 0.1, 0.05, 1)
light_energy = 3.5
omni_range = 22.0

[node name="NavigationRegion3D" type="NavigationRegion3D" parent="."]
navigation_mesh = SubResource("NavigationMesh_lck")

[node name="Ground" type="StaticBody3D" parent="NavigationRegion3D"]

[node name="CollisionShape3D" type="CollisionShape3D" parent="NavigationRegion3D/Ground"]
shape = SubResource("BoxShape3D_flr")

[node name="MeshInstance3D" type="MeshInstance3D" parent="NavigationRegion3D/Ground"]
mesh = SubResource("PlaneMesh_flr")
surface_material_override/0 = ExtResource("8_mflr")

[node name="ArenaColumns" type="Node3D" parent="."]

[node name="Col1" type="MeshInstance3D" parent="ArenaColumns"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10, 0, -10)
mesh = ExtResource("9_mpil")

[node name="Col2" type="MeshInstance3D" parent="ArenaColumns"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 0, -10)
mesh = ExtResource("9_mpil")

[node name="Col3" type="MeshInstance3D" parent="ArenaColumns"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -10, 0, 10)
mesh = ExtResource("9_mpil")

[node name="Col4" type="MeshInstance3D" parent="ArenaColumns"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 10, 0, 10)
mesh = ExtResource("9_mpil")

[node name="Player" parent="." instance=ExtResource("1_p001")]

[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]
script = ExtResource("2_g001")
zombie_scene = ExtResource("3_z001")
spawn_points = [NodePath("BossSpawn")]

[node name="BossSpawn" type="Node3D" parent="ZombieSpawner"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -12)

[node name="ImpactPool" type="Node3D" parent="." groups=["impact_pool"]]
script = ExtResource("4_i001")
impact_scenes = {
"blood": ExtResource("6_be01"),
"concrete": ExtResource("5_ie01")
}

[node name="ResultUI" parent="." instance=ExtResource("7_r001")]

[node name="AmbiencePlayer" type="AudioStreamPlayer" parent="."]
stream = ExtResource("10_samb")
volume_db = -4.0
autoplay = true
"""
    with open('scenes/environments/FinalLockdown.tscn', 'w') as f:
        f.write(content.strip() + '\n')
    print("Created FinalLockdown.tscn")

if __name__ == '__main__':
    create_airport_terminal()
    create_dark_industrial()
    create_railway_station()
    create_abandoned_train()
    create_final_lockdown()
