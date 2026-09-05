import sys
import os
import math
sys.path.append(os.getcwd())
import bpy
from tools.blender.scripts.asset_builder import (
    clear_scene, create_pbr_material, add_box, add_cylinder, add_cone, add_uv_sphere,
    join_objects, export_glb, export_obj
)

def build_usp45_pistol():
    print("Building High-Visibility Weapon 1: Tactical USP-45 Pistol...")
    clear_scene()
    
    # Enhanced high-visibility PBR materials
    m_steel = create_pbr_material("Mat_PistolSteel", (0.40, 0.43, 0.47, 1.0), metallic=0.82, roughness=0.32)
    m_poly = create_pbr_material("Mat_PistolPolymer", (0.24, 0.26, 0.29, 1.0), metallic=0.12, roughness=0.62)
    m_barrel = create_pbr_material("Mat_PistolBarrel", (0.62, 0.65, 0.68, 1.0), metallic=0.90, roughness=0.18)
    m_sight = create_pbr_material("Mat_TritiumDot", (0.20, 1.0, 0.35, 1.0), metallic=0.0, roughness=0.2, emission=(0.20, 1.0, 0.35, 1.0), emission_strength=5.0)
    
    parts = []
    
    # Slide (Top Assembly)
    parts.append(add_box("Slide_Body", (0, 0.022, -0.05), (0.034, 0.040, 0.22), m_steel))
    # Serrations front & rear
    parts.append(add_box("Slide_Serration_Rear_L", (-0.018, 0.022, 0.015), (0.004, 0.032, 0.05), m_steel))
    parts.append(add_box("Slide_Serration_Rear_R", (0.018, 0.022, 0.015), (0.004, 0.032, 0.05), m_steel))
    parts.append(add_box("Slide_Serration_Front_L", (-0.018, 0.022, -0.11), (0.004, 0.030, 0.04), m_steel))
    parts.append(add_box("Slide_Serration_Front_R", (0.018, 0.022, -0.11), (0.004, 0.030, 0.04), m_steel))
    
    # Ejection Port & Extractor with gleaming silver chamber
    parts.append(add_box("Ejection_Port", (0.013, 0.028, -0.04), (0.015, 0.025, 0.048), m_barrel))
    
    # Barrel & Guide Rod
    parts.append(add_cylinder("Barrel", (0, 0.022, -0.17), 0.009, 0.06, rotation=(math.radians(90), 0, 0), material=m_barrel))
    parts.append(add_cylinder("GuideRod", (0, 0.006, -0.16), 0.005, 0.045, rotation=(math.radians(90), 0, 0), material=m_steel))
    
    # Tactical Sights with high-visibility Tritium night dots
    parts.append(add_box("Sight_Front", (0, 0.045, -0.14), (0.007, 0.012, 0.016), m_steel))
    parts.append(add_uv_sphere("Sight_Dot_Front", (0, 0.045, -0.132), 0.003, m_sight))
    parts.append(add_box("Sight_Rear", (0, 0.045, 0.038), (0.016, 0.012, 0.014), m_steel))
    parts.append(add_uv_sphere("Sight_Dot_Rear_L", (-0.005, 0.045, 0.041), 0.0025, m_sight))
    parts.append(add_uv_sphere("Sight_Dot_Rear_R", (0.005, 0.045, 0.041), 0.0025, m_sight))
    
    # Polymer Frame & Ergonomic Grip
    parts.append(add_box("Frame_Rail", (0, -0.002, -0.07), (0.032, 0.020, 0.17), m_poly))
    parts.append(add_box("Frame_Grip", (0, -0.055, 0.015), (0.032, 0.118, 0.052), m_poly))
    # Grip texturing ribs
    parts.append(add_box("Grip_Ribs", (0, -0.055, 0.016), (0.034, 0.082, 0.045), m_poly))
    # Trigger Guard & Trigger
    parts.append(add_box("Trigger_Guard", (0, -0.028, -0.04), (0.014, 0.036, 0.050), m_poly))
    parts.append(add_box("Trigger", (0, -0.024, -0.035), (0.006, 0.022, 0.012), m_steel))
    # External Hammer & Beavertail
    parts.append(add_box("Hammer", (0, 0.026, 0.048), (0.009, 0.024, 0.014), m_steel))
    parts.append(add_box("Beavertail", (0, 0.008, 0.044), (0.022, 0.014, 0.028), m_poly))
    # Magazine Baseplate
    parts.append(add_box("Mag_Baseplate", (0, -0.118, 0.020), (0.036, 0.014, 0.058), m_poly))
    
    pistol_obj = join_objects(parts, "Pistol_USP45")
    export_obj('models/weapons/pistol.obj')
    
    # Add MuzzleSocket Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.022, -0.20))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = pistol_obj
    
    export_glb('assets/3d/weapons/pistol.glb', 'tools/blender/generated/pistol.blend')

