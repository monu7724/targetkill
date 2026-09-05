import sys
import os
import math
sys.path.append(os.getcwd())
import bpy
from tools.blender.scripts.asset_builder import (
    clear_scene, create_pbr_material, add_box, add_cylinder, add_cone, add_uv_sphere,
    join_objects, export_glb, export_obj
)

def build_normal_zombie():
    print("Building High-Visibility Zombie Variant 1: Normal Infected...")
    clear_scene()
    
    # High-visibility pale rotting flesh, distinct blue shirt, crimson blood, pale bone
    m_skin = create_pbr_material("Mat_ZombieSkin", (0.52, 0.62, 0.48, 1.0), metallic=0.04, roughness=0.65)
    m_shirt = create_pbr_material("Mat_ZombieShirt", (0.42, 0.48, 0.58, 1.0), metallic=0.0, roughness=0.75)
    m_blood = create_pbr_material("Mat_ZombieBlood", (0.85, 0.08, 0.06, 1.0), metallic=0.15, roughness=0.22)
    m_bone = create_pbr_material("Mat_ZombieBone", (0.92, 0.90, 0.82, 1.0), metallic=0.0, roughness=0.45)
    m_pants = create_pbr_material("Mat_ZombiePants", (0.28, 0.34, 0.45, 1.0), metallic=0.0, roughness=0.78)
    m_boot = create_pbr_material("Mat_ZombieBoot", (0.18, 0.16, 0.15, 1.0), metallic=0.1, roughness=0.70)
    m_eyes = create_pbr_material("Mat_ZombieEyes", (0.95, 0.20, 0.10, 1.0), metallic=0.0, roughness=0.2, emission=(0.95, 0.20, 0.10, 1.0), emission_strength=3.5)
    
    parts = []
    # Head & Jaw
    parts.append(add_box("Head_Cranium", (0, 1.62, 0.04), (0.19, 0.22, 0.19), m_skin))
    parts.append(add_box("Head_Jaw", (0, 1.53, 0.12), (0.13, 0.07, 0.10), m_skin))
    parts.append(add_box("Head_Teeth", (0, 1.55, 0.14), (0.10, 0.03, 0.02), m_bone))
    # Glowing bloodshot eye sockets so the head is always identifiable
    parts.append(add_uv_sphere("Head_Eye_L", (-0.05, 1.63, 0.13), 0.022, m_eyes))
    parts.append(add_uv_sphere("Head_Eye_R", (0.05, 1.63, 0.13), 0.022, m_eyes))
    
    # Torso & wounds
    parts.append(add_box("Torso_Main", (0, 1.25, 0), (0.32, 0.44, 0.20), m_shirt))
    parts.append(add_box("Torso_Wound", (0.06, 1.28, 0.09), (0.12, 0.16, 0.04), m_blood))
    parts.append(add_box("Torso_Rib1", (0.06, 1.32, 0.11), (0.10, 0.02, 0.02), m_bone))
    parts.append(add_box("Torso_Rib2", (0.06, 1.26, 0.11), (0.10, 0.02, 0.02), m_bone))
    
    # Arms
    parts.append(add_cylinder("Arm_Upper_L", (-0.22, 1.30, 0.10), 0.052, 0.28, rotation=(math.radians(75), 0, 0), material=m_shirt))
    parts.append(add_cylinder("Arm_Fore_L", (-0.22, 1.26, 0.32), 0.042, 0.26, rotation=(math.radians(85), 0, 0), material=m_skin))
    parts.append(add_box("Arm_Hand_L", (-0.22, 1.25, 0.46), (0.055, 0.065, 0.08), m_skin))
    parts.append(add_box("Claws_L", (-0.22, 1.25, 0.51), (0.05, 0.02, 0.03), m_bone))
    
    parts.append(add_cylinder("Arm_Upper_R", (0.22, 1.26, 0.08), 0.052, 0.26, rotation=(math.radians(65), 0, 0), material=m_shirt))
    parts.append(add_cylinder("Arm_Fore_R", (0.22, 1.20, 0.28), 0.042, 0.24, rotation=(math.radians(75), 0, 0), material=m_skin))
    parts.append(add_box("Arm_Hand_R", (0.22, 1.18, 0.40), (0.055, 0.065, 0.08), m_skin))
    parts.append(add_box("Claws_R", (0.22, 1.18, 0.45), (0.05, 0.02, 0.03), m_bone))
    
    # Pelvis & Legs
    parts.append(add_box("Pelvis", (0, 0.96, 0), (0.29, 0.16, 0.18), m_pants))
    parts.append(add_cylinder("Leg_Thigh_L", (-0.10, 0.70, 0), 0.072, 0.42, material=m_pants))
    parts.append(add_box("Leg_KneeWound_L", (-0.10, 0.50, 0.06), (0.08, 0.08, 0.03), m_blood))
    parts.append(add_box("Leg_KneeBone_L", (-0.10, 0.50, 0.07), (0.05, 0.05, 0.02), m_bone))
    parts.append(add_cylinder("Leg_Shin_L", (-0.10, 0.28, 0), 0.062, 0.40, material=m_pants))
    parts.append(add_box("Leg_Foot_L", (-0.10, 0.06, 0.03), (0.10, 0.10, 0.22), m_boot))
    
    parts.append(add_cylinder("Leg_Thigh_R", (0.10, 0.70, 0), 0.072, 0.42, material=m_pants))
    parts.append(add_cylinder("Leg_Shin_R", (0.10, 0.28, 0), 0.062, 0.40, material=m_skin))
    parts.append(add_box("Leg_Foot_R", (0.10, 0.06, 0.03), (0.10, 0.10, 0.22), m_boot))
    
    zombie_obj = join_objects(parts, "Zombie_Normal")
    export_obj('models/zombies/zombie_normal.obj')
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Zombie_Rig"
    zombie_obj.parent = arm_obj
    export_glb('assets/3d/zombies/zombie_normal.glb', 'tools/blender/generated/zombie_normal.blend')

