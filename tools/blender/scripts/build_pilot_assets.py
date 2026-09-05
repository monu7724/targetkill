import sys
import os
import math
sys.path.append(os.getcwd())
import bpy
from tools.blender.scripts.asset_builder import (
    clear_scene, create_pbr_material, add_box, add_cylinder, add_cone, add_uv_sphere,
    join_objects, export_glb
)

def build_pilot_zombie():
    print("Building Pilot Asset 1: Realistic Normal Zombie...")
    clear_scene()
    
    # Materials
    m_skin = create_pbr_material("Mat_ZombieSkin", (0.35, 0.44, 0.32, 1.0), metallic=0.05, roughness=0.68)
    m_shirt = create_pbr_material("Mat_ZombieShirt", (0.15, 0.17, 0.22, 1.0), metallic=0.0, roughness=0.88)
    m_blood = create_pbr_material("Mat_ZombieBlood", (0.35, 0.03, 0.02, 1.0), metallic=0.2, roughness=0.30)
    m_bone = create_pbr_material("Mat_ZombieBone", (0.75, 0.72, 0.62, 1.0), metallic=0.0, roughness=0.55)
    m_pants = create_pbr_material("Mat_ZombiePants", (0.12, 0.18, 0.28, 1.0), metallic=0.0, roughness=0.82)
    m_boot = create_pbr_material("Mat_ZombieBoot", (0.05, 0.05, 0.06, 1.0), metallic=0.1, roughness=0.75)
    
    parts = []
    
    # Head & Jaw
    parts.append(add_box("Head_Cranium", (0, 1.62, 0.04), (0.19, 0.22, 0.19), m_skin))
    parts.append(add_box("Head_Jaw", (0, 1.53, 0.12), (0.13, 0.07, 0.10), m_skin))
    parts.append(add_box("Head_Teeth", (0, 1.55, 0.14), (0.10, 0.03, 0.02), m_bone))
    parts.append(add_box("Head_EyeSocket_L", (-0.05, 1.63, 0.13), (0.04, 0.04, 0.03), m_blood))
    parts.append(add_box("Head_EyeSocket_R", (0.05, 1.63, 0.13), (0.04, 0.04, 0.03), m_blood))
    
    # Torso with torn shirt & exposed ribs
    parts.append(add_box("Torso_Main", (0, 1.25, 0), (0.32, 0.44, 0.20), m_shirt))
    parts.append(add_box("Torso_Wound", (0.06, 1.28, 0.09), (0.12, 0.16, 0.04), m_blood))
    parts.append(add_box("Torso_Rib1", (0.06, 1.32, 0.11), (0.10, 0.02, 0.02), m_bone))
    parts.append(add_box("Torso_Rib2", (0.06, 1.26, 0.11), (0.10, 0.02, 0.02), m_bone))
    
    # Left Arm (Reaching forward)
    parts.append(add_cylinder("Arm_Upper_L", (-0.22, 1.30, 0.10), 0.052, 0.28, rotation=(math.radians(75), 0, 0), material=m_shirt))
    parts.append(add_cylinder("Arm_Fore_L", (-0.22, 1.26, 0.32), 0.042, 0.26, rotation=(math.radians(85), 0, 0), material=m_skin))
    parts.append(add_box("Arm_Hand_L", (-0.22, 1.25, 0.46), (0.055, 0.065, 0.08), m_skin))
    parts.append(add_box("Claws_L", (-0.22, 1.25, 0.51), (0.05, 0.02, 0.03), m_bone))
    
    # Right Arm (Asymmetrical reaching forward)
    parts.append(add_cylinder("Arm_Upper_R", (0.22, 1.26, 0.08), 0.052, 0.26, rotation=(math.radians(65), 0, 0), material=m_shirt))
    parts.append(add_cylinder("Arm_Fore_R", (0.22, 1.20, 0.28), 0.042, 0.24, rotation=(math.radians(75), 0, 0), material=m_skin))
    parts.append(add_box("Arm_Hand_R", (0.22, 1.18, 0.40), (0.055, 0.065, 0.08), m_skin))
    parts.append(add_box("Claws_R", (0.22, 1.18, 0.45), (0.05, 0.02, 0.03), m_bone))
    
    # Pelvis & Trousers
    parts.append(add_box("Pelvis", (0, 0.96, 0), (0.29, 0.16, 0.18), m_pants))
    
    # Left Leg with torn knee showing bone
    parts.append(add_cylinder("Leg_Thigh_L", (-0.10, 0.70, 0), 0.072, 0.42, material=m_pants))
    parts.append(add_box("Leg_KneeWound_L", (-0.10, 0.50, 0.06), (0.08, 0.08, 0.03), m_blood))
    parts.append(add_box("Leg_KneeBone_L", (-0.10, 0.50, 0.07), (0.05, 0.05, 0.02), m_bone))
    parts.append(add_cylinder("Leg_Shin_L", (-0.10, 0.28, 0), 0.062, 0.40, material=m_pants))
    parts.append(add_box("Leg_Foot_L", (-0.10, 0.06, 0.03), (0.10, 0.10, 0.22), m_boot))
    
    # Right Leg
    parts.append(add_cylinder("Leg_Thigh_R", (0.10, 0.70, 0), 0.072, 0.42, material=m_pants))
    parts.append(add_cylinder("Leg_Shin_R", (0.10, 0.28, 0), 0.062, 0.40, material=m_skin)) # Ripped pant leg
    parts.append(add_box("Leg_Foot_R", (0.10, 0.06, 0.03), (0.10, 0.10, 0.22), m_boot))
    
    # Join into single unified character mesh
    zombie_obj = join_objects(parts, "Zombie_Normal")
    
    # Create Root Armature for Godot Animations
    bpy.ops.object.armature_add(location=(0, 0, 0))
    arm_obj = bpy.context.active_object
    arm_obj.name = "Zombie_Rig"
    
    # Parent mesh to armature
    zombie_obj.parent = arm_obj
    
    # Create simple base Actions for Godot AnimationPlayer
    action_idle = bpy.data.actions.new(name="idle")
    arm_obj.animation_data_create()
    arm_obj.animation_data.action = action_idle
    arm_obj.keyframe_insert(data_path="location", frame=1)
    arm_obj.keyframe_insert(data_path="location", frame=30)
    
    export_glb(
        'assets/3d/zombies/zombie_normal.glb',
        'tools/blender/generated/zombie_normal.blend'
    )

