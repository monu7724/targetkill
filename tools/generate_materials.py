import os

materials = {
    "mat_weapon.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_weapon_metal.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.85
roughness = 0.35
""",
    "mat_player.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_swat_camo.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.15
roughness = 0.75
""",
    "mat_zombie_normal.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_zombie_normal.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.05
roughness = 0.65
""",
    "mat_zombie_fast.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_zombie_fast.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.05
roughness = 0.60
""",
    "mat_zombie_heavy.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_zombie_heavy.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.35
roughness = 0.50
""",
    "mat_zombie_boss.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_zombie_boss.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.25
roughness = 0.40
emission_enabled = true
emission = Color(0.8, 0.15, 0.02, 1)
emission_energy_multiplier = 1.2
""",
    "mat_airport_floor.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_airport_tile.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.10
roughness = 0.25
uv1_scale = Vector3(4, 4, 1)
""",
    "mat_station_platform.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_station_concrete.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.05
roughness = 0.85
uv1_scale = Vector3(2, 4, 1)
""",
    "mat_train.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_train_metal.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.70
roughness = 0.35
""",
    "mat_industrial_road.tres": """[gd_resource type="StandardMaterial3D" load_steps=2 format=3]
[ext_resource type="Texture2D" path="res://textures/pbr/tex_industrial_asphalt.png" id="1_tex"]
[resource]
albedo_texture = ExtResource("1_tex")
metallic = 0.05
roughness = 0.90
uv1_scale = Vector3(4, 4, 1)
"""
}

for fname, content in materials.items():
    path = os.path.join("resources/materials", fname)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Created material: {path}")