def build_fast_zombie():
    print("Building High-Visibility Zombie Variant 2: Fast Runner...")
    clear_scene()
    
    m_skin = create_pbr_material("Mat_ZombieFastSkin", (0.58, 0.68, 0.52, 1.0), metallic=0.05, roughness=0.55)
    m_blood = create_pbr_material("Mat_ZombieBlood", (0.85, 0.08, 0.06, 1.0), metallic=0.15, roughness=0.22)
    m_bone = create_pbr_material("Mat_ZombieBone", (0.92, 0.90, 0.82, 1.0), metallic=0.0, roughness=0.45)
    m_torn = create_pbr_material("Mat_FastTornClothes", (0.50, 0.28, 0.20, 1.0), metallic=0.0, roughness=0.80)
    m_eye = create_pbr_material("Mat_FeralEye", (1.0, 0.92, 0.15, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.92, 0.15, 1.0), emission_strength=5.0)
    
    parts = []
    # Hunched head & gaping maw
    parts.append(add_box("Head_Cranium", (0, 1.48, 0.18), (0.17, 0.19, 0.18), m_skin))
    parts.append(add_box("Head_JawOpen", (0, 1.38, 0.26), (0.12, 0.09, 0.12), m_blood))
    parts.append(add_box("FeralTeeth", (0, 1.40, 0.28), (0.10, 0.04, 0.03), m_bone))
    parts.append(add_uv_sphere("Eye_L", (-0.05, 1.50, 0.26), 0.022, m_eye))
    parts.append(add_uv_sphere("Eye_R", (0.05, 1.50, 0.26), 0.022, m_eye))
    
    # Lean, sprint-angled torso
    parts.append(add_box("Torso_Leaned", (0, 1.18, 0.08), (0.26, 0.42, 0.17), m_torn))
    parts.append(add_box("Spine_Bones", (0, 1.20, 0.0), (0.04, 0.36, 0.04), m_bone))
    
    # Elongated running arms with claw fingers
    parts.append(add_cylinder("Arm_L_Upper", (-0.19, 1.22, 0.18), 0.042, 0.32, rotation=(math.radians(95), math.radians(-15), 0), material=m_skin))
    parts.append(add_cylinder("Arm_L_Fore", (-0.24, 1.18, 0.45), 0.034, 0.30, rotation=(math.radians(105), 0, 0), material=m_skin))
    parts.append(add_box("Claws_L", (-0.24, 1.15, 0.62), (0.07, 0.02, 0.10), m_bone))
    
    parts.append(add_cylinder("Arm_R_Upper", (0.19, 1.20, -0.05), 0.042, 0.32, rotation=(math.radians(35), math.radians(15), 0), material=m_skin))
    parts.append(add_cylinder("Arm_R_Fore", (0.24, 1.10, -0.25), 0.034, 0.30, rotation=(math.radians(20), 0, 0), material=m_skin))
    parts.append(add_box("Claws_R", (0.24, 1.05, -0.40), (0.07, 0.02, 0.10), m_bone))
    
    # High-speed sprint legs
    parts.append(add_box("Pelvis", (0, 0.90, 0.04), (0.24, 0.14, 0.16), m_torn))
    parts.append(add_cylinder("Leg_L_Thigh", (-0.09, 0.70, 0.15), 0.058, 0.42, rotation=(math.radians(35), 0, 0), material=m_torn))
    parts.append(add_cylinder("Leg_L_Shin", (-0.09, 0.34, 0.26), 0.048, 0.44, rotation=(math.radians(-25), 0, 0), material=m_skin))
    parts.append(add_box("Leg_L_Foot", (-0.09, 0.08, 0.32), (0.08, 0.07, 0.20), m_skin))
    parts.append(add_cylinder("Leg_R_Thigh", (0.09, 0.68, -0.15), 0.058, 0.42, rotation=(math.radians(-40), 0, 0), material=m_torn))
    parts.append(add_cylinder("Leg_R_Shin", (0.09, 0.32, -0.32), 0.048, 0.44, rotation=(math.radians(45), 0, 0), material=m_skin))
    parts.append(add_box("Leg_R_Foot", (0.09, 0.06, -0.44), (0.08, 0.07, 0.18), m_skin))
    
    fast_obj = join_objects(parts, "Zombie_Fast")
    export_obj('models/zombies/zombie_fast.obj')
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Fast_Rig"
    fast_obj.parent = arm_obj
    export_glb('assets/3d/zombies/zombie_fast.glb', 'tools/blender/generated/zombie_fast.blend')

