import sys
import os
import math

sys.path.append(os.getcwd())
import bpy
from tools.blender.scripts.asset_builder import (
    clear_scene, create_pbr_material, add_box, add_cylinder, add_cone, add_uv_sphere,
    join_objects, export_glb, export_obj
)

def build_materials():
    mats = {}
    mats['steel'] = create_pbr_material("Mat_Steel", (0.35, 0.38, 0.42, 1.0), metallic=0.85, roughness=0.30)
    mats['polished_steel'] = create_pbr_material("Mat_PolishedSteel", (0.65, 0.68, 0.72, 1.0), metallic=0.92, roughness=0.18)
    mats['dark_metal'] = create_pbr_material("Mat_DarkMetal", (0.18, 0.20, 0.22, 1.0), metallic=0.80, roughness=0.40)
    mats['polymer_black'] = create_pbr_material("Mat_PolymerBlack", (0.15, 0.16, 0.18, 1.0), metallic=0.10, roughness=0.65)
    mats['polymer_od'] = create_pbr_material("Mat_PolymerOD", (0.22, 0.28, 0.20, 1.0), metallic=0.12, roughness=0.60)
    mats['wood'] = create_pbr_material("Mat_Wood", (0.45, 0.22, 0.12, 1.0), metallic=0.05, roughness=0.55)
    mats['chrome'] = create_pbr_material("Mat_Chrome", (0.75, 0.78, 0.82, 1.0), metallic=0.95, roughness=0.15)
    mats['brass'] = create_pbr_material("Mat_Brass", (0.85, 0.65, 0.25, 1.0), metallic=0.88, roughness=0.25)
    mats['rubber'] = create_pbr_material("Mat_Rubber", (0.12, 0.12, 0.14, 1.0), metallic=0.02, roughness=0.85)
    mats['tritium'] = create_pbr_material("Mat_Tritium", (0.2, 1.0, 0.35, 1.0), metallic=0.0, roughness=0.2, emission=(0.2, 1.0, 0.35, 1.0), emission_strength=5.0)
    mats['red_dot'] = create_pbr_material("Mat_RedDot", (1.0, 0.1, 0.08, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.1, 0.08, 1.0), emission_strength=6.0)
    mats['optic_glass'] = create_pbr_material("Mat_OpticGlass", (0.3, 0.5, 0.7, 1.0), metallic=0.1, roughness=0.1)
    return mats

def build_usp45():
    clear_scene()
    m = build_materials()
    parts = []
    # Slide
    parts.append(add_box("Slide", (0, 0.022, -0.05), (0.034, 0.040, 0.22), m['steel']))
    parts.append(add_box("Ejection_Port", (0.013, 0.028, -0.04), (0.015, 0.025, 0.048), m['polished_steel']))
    # Barrel
    parts.append(add_cylinder("Barrel", (0, 0.022, -0.17), 0.009, 0.06, rotation=(math.radians(90), 0, 0), material=m['polished_steel']))
    parts.append(add_cylinder("GuideRod", (0, 0.006, -0.16), 0.005, 0.045, rotation=(math.radians(90), 0, 0), material=m['steel']))
    # Sights
    parts.append(add_box("Sight_Front", (0, 0.045, -0.14), (0.007, 0.012, 0.016), m['steel']))
    parts.append(add_uv_sphere("Sight_Dot_Front", (0, 0.045, -0.132), 0.003, m['tritium']))
    parts.append(add_box("Sight_Rear", (0, 0.045, 0.038), (0.016, 0.012, 0.014), m['steel']))
    # Frame
    parts.append(add_box("Frame", (0, -0.002, -0.07), (0.032, 0.020, 0.17), m['polymer_black']))
    parts.append(add_box("Grip", (0, -0.055, 0.015), (0.032, 0.118, 0.052), m['polymer_black']))
    parts.append(add_box("TriggerGuard", (0, -0.028, -0.04), (0.014, 0.036, 0.050), m['polymer_black']))
    parts.append(add_box("Trigger", (0, -0.024, -0.035), (0.006, 0.022, 0.012), m['steel']))
    parts.append(add_box("Hammer", (0, 0.026, 0.048), (0.009, 0.024, 0.014), m['steel']))
    parts.append(add_box("Mag_Baseplate", (0, -0.118, 0.020), (0.036, 0.014, 0.058), m['polymer_black']))

    obj = join_objects(parts, "Weapon_USP45")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.022, -0.20))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/usp45.obj')
    export_obj('models/weapons/pistol.obj')
    export_glb('assets/3d/weapons/usp45.glb')
    export_glb('assets/3d/weapons/pistol.glb')
    print("USP-45 / Pistol generated.")