def build_m4a1_rifle():
    print("Building High-Visibility Weapon 2: M4A1 Sentinel Assault Rifle...")
    clear_scene()
    
    m_anodized = create_pbr_material("Mat_RifleAnodized", (0.35, 0.38, 0.42, 1.0), metallic=0.78, roughness=0.35)
    m_poly = create_pbr_material("Mat_RiflePolymer", (0.26, 0.27, 0.30, 1.0), metallic=0.10, roughness=0.65)
    m_steel = create_pbr_material("Mat_RifleSteel", (0.58, 0.60, 0.64, 1.0), metallic=0.88, roughness=0.25)
    m_optic_lens = create_pbr_material("Mat_RedDotReticle", (1.0, 0.10, 0.08, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.10, 0.08, 1.0), emission_strength=6.0)
    
    parts = []
    
    # 1. Receiver (Upper + Lower)
    parts.append(add_box("Lower_Receiver", (0, 0.01, 0.02), (0.040, 0.060, 0.23), m_anodized))
    parts.append(add_box("Upper_Receiver", (0, 0.048, 0.02), (0.038, 0.044, 0.23), m_anodized))
    # Brass deflector & Forward assist
    parts.append(add_box("Brass_Deflector", (0.026, 0.050, 0.06), (0.016, 0.024, 0.026), m_anodized))
    parts.append(add_cylinder("Forward_Assist", (0.026, 0.050, 0.10), 0.008, 0.032, rotation=(0, math.radians(45), 0), material=m_steel))
    
    # 2. Picatinny Top Rail
    parts.append(add_box("Top_Picatinny_Rail", (0, 0.074, -0.06), (0.024, 0.012, 0.39), m_steel))
    
    # 3. Holographic / Red Dot Sight
    parts.append(add_box("Optic_Riser", (0, 0.086, 0.01), (0.032, 0.014, 0.075), m_steel))
    parts.append(add_box("Optic_Hood", (0, 0.114, 0.01), (0.038, 0.045, 0.085), m_poly))
    # Interior glass lens with glowing red reticle
    parts.append(add_cylinder("Optic_Lens_Glass", (0, 0.114, 0.01), 0.014, 0.07, rotation=(math.radians(90), 0, 0), material=m_optic_lens))
    
    # 4. Quad-Rail Handguard & Angled Foregrip
    parts.append(add_box("Handguard_Quad", (0, 0.042, -0.22), (0.044, 0.046, 0.27), m_anodized))
    # Ventilation cutouts
    for z_cut in [-0.14, -0.20, -0.26, -0.32]:
        parts.append(add_box(f"Vent_{z_cut}", (0.024, 0.042, z_cut), (0.005, 0.020, 0.032), m_steel))
        parts.append(add_box(f"Vent_L_{z_cut}", (-0.024, 0.042, z_cut), (0.005, 0.020, 0.032), m_steel))
    # Tactical Angled Foregrip
    parts.append(add_box("Angled_Foregrip", (0, 0.006, -0.22), (0.030, 0.048, 0.115), m_poly))
    
    # 5. Barrel, Gas Block, and Birdcage Flash Hider
    parts.append(add_cylinder("Barrel_14_5", (0, 0.042, -0.39), 0.011, 0.21, rotation=(math.radians(90), 0, 0), material=m_steel))
    parts.append(add_cylinder("Gas_Block", (0, 0.048, -0.37), 0.015, 0.032, rotation=(math.radians(90), 0, 0), material=m_steel))
    parts.append(add_cylinder("Birdcage_Hider", (0, 0.042, -0.50), 0.013, 0.048, rotation=(math.radians(90), 0, 0), material=m_steel))
    
    # 6. Curved 30-round STANAG Magazine
    parts.append(add_box("STANAG_Mag", (0, -0.098, -0.03), (0.028, 0.175, 0.068), m_poly))
    parts.append(add_box("Mag_Base", (0, -0.190, -0.02), (0.030, 0.016, 0.074), m_poly))
    
    # 7. Ergonomic Tactical Pistol Grip & Trigger
    parts.append(add_box("Pistol_Grip", (0, -0.068, 0.09), (0.032, 0.118, 0.048), m_poly))
    parts.append(add_box("Trigger_Guard", (0, -0.028, 0.035), (0.015, 0.030, 0.048), m_poly))
    parts.append(add_box("Trigger", (0, -0.024, 0.040), (0.006, 0.020, 0.012), m_steel))
    
    # 8. Buffer Tube & Telescopic Crane Stock
    parts.append(add_cylinder("Buffer_Tube", (0, 0.044, 0.22), 0.016, 0.19, rotation=(math.radians(90), 0, 0), material=m_steel))
    parts.append(add_box("Crane_Stock_Cheek", (0, 0.052, 0.26), (0.046, 0.068, 0.19), m_poly))
    parts.append(add_box("Rubber_Buttpad", (0, 0.047, 0.35), (0.044, 0.125, 0.020), m_poly))
    
    rifle_obj = join_objects(parts, "Rifle_M4A1")
    export_obj('models/weapons/rifle.obj')
    
    # Add MuzzleSocket
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.042, -0.53))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = rifle_obj
    
    export_glb('assets/3d/weapons/rifle.glb', 'tools/blender/generated/rifle.blend')