def build_heavy_zombie():
    print("Building High-Visibility Zombie Variant 3: Heavy / Brute...")
    clear_scene()
    
    m_skin = create_pbr_material("Mat_BruteSkin", (0.46, 0.54, 0.44, 1.0), metallic=0.06, roughness=0.68)
    m_armor = create_pbr_material("Mat_BruteArmor", (0.28, 0.32, 0.36, 1.0), metallic=0.65, roughness=0.40)
    m_metal_spike = create_pbr_material("Mat_RebarSpike", (0.65, 0.55, 0.45, 1.0), metallic=0.85, roughness=0.40)
    m_blood = create_pbr_material("Mat_DarkBlood", (0.85, 0.08, 0.06, 1.0), metallic=0.12, roughness=0.25)
    m_plate = create_pbr_material("Mat_ArmoredPlates", (0.35, 0.38, 0.42, 1.0), metallic=0.55, roughness=0.48)
    m_eyes = create_pbr_material("Mat_BruteEyes", (1.0, 0.4, 0.1, 1.0), metallic=0.0, roughness=0.2, emission=(1.0, 0.4, 0.1, 1.0), emission_strength=4.0)
    
    parts = []
    # Bulky heavy skull with metal plate bolted into forehead
    parts.append(add_box("Head_Massive", (0, 1.76, 0.05), (0.26, 0.28, 0.26), m_skin))
    parts.append(add_box("Forehead_Armor", (0, 1.84, 0.16), (0.22, 0.10, 0.06), m_armor))
    parts.append(add_cylinder("Head_Spike", (0.06, 1.88, 0.17), 0.012, 0.10, rotation=(math.radians(45), 0, 0), material=m_metal_spike))
    parts.append(add_box("Jaw_Crusher", (0, 1.62, 0.14), (0.20, 0.12, 0.15), m_skin))
    parts.append(add_uv_sphere("Eye_Brute", (-0.06, 1.76, 0.17), 0.024, m_eyes))
    
    # Huge muscular torso with swat armor vest
    parts.append(add_box("Torso_Giant", (0, 1.34, 0), (0.54, 0.56, 0.34), m_skin))
    parts.append(add_box("Armor_Chest_Vest", (0, 1.36, 0.08), (0.48, 0.44, 0.24), m_armor))
    parts.append(add_box("Armor_Back_Plate", (0, 1.36, -0.10), (0.48, 0.44, 0.16), m_armor))
    
    # Massive mutated Right Arm with embedded steel rebar club
    parts.append(add_cylinder("Arm_R_Huge_Upper", (0.38, 1.36, 0.05), 0.12, 0.36, rotation=(math.radians(35), 0, 0), material=m_skin))
    parts.append(add_cylinder("Arm_R_Huge_Fore", (0.44, 1.15, 0.26), 0.14, 0.42, rotation=(math.radians(65), 0, 0), material=m_skin))
    parts.append(add_box("Arm_R_Fist_Club", (0.48, 1.00, 0.48), (0.24, 0.24, 0.26), m_plate))
    parts.append(add_cylinder("Spike_1", (0.50, 1.08, 0.58), 0.018, 0.32, rotation=(math.radians(75), 0, 0), material=m_metal_spike))
    parts.append(add_cylinder("Spike_2", (0.44, 0.94, 0.56), 0.018, 0.28, rotation=(math.radians(60), 0, 0), material=m_metal_spike))
    
    # Left Arm
    parts.append(add_cylinder("Arm_L_Upper", (-0.34, 1.34, 0.02), 0.09, 0.34, rotation=(math.radians(45), 0, 0), material=m_skin))
    parts.append(add_box("Shoulder_Pauldrons", (-0.36, 1.48, 0.02), (0.22, 0.18, 0.24), m_armor))
    parts.append(add_cylinder("Arm_L_Fore", (-0.36, 1.15, 0.22), 0.08, 0.36, rotation=(math.radians(65), 0, 0), material=m_skin))
    parts.append(add_box("Arm_L_Fist", (-0.36, 1.02, 0.38), (0.16, 0.16, 0.18), m_skin))
    
    # Legs
    parts.append(add_box("Pelvis_Broad", (0, 0.98, 0), (0.44, 0.22, 0.28), m_plate))
    parts.append(add_cylinder("Leg_L_Thigh", (-0.16, 0.68, 0), 0.12, 0.46, material=m_armor))
    parts.append(add_cylinder("Leg_L_Shin", (-0.16, 0.28, 0), 0.11, 0.44, material=m_plate))
    parts.append(add_box("Leg_L_Boot", (-0.16, 0.08, 0.04), (0.18, 0.16, 0.30), m_armor))
    
    parts.append(add_cylinder("Leg_R_Thigh", (0.16, 0.68, 0), 0.12, 0.46, material=m_armor))
    parts.append(add_cylinder("Leg_R_Shin", (0.16, 0.28, 0), 0.11, 0.44, material=m_plate))
    parts.append(add_box("Leg_R_Boot", (0.16, 0.08, 0.04), (0.18, 0.16, 0.30), m_armor))
    
    heavy_obj = join_objects(parts, "Zombie_Heavy")
    export_obj('models/zombies/zombie_heavy.obj')
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Heavy_Rig"
    heavy_obj.parent = arm_obj
    export_glb('assets/3d/zombies/zombie_heavy.glb', 'tools/blender/generated/zombie_heavy.blend')