def build_m4a1():
    clear_scene()
    m = build_materials()
    parts = []
    # Receiver
    parts.append(add_box("Lower_Receiver", (0, 0.01, 0.02), (0.040, 0.060, 0.23), m['steel']))
    parts.append(add_box("Upper_Receiver", (0, 0.048, 0.02), (0.038, 0.044, 0.23), m['steel']))
    parts.append(add_box("Top_Rail", (0, 0.074, -0.06), (0.024, 0.012, 0.39), m['dark_metal']))
    # Sight
    parts.append(add_box("Optic_Hood", (0, 0.114, 0.01), (0.038, 0.045, 0.085), m['polymer_black']))
    parts.append(add_cylinder("Optic_Lens", (0, 0.114, 0.01), 0.014, 0.07, rotation=(math.radians(90), 0, 0), material=m['red_dot']))
    # Handguard & Barrel
    parts.append(add_box("Handguard", (0, 0.042, -0.22), (0.044, 0.046, 0.27), m['steel']))
    parts.append(add_box("Angled_Foregrip", (0, 0.006, -0.22), (0.030, 0.048, 0.115), m['polymer_black']))
    parts.append(add_cylinder("Barrel", (0, 0.042, -0.39), 0.011, 0.21, rotation=(math.radians(90), 0, 0), material=m['polished_steel']))
    parts.append(add_cylinder("Flash_Hider", (0, 0.042, -0.50), 0.013, 0.048, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    # Mag & Grip & Stock
    parts.append(add_box("STANAG_Mag", (0, -0.098, -0.03), (0.028, 0.175, 0.068), m['polymer_black']))
    parts.append(add_box("Pistol_Grip", (0, -0.068, 0.09), (0.032, 0.118, 0.048), m['polymer_black']))
    parts.append(add_cylinder("Buffer_Tube", (0, 0.044, 0.22), 0.016, 0.19, rotation=(math.radians(90), 0, 0), material=m['steel']))
    parts.append(add_box("Crane_Stock", (0, 0.052, 0.26), (0.046, 0.068, 0.19), m['polymer_black']))
    parts.append(add_box("Rubber_Buttpad", (0, 0.047, 0.35), (0.044, 0.125, 0.020), m['rubber']))

    obj = join_objects(parts, "Weapon_M4A1")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.042, -0.53))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/m4a1.obj')
    export_obj('models/weapons/rifle.obj')
    export_glb('assets/3d/weapons/m4a1.glb')
    export_glb('assets/3d/weapons/rifle.glb')
    print("M4A1 / Rifle generated.")