def build_pilot_pistol():
    print("Building Pilot Asset 2: Realistic USP-45 Pistol...")
    clear_scene()
    
    # Materials
    m_steel = create_pbr_material("Mat_PistolSteel", (0.08, 0.09, 0.11, 1.0), metallic=0.92, roughness=0.28)
    m_poly = create_pbr_material("Mat_PistolPolymer", (0.04, 0.04, 0.05, 1.0), metallic=0.08, roughness=0.72)
    m_barrel = create_pbr_material("Mat_PistolBarrel", (0.14, 0.14, 0.16, 1.0), metallic=0.85, roughness=0.22)
    m_sight = create_pbr_material("Mat_TritiumDot", (0.15, 0.95, 0.25, 1.0), metallic=0.0, roughness=0.2, emission=(0.15, 0.95, 0.25, 1.0), emission_strength=2.5)
    
    parts = []
    
    # Slide (Top Assembly)
    parts.append(add_box("Slide_Body", (0, 0.022, -0.05), (0.032, 0.038, 0.21), m_steel))
    # Serrations
    parts.append(add_box("Slide_Serration_L", (-0.017, 0.022, 0.015), (0.003, 0.030, 0.05), m_steel))
    parts.append(add_box("Slide_Serration_R", (0.017, 0.022, 0.015), (0.003, 0.030, 0.05), m_steel))
    # Ejection Port Cutout
    parts.append(add_box("Ejection_Port", (0.012, 0.028, -0.04), (0.014, 0.024, 0.045), m_barrel))
    
    # Barrel with hollow muzzle opening
    parts.append(add_cylinder("Barrel", (0, 0.022, -0.16), 0.008, 0.05, rotation=(math.radians(90), 0, 0), material=m_barrel))
    parts.append(add_cylinder("GuideRod", (0, 0.006, -0.15), 0.004, 0.04, rotation=(math.radians(90), 0, 0), material=m_steel))
    
    # Tactical Sights with Tritium night dots
    parts.append(add_box("Sight_Front", (0, 0.044, -0.14), (0.006, 0.010, 0.015), m_steel))
    parts.append(add_uv_sphere("Sight_Dot_Front", (0, 0.044, -0.132), 0.0025, m_sight))
    parts.append(add_box("Sight_Rear", (0, 0.044, 0.035), (0.014, 0.010, 0.012), m_steel))
    parts.append(add_uv_sphere("Sight_Dot_Rear_L", (-0.004, 0.044, 0.038), 0.002, m_sight))
    parts.append(add_uv_sphere("Sight_Dot_Rear_R", (0.004, 0.044, 0.038), 0.002, m_sight))
    
    # Polymer Frame & Ergonomic Grip
    parts.append(add_box("Frame_Rail", (0, -0.002, -0.07), (0.030, 0.018, 0.16), m_poly))
    parts.append(add_box("Frame_Grip", (0, -0.055, 0.015), (0.030, 0.115, 0.048), m_poly))
    # Grip texturing ribs
    parts.append(add_box("Grip_Ribs", (0, -0.055, 0.016), (0.032, 0.080, 0.042), m_poly))
    # Trigger Guard & Trigger
    parts.append(add_box("Trigger_Guard", (0, -0.028, -0.04), (0.012, 0.034, 0.048), m_poly))
    parts.append(add_box("Trigger", (0, -0.024, -0.035), (0.005, 0.020, 0.010), m_steel))
    # External Hammer
    parts.append(add_box("Hammer", (0, 0.024, 0.045), (0.008, 0.022, 0.012), m_steel))
    # Magazine Baseplate
    parts.append(add_box("Mag_Baseplate", (0, -0.115, 0.020), (0.034, 0.012, 0.055), m_poly))
    
    pistol_obj = join_objects(parts, "Pistol_USP45")
    
    # Add MuzzleSocket Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.022, -0.185))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = pistol_obj
    
    export_glb(
        'assets/3d/weapons/pistol.glb',
        'tools/blender/generated/pistol.blend'
    )