def build_boss_zombie():
    print("Building High-Visibility Zombie Variant 4: Boss Mutant Alpha...")
    clear_scene()
    
    m_skin = create_pbr_material("Mat_BossFlesh", (0.42, 0.48, 0.44, 1.0), metallic=0.08, roughness=0.60)
    m_veins = create_pbr_material("Mat_BossToxicVeins", (0.15, 1.0, 0.30, 1.0), metallic=0.0, roughness=0.2, emission=(0.15, 1.0, 0.30, 1.0), emission_strength=7.0)
    m_eyes = create_pbr_material("Mat_BossGlowingEyes", (1.0, 0.08, 0.05, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.08, 0.05, 1.0), emission_strength=8.0)
    m_spikes = create_pbr_material("Mat_BossBoneSpikes", (0.90, 0.88, 0.78, 1.0), metallic=0.05, roughness=0.40)
    m_carapace = create_pbr_material("Mat_BossArmorCarapace", (0.24, 0.26, 0.28, 1.0), metallic=0.60, roughness=0.35)
    
    parts = []
    # Dominant Head with twin red glowing ocular clusters and horned crest
    parts.append(add_box("Head_Skull", (0, 2.10, 0.10), (0.32, 0.34, 0.34), m_skin))
    parts.append(add_box("Head_Horn_Crest", (0, 2.30, 0.05), (0.42, 0.12, 0.28), m_carapace))
    # 4 glowing red eyes
    parts.append(add_uv_sphere("Eye_1", (-0.09, 2.12, 0.26), 0.030, m_eyes))
    parts.append(add_uv_sphere("Eye_2", (0.09, 2.12, 0.26), 0.030, m_eyes))
    parts.append(add_uv_sphere("Eye_3", (-0.05, 2.17, 0.25), 0.024, m_eyes))
    parts.append(add_uv_sphere("Eye_4", (0.05, 2.17, 0.25), 0.024, m_eyes))
    parts.append(add_box("Jaw_Alpha", (0, 1.95, 0.20), (0.24, 0.14, 0.20), m_skin))
    parts.append(add_box("Fangs", (0, 1.98, 0.28), (0.20, 0.06, 0.04), m_spikes))
    
    # Gigantic Colossal Torso with glowing bio-luminescent toxic veins
    parts.append(add_box("Torso_Alpha", (0, 1.55, 0), (0.72, 0.74, 0.44), m_skin))
    parts.append(add_box("Carapace_Chest", (0, 1.65, 0.16), (0.64, 0.45, 0.18), m_carapace))
    # Toxic glowing vein lines along chest
    parts.append(add_box("Vein_Core", (0, 1.62, 0.24), (0.14, 0.34, 0.05), m_veins))
    parts.append(add_box("Vein_Branch_L", (-0.18, 1.70, 0.22), (0.24, 0.06, 0.05), m_veins))
    parts.append(add_box("Vein_Branch_R", (0.18, 1.70, 0.22), (0.24, 0.06, 0.05), m_veins))
    
    # Dorsal Spine Spikes
    for i, z_offset in enumerate([-0.18, -0.22, -0.25, -0.22, -0.18]):
        y_pos = 1.85 - i * 0.14
        parts.append(add_cone(f"Spine_Spike_{i}", (0, y_pos, z_offset), 0.06, 0.38, rotation=(math.radians(-45), 0, 0), material=m_spikes))
        parts.append(add_cone(f"Spike_L_{i}", (-0.28, y_pos, z_offset + 0.05), 0.04, 0.28, rotation=(math.radians(-35), math.radians(-30), 0), material=m_spikes))
        parts.append(add_cone(f"Spike_R_{i}", (0.28, y_pos, z_offset + 0.05), 0.04, 0.28, rotation=(math.radians(-35), math.radians(30), 0), material=m_spikes))
        
    # Giant Mutated Alpha Claw (Left Arm)
    parts.append(add_cylinder("Arm_L_Upper", (-0.48, 1.55, 0.08), 0.16, 0.46, rotation=(math.radians(45), 0, 0), material=m_skin))
    parts.append(add_cylinder("Arm_L_Fore", (-0.56, 1.28, 0.38), 0.18, 0.52, rotation=(math.radians(70), 0, 0), material=m_carapace))
    parts.append(add_box("Claw_Base", (-0.60, 1.10, 0.65), (0.28, 0.28, 0.24), m_carapace))
    for idx, x_off in enumerate([-0.70, -0.60, -0.50]):
        parts.append(add_cone(f"Talon_{idx}", (x_off, 1.08, 0.85), 0.045, 0.38, rotation=(math.radians(90), 0, 0), material=m_spikes))
        
    # Right Arm
    parts.append(add_cylinder("Arm_R_Upper", (0.46, 1.55, 0.04), 0.14, 0.44, rotation=(math.radians(40), 0, 0), material=m_skin))
    parts.append(add_cylinder("Arm_R_Fore", (0.52, 1.28, 0.30), 0.14, 0.46, rotation=(math.radians(60), 0, 0), material=m_skin))
    parts.append(add_box("Hand_R", (0.55, 1.12, 0.52), (0.20, 0.20, 0.22), m_carapace))
    parts.append(add_cone("Claw_R_Thumb", (0.55, 1.10, 0.66), 0.035, 0.24, rotation=(math.radians(90), 0, 0), material=m_spikes))
    
    # Legs
    parts.append(add_box("Pelvis_Alpha", (0, 1.12, 0), (0.56, 0.28, 0.36), m_carapace))
    parts.append(add_cylinder("Leg_L_Thigh", (-0.22, 0.78, 0), 0.16, 0.54, material=m_carapace))
    parts.append(add_cylinder("Leg_L_Shin", (-0.22, 0.32, 0), 0.15, 0.50, material=m_skin))
    parts.append(add_box("Leg_L_Stomp", (-0.22, 0.09, 0.05), (0.24, 0.18, 0.36), m_carapace))
    
    parts.append(add_cylinder("Leg_R_Thigh", (0.22, 0.78, 0), 0.16, 0.54, material=m_carapace))
    parts.append(add_cylinder("Leg_R_Shin", (0.22, 0.32, 0), 0.15, 0.50, material=m_skin))
    parts.append(add_box("Leg_R_Stomp", (0.22, 0.09, 0.05), (0.24, 0.18, 0.36), m_carapace))
    
    boss_obj = join_objects(parts, "Zombie_Boss")
    export_obj('models/zombies/zombie_boss.obj')
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Boss_Rig"
    boss_obj.parent = arm_obj
    export_glb('assets/3d/zombies/zombie_boss.glb', 'tools/blender/generated/zombie_boss.blend')