def build_remington870():
    clear_scene()
    m = build_materials()
    parts = []
    # Receiver
    parts.append(add_box("Receiver", (0, 0.020, 0.04), (0.040, 0.066, 0.22), m['dark_metal']))
    # Barrel & Mag tube
    parts.append(add_cylinder("Barrel_12G", (0, 0.040, -0.33), 0.014, 0.54, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_box("Heat_Shield", (0, 0.052, -0.29), (0.032, 0.020, 0.38), m['steel']))
    parts.append(add_uv_sphere("Front_Bead", (0, 0.056, -0.58), 0.004, m['brass']))
    parts.append(add_cylinder("Mag_Tube", (0, 0.013, -0.31), 0.015, 0.52, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_box("Barrel_Clamp", (0, 0.026, -0.52), (0.034, 0.048, 0.022), m['steel']))
    # Pump slide
    parts.append(add_cylinder("Pump_Forend", (0, 0.013, -0.25), 0.024, 0.21, rotation=(math.radians(90), 0, 0), material=m['polymer_black']))
    # Stock
    parts.append(add_box("Stock_Wrist", (0, -0.006, 0.17), (0.034, 0.060, 0.085), m['polymer_black']))
    parts.append(add_box("Pistol_Grip", (0, -0.078, 0.14), (0.034, 0.114, 0.050), m['polymer_black']))
    parts.append(add_box("Buttstock", (0, -0.022, 0.30), (0.038, 0.098, 0.21), m['polymer_black']))
    parts.append(add_box("Recoil_Pad", (0, -0.026, 0.405), (0.040, 0.128, 0.026), m['rubber']))

    obj = join_objects(parts, "Weapon_Remington870")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.040, -0.60))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/remington870.obj')
    export_obj('models/weapons/shotgun.obj')
    export_glb('assets/3d/weapons/remington870.glb')
    export_glb('assets/3d/weapons/shotgun.glb')
    print("Remington 870 / Shotgun generated.")