def build_pilot_airport_section():
    print("Building Pilot Asset 3: Realistic Airport Terminal Section...")
    clear_scene()
    
    # Materials
    m_floor = create_pbr_material("Mat_AirportFloor", (0.72, 0.74, 0.76, 1.0), metallic=0.10, roughness=0.22)
    m_counter = create_pbr_material("Mat_CounterWood", (0.16, 0.14, 0.12, 1.0), metallic=0.0, roughness=0.52)
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_seat = create_pbr_material("Mat_LoungeSeat", (0.08, 0.14, 0.22, 1.0), metallic=0.0, roughness=0.68)
    m_beacon = create_pbr_material("Mat_EmergencyBeacon", (0.95, 0.08, 0.04, 1.0), metallic=0.1, roughness=0.2, emission=(0.95, 0.08, 0.04, 1.0), emission_strength=3.5)
    m_screen = create_pbr_material("Mat_FlightScreen", (0.04, 0.12, 0.25, 1.0), metallic=0.1, roughness=0.3, emission=(0.08, 0.25, 0.55, 1.0), emission_strength=1.8)
    m_case1 = create_pbr_material("Mat_SuitcaseBrown", (0.35, 0.22, 0.14, 1.0), metallic=0.05, roughness=0.60)
    m_case2 = create_pbr_material("Mat_SuitcaseRed", (0.50, 0.08, 0.08, 1.0), metallic=0.05, roughness=0.60)
    
    parts = []
    
    # 1. Floor Tile Platform (10m x 10m x 0.1m)
    parts.append(add_box("Floor_Base", (0, -0.05, 0), (10.0, 0.1, 10.0), m_floor))
    
    # 2. Check-in Counter Desk with Luggage Scale & Monitor
    parts.append(add_box("Desk_Main", (0, 0.60, -3.5), (2.6, 1.2, 0.8), m_counter))
    parts.append(add_box("Desk_Top", (0, 1.22, -3.6), (2.7, 0.05, 0.6), m_metal))
    parts.append(add_box("Desk_BaggageScale", (0, 0.12, -3.0), (1.8, 0.24, 0.7), m_metal))
    # Monitor console
    parts.append(add_cylinder("Monitor_Stand", (-0.5, 1.35, -3.6), 0.02, 0.20, material=m_metal))
    parts.append(add_box("Monitor_Frame", (-0.5, 1.55, -3.6), (0.45, 0.32, 0.06), m_metal))
    parts.append(add_box("Monitor_Display", (-0.5, 1.55, -3.56), (0.41, 0.28, 0.01), m_screen))
    
    # 3. Airport Lounge Seats (Row of 3)
    parts.append(add_box("Seat_Beam", (0, 0.40, 2.5), (1.9, 0.06, 0.08), m_metal))
    parts.append(add_box("Seat_Leg_L", (-0.8, 0.20, 2.5), (0.06, 0.40, 0.40), m_metal))
    parts.append(add_box("Seat_Leg_R", (0.8, 0.20, 2.5), (0.06, 0.40, 0.40), m_metal))
    for x_pos in [-0.6, 0.0, 0.6]:
        parts.append(add_box(f"Seat_Cushion_{x_pos}", (x_pos, 0.46, 2.5), (0.50, 0.06, 0.46), m_seat))
        parts.append(add_box(f"Seat_Back_{x_pos}", (x_pos, 0.74, 2.25), (0.50, 0.52, 0.06), m_seat))
        
    # 4. Structural Pillar with Emergency Light
    parts.append(add_box("Pillar_Base", (-3.5, 0.25, 0), (1.1, 0.5, 1.1), m_metal))
    parts.append(add_box("Pillar_Column", (-3.5, 3.25, 0), (0.75, 5.5, 0.75), m_floor))
    parts.append(add_box("Pillar_Capital", (-3.5, 6.15, 0), (1.1, 0.3, 1.1), m_metal))
    # Emergency Siren Light Housing
    parts.append(add_box("Beacon_Box", (-3.5, 3.0, 0.42), (0.24, 0.32, 0.12), m_metal))
    parts.append(add_cylinder("Beacon_Dome", (-3.5, 3.0, 0.50), 0.07, 0.12, rotation=(math.radians(90), 0, 0), material=m_beacon))
    
    # 5. Luggage Trolley with Suitcases
    parts.append(add_box("Cart_Frame", (3.0, 0.14, -1.0), (0.70, 0.06, 1.10), m_metal))
    parts.append(add_box("Cart_Handle", (3.0, 0.62, -0.45), (0.65, 0.90, 0.05), m_metal))
    parts.append(add_box("Suitcase_1", (3.0, 0.30, -1.1), (0.55, 0.24, 0.75), m_case1))
    parts.append(add_box("Suitcase_2", (3.02, 0.50, -1.05), (0.48, 0.18, 0.62), m_case2))
    
    terminal_obj = join_objects(parts, "Airport_Terminal_Section")
    
    export_glb(
        'assets/3d/environments/airport_terminal_section.glb',
        'tools/blender/generated/airport_terminal_section.blend'
    )

if __name__ == '__main__':
    build_pilot_zombie()
    build_pilot_pistol()
    build_pilot_airport_section()
    print("ALL PILOT ASSETS SUCCESSFULLY BUILT AND EXPORTED TO GLB!")