def build_player_soldier():
    print("Building High-Visibility Player Soldier Character...")
    clear_scene()
    
    m_camo = create_pbr_material("Mat_SoldierUniform", (0.34, 0.40, 0.30, 1.0), metallic=0.0, roughness=0.75)
    m_vest = create_pbr_material("Mat_TacticalVest", (0.22, 0.25, 0.24, 1.0), metallic=0.20, roughness=0.60)
    m_helmet = create_pbr_material("Mat_KevlarHelmet", (0.28, 0.32, 0.28, 1.0), metallic=0.25, roughness=0.50)
    m_goggles = create_pbr_material("Mat_TacticalGoggles", (0.10, 0.85, 0.40, 1.0), metallic=0.90, roughness=0.15, emission=(0.10, 0.85, 0.40, 1.0), emission_strength=1.5)
    m_skin = create_pbr_material("Mat_SoldierSkin", (0.84, 0.68, 0.58, 1.0), metallic=0.0, roughness=0.65)
    m_boots = create_pbr_material("Mat_CombatBoots", (0.16, 0.16, 0.18, 1.0), metallic=0.15, roughness=0.70)
    m_pouch = create_pbr_material("Mat_GearPouches", (0.30, 0.34, 0.26, 1.0), metallic=0.05, roughness=0.75)
    
    parts = []
    # Head & Helmet
    parts.append(add_box("Head_Face", (0, 1.62, 0.02), (0.18, 0.20, 0.18), m_skin))
    parts.append(add_box("Helmet_Dome", (0, 1.68, 0), (0.23, 0.18, 0.23), m_helmet))
    parts.append(add_box("Helmet_EarProtectors", (0, 1.62, -0.01), (0.24, 0.12, 0.14), m_helmet))
    parts.append(add_box("NVG_Shroud", (0, 1.70, 0.12), (0.06, 0.06, 0.02), m_vest))
    parts.append(add_box("Ballistic_Goggles", (0, 1.63, 0.10), (0.17, 0.06, 0.04), m_goggles))
    
    # Torso
    parts.append(add_box("Torso_Uniform", (0, 1.25, 0), (0.34, 0.44, 0.22), m_camo))
    parts.append(add_box("PlateCarrier_Front", (0, 1.26, 0.06), (0.30, 0.38, 0.15), m_vest))
    parts.append(add_box("PlateCarrier_Back", (0, 1.26, -0.06), (0.30, 0.38, 0.15), m_vest))
    for mx in [-0.08, 0.0, 0.08]:
        parts.append(add_box(f"Mag_Pouch_{mx}", (mx, 1.20, 0.14), (0.06, 0.14, 0.04), m_pouch))
        
    # Arms
    parts.append(add_cylinder("Arm_L_Upper", (-0.22, 1.30, 0), 0.055, 0.28, material=m_camo))
    parts.append(add_box("ElbowPad_L", (-0.22, 1.15, -0.05), (0.08, 0.08, 0.03), m_vest))
    parts.append(add_cylinder("Arm_L_Fore", (-0.22, 1.00, 0), 0.048, 0.26, material=m_camo))
    parts.append(add_box("Glove_L", (-0.22, 0.84, 0.02), (0.06, 0.10, 0.08), m_vest))
    
    parts.append(add_cylinder("Arm_R_Upper", (0.22, 1.30, 0), 0.055, 0.28, material=m_camo))
    parts.append(add_box("ElbowPad_R", (0.22, 1.15, -0.05), (0.08, 0.08, 0.03), m_vest))
    parts.append(add_cylinder("Arm_R_Fore", (0.22, 1.00, 0), 0.048, 0.26, material=m_camo))
    parts.append(add_box("Glove_R", (0.22, 0.84, 0.02), (0.06, 0.10, 0.08), m_vest))
    
    # Belt & Legs
    parts.append(add_box("Tactical_Belt", (0, 0.98, 0), (0.32, 0.08, 0.22), m_vest))
    parts.append(add_box("Pistol_Holster", (0.18, 0.88, 0.02), (0.08, 0.16, 0.10), m_vest))
    parts.append(add_cylinder("Leg_L_Thigh", (-0.11, 0.70, 0), 0.075, 0.42, material=m_camo))
    parts.append(add_box("KneePad_L", (-0.11, 0.48, 0.07), (0.10, 0.10, 0.03), m_vest))
    parts.append(add_cylinder("Leg_L_Shin", (-0.11, 0.28, 0), 0.068, 0.38, material=m_camo))
    parts.append(add_box("Leg_L_Boot", (-0.11, 0.06, 0.03), (0.11, 0.12, 0.24), m_boots))
    parts.append(add_cylinder("Leg_R_Thigh", (0.11, 0.70, 0), 0.075, 0.42, material=m_camo))
    parts.append(add_box("KneePad_R", (0.11, 0.48, 0.07), (0.10, 0.10, 0.03), m_vest))
    parts.append(add_cylinder("Leg_R_Shin", (0.11, 0.28, 0), 0.068, 0.38, material=m_camo))
    parts.append(add_box("Leg_R_Boot", (0.11, 0.06, 0.03), (0.11, 0.12, 0.24), m_boots))
    
    soldier_obj = join_objects(parts, "Player_Soldier")
    export_obj('models/player/player_soldier.obj')
    
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Soldier_Rig"
    soldier_obj.parent = arm_obj
    export_glb('assets/3d/characters/player_soldier.glb', 'tools/blender/generated/player_soldier.blend')