def build_ak47():
    clear_scene()
    m = build_materials()
    parts = []
    # Stamped receiver & dust cover
    parts.append(add_box("Receiver", (0, 0.020, 0.02), (0.042, 0.062, 0.26), m['dark_metal']))
    parts.append(add_cylinder("Dust_Cover", (0, 0.052, 0.02), 0.020, 0.25, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    # Gas Tube & Barrel
    parts.append(add_cylinder("Gas_Tube", (0, 0.055, -0.20), 0.012, 0.22, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Barrel", (0, 0.032, -0.34), 0.011, 0.46, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Front_Sight_Post", (0, 0.065, -0.46), 0.005, 0.035, rotation=(0, 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Slant_Brake", (0, 0.032, -0.58), 0.013, 0.040, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    # Laminated Wood Furniture
    parts.append(add_box("Lower_Handguard", (0, 0.026, -0.19), (0.044, 0.038, 0.19), m['wood']))
    parts.append(add_box("Upper_Handguard", (0, 0.058, -0.19), (0.038, 0.026, 0.16), m['wood']))
    parts.append(add_box("Wood_Pistol_Grip", (0, -0.065, 0.10), (0.032, 0.115, 0.046), m['wood']))
    parts.append(add_box("Wood_Buttstock", (0, 0.008, 0.29), (0.038, 0.095, 0.25), m['wood']))
    parts.append(add_box("Stock_Plate", (0, 0.008, 0.418), (0.038, 0.098, 0.012), m['dark_metal']))
    # Curved Banana Mag
    parts.append(add_box("Curved_Mag", (0, -0.110, -0.03), (0.030, 0.180, 0.085), m['steel']))

    obj = join_objects(parts, "Weapon_AK47")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.032, -0.60))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/ak47.obj')
    export_glb('assets/3d/weapons/ak47.glb')
    print("AK-47 generated.")

def build_desert_eagle():
    clear_scene()
    m = build_materials()
    parts = []
    # Chrome Slide & Fluted Barrel
    parts.append(add_box("Slide_Massive", (0, 0.028, -0.06), (0.042, 0.048, 0.26), m['chrome']))
    parts.append(add_box("Barrel_Fluted", (0, 0.028, -0.19), (0.040, 0.044, 0.12), m['chrome']))
    parts.append(add_cylinder("Bore_50AE", (0, 0.032, -0.24), 0.013, 0.05, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    # Top Picatinny Slots
    parts.append(add_box("Top_Rib", (0, 0.055, -0.14), (0.022, 0.010, 0.22), m['chrome']))
    parts.append(add_box("Combat_Sight_Front", (0, 0.064, -0.23), (0.008, 0.014, 0.018), m['dark_metal']))
    parts.append(add_box("Combat_Sight_Rear", (0, 0.064, 0.045), (0.018, 0.014, 0.016), m['dark_metal']))
    # Frame & Rubber Wrap Grip
    parts.append(add_box("Frame_Chrome", (0, 0.002, -0.06), (0.038, 0.024, 0.20), m['chrome']))
    parts.append(add_box("Heavy_Grip", (0, -0.062, 0.022), (0.038, 0.128, 0.062), m['rubber']))
    parts.append(add_box("Beaver_Tail", (0, 0.015, 0.060), (0.026, 0.018, 0.034), m['chrome']))
    parts.append(add_box("Trigger_Guard", (0, -0.030, -0.045), (0.016, 0.040, 0.056), m['chrome']))
    parts.append(add_box("Trigger", (0, -0.026, -0.038), (0.007, 0.024, 0.014), m['dark_metal']))

    obj = join_objects(parts, "Weapon_DesertEagle")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.032, -0.26))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/desert_eagle.obj')
    export_glb('assets/3d/weapons/desert_eagle.glb')
    print("Desert Eagle generated.")

def build_mp5():
    clear_scene()
    m = build_materials()
    parts = []
    # Compact Upper & Lower
    parts.append(add_cylinder("Receiver_Tube", (0, 0.035, 0.02), 0.022, 0.28, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_box("Lower_Frame", (0, -0.005, 0.04), (0.036, 0.045, 0.16), m['polymer_black']))
    # Front Hooded Sight
    parts.append(add_cylinder("Sight_Hood_Ring", (0, 0.062, -0.28), 0.014, 0.016, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Sight_Post", (0, 0.062, -0.28), 0.002, 0.012, rotation=(0, 0, 0), material=m['tritium']))
    # Barrel & 3-lug adapter
    parts.append(add_cylinder("Barrel_9mm", (0, 0.035, -0.26), 0.010, 0.20, rotation=(math.radians(90), 0, 0), material=m['steel']))
    parts.append(add_cylinder("Three_Lug", (0, 0.035, -0.34), 0.012, 0.04, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    # Ribbed Handguard
    parts.append(add_box("Ribbed_Handguard", (0, 0.024, -0.16), (0.044, 0.048, 0.16), m['polymer_black']))
    # Curved 9mm Magazine
    parts.append(add_box("Curved_9mm_Mag", (0, -0.090, -0.04), (0.024, 0.160, 0.048), m['steel']))
    # Grip & Retractable Struts
    parts.append(add_box("Pistol_Grip", (0, -0.065, 0.08), (0.030, 0.110, 0.044), m['polymer_black']))
    parts.append(add_box("Stock_Strut_L", (-0.020, 0.035, 0.16), (0.006, 0.010, 0.18), m['steel']))
    parts.append(add_box("Stock_Strut_R", (0.020, 0.035, 0.16), (0.006, 0.010, 0.18), m['steel']))
    parts.append(add_box("Stock_Buttpad", (0, 0.035, 0.25), (0.044, 0.095, 0.018), m['rubber']))

    obj = join_objects(parts, "Weapon_MP5")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.035, -0.37))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/mp5.obj')
    export_glb('assets/3d/weapons/mp5.glb')
    print("MP5 generated.")

def build_awp():
    clear_scene()
    m = build_materials()
    parts = []
    # Thumbhole Olive Drab Stock
    parts.append(add_box("Chassis_Forend", (0, 0.020, -0.20), (0.046, 0.052, 0.40), m['polymer_od']))
    parts.append(add_box("Chassis_Rear", (0, 0.010, 0.18), (0.044, 0.085, 0.28), m['polymer_od']))
    parts.append(add_box("Cheek_Rest", (0, 0.065, 0.16), (0.036, 0.030, 0.14), m['rubber']))
    parts.append(add_box("Recoil_Pad", (0, 0.010, 0.325), (0.044, 0.110, 0.025), m['rubber']))
    # Long Fluted Heavy Barrel & Muzzle Brake
    parts.append(add_cylinder("Heavy_Barrel", (0, 0.042, -0.52), 0.015, 0.65, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_box("Muzzle_Brake", (0, 0.042, -0.86), (0.034, 0.032, 0.065), m['steel']))
    # Massive Sniper Scope
    parts.append(add_cylinder("Scope_Body", (0, 0.105, -0.05), 0.020, 0.26, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Scope_Bell_Front", (0, 0.105, -0.19), 0.028, 0.08, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Scope_Bell_Rear", (0, 0.105, 0.09), 0.024, 0.06, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Scope_Lens", (0, 0.105, -0.22), 0.025, 0.01, rotation=(math.radians(90), 0, 0), material=m['optic_glass']))
    parts.append(add_box("Mount_Front", (0, 0.065, -0.12), (0.028, 0.042, 0.025), m['steel']))
    parts.append(add_box("Mount_Rear", (0, 0.065, 0.02), (0.028, 0.042, 0.025), m['steel']))
    # Bolt Handle & Magazine
    parts.append(add_cylinder("Bolt_Handle", (0.035, 0.045, 0.05), 0.006, 0.05, rotation=(0, 0, math.radians(45)), material=m['polished_steel']))
    parts.append(add_uv_sphere("Bolt_Knob", (0.055, 0.055, 0.05), 0.012, m['polymer_black']))
    parts.append(add_box("Lapua_Mag", (0, -0.045, -0.02), (0.032, 0.085, 0.082), m['dark_metal']))
    # Folding Bipod
    parts.append(add_cylinder("Bipod_Leg_L", (-0.025, -0.015, -0.34), 0.006, 0.14, rotation=(math.radians(85), math.radians(10), 0), material=m['steel']))
    parts.append(add_cylinder("Bipod_Leg_R", (0.025, -0.015, -0.34), 0.006, 0.14, rotation=(math.radians(85), math.radians(-10), 0), material=m['steel']))

    obj = join_objects(parts, "Weapon_AWP")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.042, -0.90))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/awp.obj')
    export_glb('assets/3d/weapons/awp.glb')
    print("AWP generated.")

def build_combat_knife():
    clear_scene()
    m = build_materials()
    parts = []
    # Tanto / Clip Point Blade with Spine Serrations
    parts.append(add_box("Blade_Main", (0, 0.012, -0.14), (0.006, 0.036, 0.18), m['dark_metal']))
    parts.append(add_box("Blade_Tip_Tanto", (0, 0.014, -0.23), (0.005, 0.026, 0.06), m['polished_steel']))
    parts.append(add_box("Spine_Serrations", (0, 0.028, -0.10), (0.008, 0.008, 0.08), m['polished_steel']))
    # Crossguard
    parts.append(add_box("Crossguard", (0, 0.010, -0.045), (0.024, 0.065, 0.014), m['steel']))
    # Textured Grip
    parts.append(add_box("Grip_Body", (0, 0.005, 0.02), (0.026, 0.042, 0.12), m['rubber']))
    for z in [-0.02, 0.01, 0.04, 0.07]:
        parts.append(add_box(f"Rib_{z}", (0, 0.005, z), (0.028, 0.044, 0.012), m['polymer_black']))
    # Glass Breaker Pommel
    parts.append(add_cone("Pommel_Spike", (0, 0.005, 0.09), 0.010, 0.022, rotation=(math.radians(-90), 0, 0), material=m['polished_steel']))

    obj = join_objects(parts, "Weapon_CombatKnife")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.014, -0.26))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/combat_knife.obj')
    export_glb('assets/3d/weapons/combat_knife.glb')
    print("Combat Knife generated.")

def build_crossbow():
    clear_scene()
    m = build_materials()
    parts = []
    # Rail / Flight Track & Stock
    parts.append(add_box("Rail_Body", (0, 0.025, -0.15), (0.038, 0.042, 0.46), m['dark_metal']))
    parts.append(add_box("Composite_Stock", (0, -0.015, 0.16), (0.042, 0.085, 0.26), m['polymer_black']))
    parts.append(add_box("Pistol_Grip", (0, -0.085, 0.06), (0.032, 0.110, 0.046), m['polymer_black']))
    # Stirrup at Front
    parts.append(add_box("Stirrup_Front", (0, 0.015, -0.42), (0.16, 0.016, 0.08), m['steel']))
    # High-Tension Recurve Limbs
    parts.append(add_box("Limb_Left", (-0.18, 0.028, -0.32), (0.24, 0.020, 0.025), m['polymer_od']))
    parts.append(add_box("Limb_Right", (0.18, 0.028, -0.32), (0.24, 0.020, 0.025), m['polymer_od']))
    # Bowstring
    parts.append(add_cylinder("Bowstring_L", (-0.14, 0.030, -0.22), 0.0025, 0.24, rotation=(0, math.radians(45), 0), material=m['polished_steel']))
    parts.append(add_cylinder("Bowstring_R", (0.14, 0.030, -0.22), 0.0025, 0.24, rotation=(0, math.radians(-45), 0), material=m['polished_steel']))
    # Tactical Bolt Loaded
    parts.append(add_cylinder("Carbon_Bolt", (0, 0.046, -0.18), 0.005, 0.32, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cone("Broadhead_Tip", (0, 0.046, -0.35), 0.012, 0.035, rotation=(math.radians(90), 0, 0), material=m['polished_steel']))
    # Optic
    parts.append(add_box("Crossbow_Optic", (0, 0.075, -0.02), (0.030, 0.035, 0.10), m['polymer_black']))
    parts.append(add_cylinder("Optic_Dot", (0, 0.075, -0.02), 0.010, 0.09, rotation=(math.radians(90), 0, 0), material=m['tritium']))

    obj = join_objects(parts, "Weapon_Crossbow")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.046, -0.38))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/crossbow.obj')
    export_glb('assets/3d/weapons/crossbow.glb')
    print("Crossbow generated.")

def build_grenade_launcher():
    clear_scene()
    m = build_materials()
    parts = []
    # 40mm Heavy Rifled Barrel
    parts.append(add_cylinder("Barrel_40mm", (0, 0.045, -0.24), 0.032, 0.36, rotation=(math.radians(90), 0, 0), material=m['dark_metal']))
    parts.append(add_cylinder("Bore_Interior", (0, 0.045, -0.38), 0.025, 0.08, rotation=(math.radians(90), 0, 0), material=m['steel']))
    # Break-action Receiver & Hinge
    parts.append(add_box("Receiver_Massive", (0, 0.025, 0.02), (0.068, 0.085, 0.18), m['steel']))
    parts.append(add_cylinder("Hinge_Pin", (0, -0.005, -0.06), 0.012, 0.072, rotation=(0, 0, math.radians(90)), material=m['polished_steel']))
    # Leaf Sight (Quadrant Sight)
    parts.append(add_box("Leaf_Sight_Post", (0, 0.105, -0.16), (0.012, 0.065, 0.012), m['dark_metal']))
    parts.append(add_box("Range_Aperture", (0, 0.125, -0.16), (0.024, 0.012, 0.012), m['tritium']))
    # Wood / Polymer Stock & Forend
    parts.append(add_box("Forend_Wood", (0, 0.005, -0.20), (0.062, 0.048, 0.22), m['wood']))
    parts.append(add_box("Pistol_Grip", (0, -0.065, 0.08), (0.036, 0.115, 0.052), m['wood']))
    parts.append(add_box("Shoulder_Stock", (0, 0.010, 0.24), (0.054, 0.115, 0.26), m['wood']))
    parts.append(add_box("Heavy_Rubber_Pad", (0, 0.010, 0.375), (0.056, 0.130, 0.028), m['rubber']))
    # 40mm HE Round preview inside
    parts.append(add_cylinder("HE_Shell_Brass", (0, 0.045, -0.04), 0.022, 0.06, rotation=(math.radians(90), 0, 0), material=m['brass']))

    obj = join_objects(parts, "Weapon_GrenadeLauncher")
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.045, -0.44))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = obj

    export_obj('models/weapons/grenade_launcher.obj')
    export_glb('assets/3d/weapons/grenade_launcher.glb')
    print("Grenade Launcher generated.")

if __name__ == '__main__':
    build_usp45()
    build_m4a1()
    build_remington870()
    build_ak47()
    build_desert_eagle()
    build_mp5()
    build_awp()
    build_combat_knife()
    build_crossbow()
    build_grenade_launcher()
    print("ALL 10 WEAPONS SUCCESSFULLY BUILT AND EXPORTED AS GLB & OBJ!")