def build_remington870_shotgun():
    print("Building High-Visibility Weapon 3: Tactical Remington 870 Shotgun...")
    clear_scene()
    
    m_gunmetal = create_pbr_material("Mat_ShotgunSteel", (0.42, 0.45, 0.49, 1.0), metallic=0.82, roughness=0.30)
    m_synthetic = create_pbr_material("Mat_ShotgunStock", (0.25, 0.27, 0.30, 1.0), metallic=0.10, roughness=0.70)
    m_rubber = create_pbr_material("Mat_RecoilPad", (0.18, 0.18, 0.20, 1.0), metallic=0.05, roughness=0.85)
    m_bead = create_pbr_material("Mat_BeadSight", (1.0, 0.88, 0.30, 1.0), metallic=0.95, roughness=0.15, emission=(1.0, 0.88, 0.30, 1.0), emission_strength=3.0)
    
    parts = []
    
    # 1. Solid Milled Steel Receiver
    parts.append(add_box("Receiver_Main", (0, 0.020, 0.04), (0.040, 0.066, 0.22), m_gunmetal))
    parts.append(add_box("Ejection_Port_Cutout", (0.019, 0.030, 0.02), (0.006, 0.028, 0.068), m_gunmetal))
    parts.append(add_box("Loading_Lifter", (0, -0.014, 0.03), (0.026, 0.010, 0.078), m_gunmetal))
    
    # 2. 12-Gauge Heavy Barrel & Ventilated Heat Shield
    parts.append(add_cylinder("Barrel_12G", (0, 0.040, -0.33), 0.014, 0.54, rotation=(math.radians(90), 0, 0), material=m_gunmetal))
    parts.append(add_box("Heat_Shield", (0, 0.052, -0.29), (0.032, 0.020, 0.38), m_gunmetal))
    parts.append(add_uv_sphere("Front_Bead", (0, 0.056, -0.58), 0.004, m_bead))
    
    # 3. Full-Length Extended Magazine Tube
    parts.append(add_cylinder("Mag_Tube", (0, 0.013, -0.31), 0.015, 0.52, rotation=(math.radians(90), 0, 0), material=m_gunmetal))
    parts.append(add_box("Barrel_Clamp", (0, 0.026, -0.52), (0.034, 0.048, 0.022), m_gunmetal))
    
    # 4. Ribbed Tactical Pump Forend Slide
    parts.append(add_cylinder("Pump_Forend", (0, 0.013, -0.25), 0.024, 0.21, rotation=(math.radians(90), 0, 0), material=m_synthetic))
    for z_rib in [-0.17, -0.21, -0.25, -0.29, -0.33]:
        parts.append(add_cylinder(f"Pump_Rib_{z_rib}", (0, 0.013, z_rib), 0.026, 0.014, rotation=(math.radians(90), 0, 0), material=m_synthetic))
        
    # 5. Trigger Guard, Trigger, and Safety
    parts.append(add_box("Trigger_Guard", (0, -0.028, 0.06), (0.015, 0.034, 0.055), m_synthetic))
    parts.append(add_box("Trigger_Curved", (0, -0.024, 0.065), (0.006, 0.022, 0.014), m_gunmetal))
    parts.append(add_cylinder("Crossbolt_Safety", (0, -0.015, 0.09), 0.005, 0.024, rotation=(0, 0, math.radians(90)), material=m_gunmetal))
    
    # 6. Full Tactical Synthetic Stock with Pistol Grip
    parts.append(add_box("Stock_Wrist", (0, -0.006, 0.17), (0.034, 0.060, 0.085), m_synthetic))
    parts.append(add_box("Pistol_Grip", (0, -0.078, 0.14), (0.034, 0.114, 0.050), m_synthetic))
    parts.append(add_box("Buttstock_Body", (0, -0.022, 0.30), (0.038, 0.098, 0.21), m_synthetic))
    parts.append(add_box("Recoil_Pad", (0, -0.026, 0.405), (0.040, 0.128, 0.026), m_rubber))
    
    shotgun_obj = join_objects(parts, "Shotgun_Remington870")
    export_obj('models/weapons/shotgun.obj')
    
    # Add MuzzleSocket
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0.040, -0.60))
    socket = bpy.context.active_object
    socket.name = "MuzzleSocket"
    socket.parent = shotgun_obj
    
    export_glb('assets/3d/weapons/shotgun.glb', 'tools/blender/generated/shotgun.blend')

if __name__ == '__main__':
    build_usp45_pistol()
    build_m4a1_rifle()
    build_remington870_shotgun()
    print("ALL 3 HIGH-VISIBILITY TACTICAL WEAPONS SUCCESSFULLY BUILT!")