def build_fps_arms():
    print("Building High-Visibility First-Person FPS Arms...")
    clear_scene()
    
    m_sleeve = create_pbr_material("Mat_TacticalSleeve", (0.34, 0.40, 0.30, 1.0), metallic=0.0, roughness=0.75)
    m_skin = create_pbr_material("Mat_ArmSkin", (0.84, 0.68, 0.58, 1.0), metallic=0.0, roughness=0.60)
    m_glove = create_pbr_material("Mat_TacticalGlove", (0.26, 0.28, 0.32, 1.0), metallic=0.20, roughness=0.60)
    m_knuckle = create_pbr_material("Mat_CarbonKnuckle", (0.55, 0.58, 0.62, 1.0), metallic=0.85, roughness=0.25)
    m_watch = create_pbr_material("Mat_TacticalWatch", (0.20, 0.22, 0.25, 1.0), metallic=0.75, roughness=0.35)
    m_screen = create_pbr_material("Mat_WatchScreen", (0.20, 0.90, 0.60, 1.0), metallic=0.0, roughness=0.2, emission=(0.20, 0.90, 0.60, 1.0), emission_strength=4.0)
    
    parts = []
    # Left Arm & Hand in weapon support forward angle
    parts.append(add_cylinder("Sleeve_L", (-0.18, 0, 0.15), 0.050, 0.26, rotation=(math.radians(70), math.radians(15), 0), material=m_sleeve))
    parts.append(add_cylinder("Forearm_L", (-0.14, -0.02, -0.06), 0.044, 0.22, rotation=(math.radians(82), math.radians(20), 0), material=m_skin))
    # Tactical watch on left wrist
    parts.append(add_cylinder("Watch_Strap", (-0.11, -0.03, -0.15), 0.046, 0.03, rotation=(math.radians(82), math.radians(20), 0), material=m_watch))
    parts.append(add_box("Watch_Bezel", (-0.11, 0.015, -0.15), (0.034, 0.012, 0.034), m_watch))
    parts.append(add_box("Watch_Screen", (-0.11, 0.022, -0.15), (0.026, 0.005, 0.026), m_screen))
    # Left Hand / Tactical Glove with carbon knuckle guard
    parts.append(add_box("Hand_L", (-0.08, -0.04, -0.25), (0.062, 0.052, 0.10), m_glove))
    parts.append(add_box("Knuckles_L", (-0.08, -0.015, -0.27), (0.058, 0.016, 0.042), m_knuckle))
    
    # Right Arm & Hand in weapon trigger grip angle
    parts.append(add_cylinder("Sleeve_R", (0.18, 0, 0.12), 0.050, 0.26, rotation=(math.radians(65), math.radians(-15), 0), material=m_sleeve))
    parts.append(add_cylinder("Forearm_R", (0.14, -0.03, -0.08), 0.044, 0.22, rotation=(math.radians(78), math.radians(-18), 0), material=m_skin))
    # Right Hand / Tactical Glove holding grip
    parts.append(add_box("Hand_R", (0.10, -0.06, -0.26), (0.062, 0.052, 0.10), m_glove))
    parts.append(add_box("Knuckles_R", (0.10, -0.035, -0.28), (0.058, 0.016, 0.042), m_knuckle))
    # Trigger index finger extended
    parts.append(add_cylinder("Trigger_Finger", (0.07, -0.045, -0.32), 0.011, 0.058, rotation=(math.radians(85), 0, 0), material=m_glove))
    
    fps_arms_obj = join_objects(parts, "FPS_Arms")
    export_obj('models/player/fps_arms.obj')
    
    export_glb('assets/3d/weapons/fps_arms.glb', 'tools/blender/generated/fps_arms.blend')

if __name__ == '__main__':
    build_normal_zombie()
    build_fast_zombie()
    build_heavy_zombie()
    build_boss_zombie()
    build_player_soldier()
    build_fps_arms()
    print("ALL HIGH-VISIBILITY 3D CHARACTERS & FPS ARMS BUILT!")
