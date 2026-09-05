"""
Sector Zero: Lockdown - Master Realistic Vertical Slice Pipeline
Generates AAA-inspired, anatomically believable models:
1. Realistic Human Survivor (player_soldier.glb / .obj)
2. Realistic Normal Zombie with human facial anatomy & clothing (zombie_normal.glb / .obj)
3. Realistic Tactical USP-45 Pistol (pistol.glb / .obj)
4. Realistic First-Person FPS Arms with 2-Handed Combat Grip (fps_arms.glb / .obj)
5. Cinematic Airport Terminal with Interior/Exterior Depth & Props (airport_terminal.glb)

Engine: Godot 4.5.1 | Blender: 4.0.2 Headless | 100% Original Procedural Pipeline
"""

import bpy
import bmesh
import math
import os

# ==============================================================================
# 0. CORE UTILITIES & PBR MATERIALS
# ==============================================================================

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for collection in [bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.armatures, bpy.data.actions]:
        for item in list(collection):
            collection.remove(item, do_unlink=True)

def create_mat(name, base_color=(0.5, 0.5, 0.5, 1.0), metallic=0.0, roughness=0.5, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if emission:
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

def add_box(name, loc, size, mat=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj

def add_cyl(name, loc, r, d, rot=(0,0,0), mat=None, verts=16, smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=verts)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        for p in obj.data.polygons: p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj

def add_sphere(name, loc, r, mat=None, segs=16, rings=12, smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=segs, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        for p in obj.data.polygons: p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj

def join_all(objs, final_name):
    valid = [o for o in objs if o and o.name in bpy.data.objects]
    if not valid: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in valid: o.select_set(True)
    bpy.context.view_layer.objects.active = valid[0]
    bpy.ops.object.join()
    res = bpy.context.active_object
    res.name = final_name
    return res

def export_assets(glb_path, obj_path=None, blend_path=None):
    os.makedirs(os.path.dirname(glb_path), exist_ok=True)
    if blend_path:
        os.makedirs(os.path.dirname(blend_path), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True,
        export_materials='EXPORT',
        export_animations=True
    )
    print(f"Exported GLB: {glb_path} ({os.path.getsize(glb_path)} bytes)")
    if obj_path:
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True, export_selected_objects=False)
        print(f"Exported OBJ: {obj_path} ({os.path.getsize(obj_path)} bytes)")


# ==============================================================================
# 1. REALISTIC HUMAN SURVIVOR (player_soldier.glb / .obj)
# ==============================================================================

def build_realistic_soldier():
    print("\n--- 1. BUILDING REALISTIC HUMAN SURVIVOR CHARACTER ---")
    clear_scene()
    
    # Materials
    m_skin = create_mat("Mat_HumanSkin", (0.78, 0.62, 0.52, 1.0), roughness=0.55)
    m_eyes = create_mat("Mat_HumanEyes", (0.92, 0.92, 0.92, 1.0), roughness=0.08)
    m_hair = create_mat("Mat_Hair", (0.12, 0.10, 0.09, 1.0), roughness=0.85)
    m_shirt = create_mat("Mat_CombatShirt", (0.26, 0.30, 0.22, 1.0), roughness=0.80)
    m_vest = create_mat("Mat_PlateCarrier", (0.16, 0.18, 0.15, 1.0), roughness=0.75)
    m_web = create_mat("Mat_MolleWebbing", (0.08, 0.08, 0.09, 1.0), roughness=0.85)
    m_pouch = create_mat("Mat_MagPouches", (0.12, 0.14, 0.11, 1.0), roughness=0.78)
    m_pants = create_mat("Mat_CargoPants", (0.20, 0.22, 0.18, 1.0), roughness=0.82)
    m_boot = create_mat("Mat_TacticalBoots", (0.06, 0.06, 0.07, 1.0), roughness=0.65)
    m_pad = create_mat("Mat_KneePads", (0.10, 0.10, 0.11, 1.0), roughness=0.45)
    m_glove = create_mat("Mat_TacticalGloves", (0.14, 0.15, 0.16, 1.0), roughness=0.70)
    m_carbon = create_mat("Mat_CarbonKnuckles", (0.05, 0.05, 0.06, 1.0), metallic=0.35, roughness=0.25)
    m_gear = create_mat("Mat_BeltHolster", (0.08, 0.08, 0.09, 1.0), metallic=0.4, roughness=0.5)
    
    parts = []
    
    # --- HEAD & ANATOMICAL FACE ---
    # Cranium (smooth skull base)
    parts.append(add_sphere("Head_Cranium", (0, 1.66, -0.015), 0.108, m_skin, segs=20, rings=16))
    
    # Forehead and Brow ridge
    parts.append(add_box("Face_Brow", (0, 1.66, 0.082), (0.13, 0.032, 0.045), m_skin))
    
    # Left and Right Eyeballs in recessed sockets
    parts.append(add_sphere("Eye_L", (-0.038, 1.65, 0.085), 0.016, m_eyes, segs=12, rings=10))
    parts.append(add_sphere("Eye_R", (0.038, 1.65, 0.085), 0.016, m_eyes, segs=12, rings=10))
    
    # Eyelid borders
    parts.append(add_box("Eyelid_L", (-0.038, 1.662, 0.088), (0.036, 0.012, 0.018), m_skin))
    parts.append(add_box("Eyelid_R", (0.038, 1.662, 0.088), (0.036, 0.012, 0.018), m_skin))
    
    # Nose (bridge and nostrils)
    parts.append(add_box("Face_Nose", (0, 1.615, 0.105), (0.032, 0.046, 0.036), m_skin))
    
    # Cheekbones & Temples
    parts.append(add_box("Face_Cheek_L", (-0.065, 1.61, 0.065), (0.038, 0.06, 0.06), m_skin))
    parts.append(add_box("Face_Cheek_R", (0.065, 1.61, 0.065), (0.038, 0.06, 0.06), m_skin))
    
    # Mouth (upper and lower lips)
    parts.append(add_box("Face_Lips", (0, 1.572, 0.092), (0.054, 0.018, 0.022), m_skin))
    
    # Jaw and Chin
    parts.append(add_box("Face_Jaw", (0, 1.530, 0.065), (0.082, 0.065, 0.085), m_skin))
    
    # Ears (anatomical helix and lobe)
    parts.append(add_box("Ear_L", (-0.112, 1.63, 0.0), (0.022, 0.055, 0.036), m_skin))
    parts.append(add_box("Ear_R", (0.112, 1.63, 0.0), (0.022, 0.055, 0.036), m_skin))
    
    # Tactical Hair (military crew cut)
    parts.append(add_sphere("Hair_Crown", (0, 1.685, -0.02), 0.114, m_hair, segs=16, rings=12))
    
    # Neck with sternocleidomastoid angles
    parts.append(add_cyl("Neck", (0, 1.48, 0.0), 0.068, 0.14, mat=m_skin, verts=16))
    
    # --- TORSO & TACTICAL GEAR ---
    # Combat shirt torso base
    parts.append(add_box("Shirt_Torso", (0, 1.25, 0.0), (0.38, 0.40, 0.22), m_shirt))
    # Mandarin shirt collar
    parts.append(add_cyl("Shirt_Collar", (0, 1.42, 0.0), 0.082, 0.055, mat=m_shirt, verts=16))
    
    # Ballistic Plate Carrier (Front & Back armor plates with depth)
    parts.append(add_box("Armor_Front", (0, 1.26, 0.055), (0.34, 0.36, 0.16), m_vest))
    parts.append(add_box("Armor_Back", (0, 1.26, -0.055), (0.34, 0.36, 0.16), m_vest))
    # Shoulder retention straps
    parts.append(add_box("Armor_Strap_L", (-0.12, 1.42, 0.0), (0.065, 0.075, 0.22), m_vest))
    parts.append(add_box("Armor_Strap_R", (0.12, 1.42, 0.0), (0.065, 0.075, 0.22), m_vest))
    
    # MOLLE Webbing Rows
    for y_offset in [1.18, 1.24, 1.30, 1.36]:
        parts.append(add_box(f"Molle_Row_{y_offset}", (0, y_offset, 0.142), (0.28, 0.018, 0.012), m_web))
        
    # 3x STANAG Magazine Pouches across lower stomach
    for x_pouch in [-0.085, 0.0, 0.085]:
        parts.append(add_box(f"Mag_Pouch_{x_pouch}", (x_pouch, 1.15, 0.155), (0.072, 0.125, 0.045), m_pouch))
        # Pouch pull-tab bungee
        parts.append(add_box(f"Pouch_Tab_{x_pouch}", (x_pouch, 1.22, 0.162), (0.035, 0.025, 0.015), m_web))
        
    # Tactical Comms Radio with antenna on upper-left chest
    parts.append(add_box("Radio_Pouch", (-0.12, 1.31, 0.150), (0.055, 0.095, 0.045), m_pouch))
    parts.append(add_cyl("Radio_Antenna", (-0.135, 1.44, 0.150), 0.004, 0.16, mat=m_gear, verts=8))
    
    # Medical IFAK pouch on right flank
    parts.append(add_box("IFAK_Pouch", (0.19, 1.10, 0.035), (0.075, 0.095, 0.070), m_pouch))
    
    # Combat Duty Belt & Cobra Buckle
    parts.append(add_box("Duty_Belt", (0, 0.99, 0.0), (0.34, 0.065, 0.22), m_gear))
    parts.append(add_box("Belt_Buckle", (0, 0.99, 0.115), (0.062, 0.045, 0.022), m_gear))
    
    # Tactical Holster on right hip with sidearm grip
    parts.append(add_box("Hip_Holster", (0.20, 0.89, 0.02), (0.065, 0.165, 0.085), m_gear))
    
    # --- ARMS, GLOVES & ARTICULATED FINGERS ---
    for side, sign in [("L", -1), ("R", 1)]:
        # Shoulder Deltoid
        parts.append(add_sphere(f"Deltoid_{side}", (sign * 0.24, 1.34, 0.0), 0.078, m_shirt, segs=14, rings=10))
        # Upper Arm Sleeve
        parts.append(add_cyl(f"Arm_Upper_{side}", (sign * 0.26, 1.16, 0.0), 0.064, 0.24, mat=m_shirt, verts=14))
        # Sleeve cuff seam
        parts.append(add_cyl(f"Sleeve_Cuff_{side}", (sign * 0.26, 1.03, 0.0), 0.069, 0.035, mat=m_shirt, verts=14))
        
        # Muscular Bare Forearm
        parts.append(add_cyl(f"Forearm_{side}", (sign * 0.26, 0.90, 0.03), 0.052, 0.24, mat=m_skin, verts=14))
        # Wrist joint
        parts.append(add_cyl(f"Wrist_{side}", (sign * 0.26, 0.77, 0.05), 0.044, 0.055, mat=m_skin, verts=14))
        
        # Tactical Glove (Palm & Back of Hand)
        parts.append(add_box(f"Glove_Palm_{side}", (sign * 0.26, 0.71, 0.06), (0.085, 0.085, 0.045), m_glove))
        # Molded Carbon Fiber Knuckle Shell
        parts.append(add_box(f"Knuckle_Plate_{side}", (sign * 0.26, 0.725, 0.085), (0.076, 0.028, 0.022), m_carbon))
        
        # 5 Articulated Glove Fingers
        # Thumb
        parts.append(add_cyl(f"Finger_Thumb_{side}", (sign * 0.215, 0.69, 0.085), 0.013, 0.050, rot=(0.35, sign * 0.4, 0), mat=m_glove, verts=8))
        # Index
        parts.append(add_cyl(f"Finger_Index_{side}", (sign * 0.238, 0.64, 0.060), 0.012, 0.058, mat=m_glove, verts=8))
        # Middle
        parts.append(add_cyl(f"Finger_Mid_{side}", (sign * 0.258, 0.63, 0.060), 0.013, 0.064, mat=m_glove, verts=8))
        # Ring
        parts.append(add_cyl(f"Finger_Ring_{side}", (sign * 0.278, 0.64, 0.060), 0.012, 0.058, mat=m_glove, verts=8))
        # Pinky
        parts.append(add_cyl(f"Finger_Pinky_{side}", (sign * 0.298, 0.65, 0.060), 0.011, 0.048, mat=m_glove, verts=8))
        
    # --- LEGS & COMBAT BOOTS ---
    # Pelvis & Trousers upper
    parts.append(add_box("Pants_Pelvis", (0, 0.94, 0.0), (0.32, 0.14, 0.20), m_pants))
    
    for side, sign in [("L", -1), ("R", 1)]:
        # Thigh with cargo pocket
        parts.append(add_cyl(f"Leg_Thigh_{side}", (sign * 0.11, 0.72, 0.0), 0.085, 0.36, mat=m_pants, verts=14))
        parts.append(add_box(f"Cargo_Pocket_{side}", (sign * 0.205, 0.72, 0.0), (0.045, 0.145, 0.115), m_pants))
        
        # Hard-shell Tactical Knee Pad
        parts.append(add_box(f"Knee_Pad_{side}", (sign * 0.11, 0.50, 0.062), (0.105, 0.125, 0.055), m_pad))
        parts.append(add_box(f"Knee_Strap_{side}", (sign * 0.11, 0.50, 0.0), (0.165, 0.045, 0.165), m_web))
        
        # Shin / Bloused trouser leg
        parts.append(add_cyl(f"Leg_Shin_{side}", (sign * 0.11, 0.29, 0.0), 0.074, 0.34, mat=m_pants, verts=14))
        
        # Tactical Combat Boot: Lugged sole, leather body, toe cap, lacing tongue
        parts.append(add_box(f"Boot_Sole_{side}", (sign * 0.11, 0.028, 0.038), (0.115, 0.055, 0.255), m_boot))
        parts.append(add_box(f"Boot_Upper_{side}", (sign * 0.11, 0.095, 0.035), (0.105, 0.095, 0.235), m_boot))
        parts.append(add_box(f"Boot_ToeCap_{side}", (sign * 0.11, 0.065, 0.135), (0.095, 0.055, 0.075), m_boot))
        parts.append(add_cyl(f"Boot_Ankle_{side}", (sign * 0.11, 0.175, 0.015), 0.072, 0.11, mat=m_boot, verts=12))

    soldier_obj = join_all(parts, "PlayerSoldier")
    export_assets(
        'assets/3d/characters/player_soldier.glb',
        'models/player/player_soldier.obj',
        'tools/blender/generated/player_soldier.blend'
    )
    print("Realistic Soldier successfully generated!")


# ==============================================================================
# 2. REALISTIC NORMAL ZOMBIE (zombie_normal.glb / .obj)
# ==============================================================================

def build_realistic_normal_zombie():
    print("\n--- 2. BUILDING REALISTIC NORMAL ZOMBIE (HUMANOID INFECTED) ---")
    clear_scene()
    
    # Materials
    m_flesh = create_mat("Mat_ZombieFlesh", (0.52, 0.62, 0.48, 1.0), roughness=0.62)
    m_gore = create_mat("Mat_ZombieGore", (0.78, 0.06, 0.05, 1.0), roughness=0.22, metallic=0.12)
    m_bone = create_mat("Mat_ZombieBone", (0.88, 0.85, 0.74, 1.0), roughness=0.45)
    m_shirt = create_mat("Mat_ZombieTornShirt", (0.38, 0.40, 0.42, 1.0), roughness=0.88)
    m_pants = create_mat("Mat_ZombieTornPants", (0.14, 0.16, 0.20, 1.0), roughness=0.85)
    m_eye_blood = create_mat("Mat_ZombieEyeBlood", (0.95, 0.15, 0.10, 1.0), emission=(0.95, 0.15, 0.10, 1.0), emission_strength=3.2)
    m_eye_milky = create_mat("Mat_ZombieEyeMilky", (0.72, 0.76, 0.72, 1.0), roughness=0.35)
    m_hair = create_mat("Mat_ZombieHair", (0.10, 0.09, 0.08, 1.0), roughness=0.90)
    m_shoe = create_mat("Mat_ZombieShoe", (0.08, 0.07, 0.07, 1.0), roughness=0.75)
    
    parts = []
    
    # --- GAUNT ASYMMETRICAL HUMAN SKULL & DAMAGED FACE ---
    # Cranium (hollowed, asymmetrical)
    parts.append(add_sphere("ZHead_Cranium", (0.01, 1.63, 0.02), 0.106, m_flesh, segs=20, rings=16))
    
    # Sunken Eye Sockets
    parts.append(add_box("ZFace_Brow", (0.01, 1.635, 0.115), (0.125, 0.030, 0.040), m_flesh))
    
    # Left Eye: Glazed Milky Cataract Blind Eye
    parts.append(add_sphere("ZEye_L", (-0.038, 1.625, 0.115), 0.017, m_eye_milky, segs=12, rings=10))
    # Right Eye: Bulging, Bloodshot Infected Eye with Glowing Amber Pupil
    parts.append(add_sphere("ZEye_R", (0.040, 1.625, 0.122), 0.019, m_eye_blood, segs=12, rings=10))
    
    # Decayed Nasal Cavity (Eroded bridge)
    parts.append(add_box("ZFace_Nose", (0.01, 1.585, 0.132), (0.028, 0.036, 0.030), m_flesh))
    parts.append(add_box("ZNasal_Hole", (0.01, 1.580, 0.142), (0.018, 0.018, 0.015), m_gore))
    
    # Slack, Unhinged Jaw (tilted and hanging open in a snarl)
    parts.append(add_box("ZFace_Jaw", (0.018, 1.505, 0.095), (0.080, 0.065, 0.080), m_flesh, rot=(0.18, 0.0, -0.14)))
    
    # Exposed Broken Teeth & Gums inside mouth cavity
    parts.append(add_box("ZTeeth_Upper", (0.012, 1.545, 0.128), (0.062, 0.015, 0.020), m_bone))
    parts.append(add_box("ZTeeth_Lower", (0.020, 1.520, 0.120), (0.058, 0.015, 0.018), m_bone))
    
    # Right Cheek: Massive Torn Laceration exposing jawbone & gore
    parts.append(add_box("ZWound_Cheek", (0.065, 1.555, 0.095), (0.035, 0.055, 0.045), m_gore))
    parts.append(add_box("ZBone_Cheek", (0.062, 1.555, 0.105), (0.015, 0.035, 0.020), m_bone))
    
    # Decayed Hair Strands
    parts.append(add_sphere("ZHair_Patch", (0.0, 1.66, 0.01), 0.112, m_hair, segs=14, rings=10))
    
    # Asymmetrical Tilting Neck with Jagged Bite Wound
    parts.append(add_cyl("ZNeck", (0.015, 1.46, 0.02), 0.065, 0.14, rot=(0.12, 0.0, 0.08), mat=m_flesh, verts=14))
    parts.append(add_box("ZNeck_Bite", (-0.042, 1.47, 0.045), (0.035, 0.045, 0.035), m_gore))
    
    # --- TORSO WITH TORN COMMUTER SHIRT & EXPOSED RIBCAGE ---
    # Stooped, asymmetrical upper torso
    parts.append(add_box("ZTorso_Main", (0.0, 1.22, 0.03), (0.35, 0.42, 0.22), m_shirt, rot=(0.12, -0.05, 0.04)))
    # Torn open collar
    parts.append(add_cyl("ZTorn_Collar", (0.01, 1.39, 0.03), 0.082, 0.05, mat=m_shirt, verts=14))
    
    # Exposed Clavicle Wound on chest
    parts.append(add_box("ZWound_Chest", (-0.05, 1.34, 0.13), (0.09, 0.06, 0.03), m_gore))
    parts.append(add_box("ZBone_Clavicle", (-0.05, 1.35, 0.14), (0.08, 0.015, 0.015), m_bone))
    
    # Right Ribcage: Massive Open Cavity with Fractured Ribs
    parts.append(add_box("ZWound_Ribs", (0.12, 1.18, 0.11), (0.12, 0.18, 0.07), m_gore))
    parts.append(add_box("ZRib_1", (0.12, 1.24, 0.14), (0.095, 0.018, 0.025), m_bone))
    parts.append(add_box("ZRib_2", (0.12, 1.18, 0.14), (0.090, 0.018, 0.025), m_bone))
    parts.append(add_box("ZRib_3", (0.12, 1.12, 0.14), (0.085, 0.018, 0.025), m_bone))
    
    # --- ASYMMETRICAL ARMS & INFECTED CLAWS ---
    # Left Arm (Raised aggressively forward at 75 degrees)
    parts.append(add_sphere("ZShoulder_L", (-0.23, 1.32, 0.05), 0.072, m_shirt))
    parts.append(add_cyl("ZArm_Upper_L", (-0.24, 1.28, 0.18), 0.056, 0.26, rot=(math.radians(72), 0, 0), mat=m_shirt, verts=12))
    # Ragged sleeve edge
    parts.append(add_cyl("ZTorn_Sleeve_L", (-0.24, 1.26, 0.28), 0.062, 0.03, rot=(math.radians(72), 0, 0), mat=m_shirt, verts=12))
    # Rotting forearm
    parts.append(add_cyl("ZForearm_L", (-0.24, 1.22, 0.42), 0.046, 0.26, rot=(math.radians(82), 0, 0), mat=m_flesh, verts=12))
    # Splayed clawed hand
    parts.append(add_box("ZHand_L", (-0.24, 1.20, 0.56), (0.075, 0.075, 0.040), m_flesh))
    for f_idx, fx in enumerate([-0.27, -0.255, -0.24, -0.225, -0.21]):
        parts.append(add_cyl(f"ZClaw_L_{f_idx}", (fx, 1.19, 0.61), 0.009, 0.055, rot=(math.radians(90), 0, 0), mat=m_flesh, verts=6))
        # Jagged blackened fingernail
        parts.append(add_box(f"ZNail_L_{f_idx}", (fx, 1.19, 0.645), (0.010, 0.006, 0.018), m_bone))
        
    # Right Arm (Dangling loosely with deep infected laceration)
    parts.append(add_sphere("ZShoulder_R", (0.23, 1.28, 0.02), 0.070, m_shirt))
    parts.append(add_cyl("ZArm_Upper_R", (0.24, 1.10, 0.08), 0.054, 0.24, rot=(math.radians(25), 0, 0), mat=m_shirt, verts=12))
    parts.append(add_cyl("ZForearm_R", (0.24, 0.88, 0.16), 0.044, 0.24, rot=(math.radians(35), 0, 0), mat=m_flesh, verts=12))
    # Forearm laceration
    parts.append(add_box("ZWound_Forearm_R", (0.25, 0.88, 0.19), (0.025, 0.10, 0.025), m_gore))
    parts.append(add_box("ZHand_R", (0.24, 0.73, 0.22), (0.070, 0.070, 0.040), m_flesh))
    
    # --- TORN COMMUTER TROUSERS & LACERATED LEGS ---
    parts.append(add_box("ZPants_Pelvis", (0.0, 0.94, 0.01), (0.30, 0.14, 0.18), m_pants))
    
    # Left Leg (Torn knee showing patella bone)
    parts.append(add_cyl("ZThigh_L", (-0.10, 0.71, 0.0), 0.076, 0.36, mat=m_pants, verts=12))
    parts.append(add_box("ZWound_Knee_L", (-0.10, 0.50, 0.065), (0.085, 0.095, 0.045), m_gore))
    parts.append(add_sphere("ZPatella_L", (-0.10, 0.50, 0.080), 0.028, m_bone, segs=8, rings=8))
    parts.append(add_cyl("ZShin_L", (-0.10, 0.28, 0.0), 0.066, 0.34, mat=m_pants, verts=12))
    parts.append(add_box("ZShoe_L", (-0.10, 0.045, 0.035), (0.105, 0.075, 0.235), m_shoe))
    # Ripped shoe toe showing decayed toes
    parts.append(add_box("ZToes_L", (-0.10, 0.035, 0.145), (0.085, 0.040, 0.040), m_flesh))
    
    # Right Leg (Shredded lower pant leg)
    parts.append(add_cyl("ZThigh_R", (0.10, 0.71, 0.0), 0.076, 0.36, mat=m_pants, verts=12))
    parts.append(add_cyl("ZShin_R", (0.10, 0.28, 0.0), 0.062, 0.34, mat=m_flesh, verts=12)) # Shredded pant
    parts.append(add_box("ZTorn_Pant_R", (0.10, 0.40, 0.0), (0.155, 0.10, 0.155), m_pants))
    parts.append(add_box("ZShoe_R", (0.10, 0.045, 0.035), (0.105, 0.075, 0.235), m_shoe))

    zombie_obj = join_all(parts, "ZombieNormal")
    export_assets(
        'assets/3d/zombies/zombie_normal.glb',
        'models/zombies/zombie_normal.obj',
        'tools/blender/generated/zombie_normal.blend'
    )
    print("Realistic Normal Zombie successfully generated!")


# ==============================================================================
# 3. REALISTIC TACTICAL USP-45 PISTOL (pistol.glb / .obj)
# ==============================================================================

def build_realistic_tactical_pistol():
    print("\n--- 3. BUILDING REALISTIC TACTICAL USP-45 PISTOL ---")
    clear_scene()
    
    # Materials
    m_steel = create_mat("Mat_PistolSteel", (0.38, 0.40, 0.44, 1.0), metallic=0.88, roughness=0.28)
    m_poly = create_mat("Mat_PistolPolymer", (0.15, 0.16, 0.17, 1.0), metallic=0.05, roughness=0.72)
    m_barrel = create_mat("Mat_PistolBarrel", (0.58, 0.60, 0.64, 1.0), metallic=0.95, roughness=0.18)
    m_tritium = create_mat("Mat_TritiumDot", (0.2, 1.0, 0.4, 1.0), emission=(0.2, 1.0, 0.4, 1.0), emission_strength=6.0)
    m_parts = create_mat("Mat_PistolDetails", (0.25, 0.26, 0.28, 1.0), metallic=0.85, roughness=0.35)
    
    parts = []
    
    # --- SLIDE & BARREL ASSEMBLY ---
    # Slide Body
    parts.append(add_box("Pistol_Slide", (0, 0.052, -0.02), (0.032, 0.038, 0.198), m_steel))
    
    # Chamfered Top Bevel
    parts.append(add_box("Slide_TopBevel", (0, 0.071, -0.02), (0.024, 0.005, 0.194), m_steel))
    
    # Front Cocking Serrations (4 grooves per side)
    for i in range(4):
        z_pos = -0.075 - (i * 0.008)
        parts.append(add_box(f"FrontSerr_L_{i}", (-0.0162, 0.052, z_pos), (0.002, 0.028, 0.004), m_parts))
        parts.append(add_box(f"FrontSerr_R_{i}", (0.0162, 0.052, z_pos), (0.002, 0.028, 0.004), m_parts))
        
    # Rear Cocking Serrations (6 grooves per side)
    for i in range(6):
        z_pos = 0.040 + (i * 0.006)
        parts.append(add_box(f"RearSerr_L_{i}", (-0.0162, 0.052, z_pos), (0.002, 0.028, 0.0035), m_parts))
        parts.append(add_box(f"RearSerr_R_{i}", (0.0162, 0.052, z_pos), (0.002, 0.028, 0.0035), m_parts))
        
    # Open Ejection Port cutout & Barrel Hood
    parts.append(add_box("Barrel_Hood", (0.006, 0.054, -0.015), (0.022, 0.024, 0.042), m_barrel))
    parts.append(add_box("Extractor_Claw", (0.0168, 0.054, -0.012), (0.003, 0.007, 0.028), m_parts))
    
    # Recessed Rifled Muzzle Barrel
    parts.append(add_cyl("Barrel_Muzzle", (0, 0.050, -0.122), 0.0075, 0.026, rot=(math.radians(90), 0, 0), mat=m_barrel, verts=16))
    parts.append(add_cyl("Muzzle_Bore", (0, 0.050, -0.134), 0.0055, 0.008, rot=(math.radians(90), 0, 0), mat=m_poly, verts=12))
    
    # Recoil Spring Guide Rod & Plug
    parts.append(add_cyl("Guide_Rod", (0, 0.036, -0.121), 0.0045, 0.020, rot=(math.radians(90), 0, 0), mat=m_parts, verts=12))
    
    # --- TRITIUM 3-DOT COMBAT SIGHTS ---
    # Front Sight Blade & Tritium Dot
    parts.append(add_box("Sight_Front", (0, 0.076, -0.110), (0.005, 0.010, 0.012), m_steel))
    parts.append(add_sphere("Tritium_Front", (0, 0.077, -0.106), 0.0022, m_tritium, segs=8, rings=6))
    
    # Rear Sight Notch & 2x Tritium Dots
    parts.append(add_box("Sight_Rear_L", (-0.0085, 0.076, 0.072), (0.007, 0.011, 0.014), m_steel))
    parts.append(add_box("Sight_Rear_R", (0.0085, 0.076, 0.072), (0.007, 0.011, 0.014), m_steel))
    parts.append(add_box("Sight_Rear_Base", (0, 0.072, 0.072), (0.024, 0.004, 0.014), m_steel))
    parts.append(add_sphere("Tritium_Rear_L", (-0.0085, 0.077, 0.067), 0.0020, m_tritium, segs=8, rings=6))
    parts.append(add_sphere("Tritium_Rear_R", (0.0085, 0.077, 0.067), 0.0020, m_tritium, segs=8, rings=6))
    
    # --- POLYMER RECEIVER FRAME & CONTROLS ---
    # Frame Dustcover & Tactical Rail
    parts.append(add_box("Frame_Rail", (0, 0.026, -0.065), (0.028, 0.018, 0.105), m_poly))
    # Rail Cross-slots
    parts.append(add_box("Rail_Slot_1", (0, 0.017, -0.075), (0.030, 0.003, 0.005), m_parts))
    parts.append(add_box("Rail_Slot_2", (0, 0.017, -0.055), (0.030, 0.003, 0.005), m_parts))
    
    # Ergonomic Contoured Grip with Stippled Side Panels
    parts.append(add_box("Grip_Main", (0, -0.035, 0.035), (0.034, 0.125, 0.054), m_poly, rot=(math.radians(12), 0, 0)))
    parts.append(add_box("Grip_Stipple_L", (-0.0175, -0.035, 0.035), (0.002, 0.095, 0.038), m_steel, rot=(math.radians(12), 0, 0)))
    parts.append(add_box("Grip_Stipple_R", (0.0175, -0.035, 0.035), (0.002, 0.095, 0.038), m_steel, rot=(math.radians(12), 0, 0)))
    
    # Trigger Guard with High Undercut & Finger Hook
    parts.append(add_box("Trigger_Guard_Bottom", (0, -0.006, -0.028), (0.014, 0.004, 0.055), m_poly))
    parts.append(add_box("Trigger_Guard_Front", (0, 0.012, -0.052), (0.014, 0.036, 0.005), m_poly))
    
    # Steel Combat Curved Trigger
    parts.append(add_box("Trigger_Steel", (0, 0.014, -0.024), (0.005, 0.022, 0.012), m_parts, rot=(math.radians(-15), 0, 0)))
    
    # Cocked External Hammer
    parts.append(add_box("Hammer_Cocked", (0, 0.052, 0.086), (0.008, 0.018, 0.014), m_parts, rot=(math.radians(28), 0, 0)))
    
    # Controls: Safety Lever, Slide Stop, Mag Release
    parts.append(add_box("Safety_Lever_L", (-0.018, 0.040, 0.055), (0.004, 0.012, 0.022), m_parts))
    parts.append(add_box("Slide_Stop_L", (-0.018, 0.042, -0.018), (0.004, 0.008, 0.028), m_parts))
    parts.append(add_box("Mag_Release_Paddle", (0, -0.005, -0.002), (0.018, 0.008, 0.010), m_parts))
    
    # Extended Magazine Floorplate with Lanyard Loop
    parts.append(add_box("Mag_Floorplate", (0, -0.098, 0.052), (0.038, 0.015, 0.058), m_poly, rot=(math.radians(12), 0, 0)))
    parts.append(add_box("Lanyard_Loop", (0, -0.106, 0.075), (0.008, 0.008, 0.008), m_parts))

    pistol_obj = join_all(parts, "Pistol_USP45")
    export_assets(
        'assets/3d/weapons/pistol.glb',
        'models/weapons/pistol.obj',
        'tools/blender/generated/pistol.blend'
    )
    print("Realistic Tactical USP-45 Pistol successfully generated!")


# ==============================================================================
# 4. REALISTIC FIRST-PERSON FPS ARMS (fps_arms.glb / .obj)
# ==============================================================================

def build_realistic_fps_arms():
    print("\n--- 4. BUILDING REALISTIC FPS ARMS WITH 2-HANDED COMBAT GRIP ---")
    clear_scene()
    
    # Materials
    m_skin = create_mat("Mat_ArmSkin", (0.84, 0.68, 0.58, 1.0), roughness=0.55)
    m_glove = create_mat("Mat_TacticalGlove", (0.16, 0.17, 0.18, 1.0), roughness=0.70)
    m_carbon = create_mat("Mat_CarbonKnuckle", (0.06, 0.06, 0.07, 1.0), metallic=0.40, roughness=0.22)
    m_sleeve = create_mat("Mat_TacticalSleeve", (0.25, 0.28, 0.22, 1.0), roughness=0.85)
    m_watch_case = create_mat("Mat_WatchCase", (0.08, 0.08, 0.09, 1.0), roughness=0.50)
    m_watch_screen = create_mat("Mat_WatchScreen", (0.2, 0.8, 0.9, 1.0), emission=(0.2, 0.8, 0.9, 1.0), emission_strength=3.0)
    
    parts = []
    
    # --- RIGHT FIRING ARM (ANGLED FROM LOWER-RIGHT TO CENTER) ---
    # Rolled sleeve cuff entering camera view
    parts.append(add_cyl("RSleeve", (0.16, -0.22, -0.12), 0.052, 0.14, rot=(math.radians(-42), math.radians(28), math.radians(-15)), mat=m_sleeve, verts=14))
    
    # Muscular Forearm
    parts.append(add_cyl("RForearm", (0.12, -0.15, -0.20), 0.044, 0.18, rot=(math.radians(-42), math.radians(28), math.radians(-15)), mat=m_skin, verts=14))
    
    # Wrist Joint with Tendon details
    parts.append(add_cyl("RWrist", (0.075, -0.09, -0.27), 0.038, 0.08, rot=(math.radians(-35), math.radians(18), math.radians(-10)), mat=m_skin, verts=12))
    
    # Right Glove Hand (Palm gripped on pistol backstrap)
    parts.append(add_box("RGlove_Palm", (0.045, -0.045, -0.33), (0.055, 0.075, 0.045), m_glove, rot=(math.radians(12), math.radians(5), 0)))
    
    # Molded Carbon Knuckle Armor
    parts.append(add_box("RKnuckle_Plate", (0.062, -0.040, -0.32), (0.024, 0.065, 0.022), m_carbon, rot=(math.radians(12), math.radians(5), 0)))
    
    # Right Thumb (resting forward along the slide/frame)
    parts.append(add_cyl("RThumb", (0.022, -0.020, -0.345), 0.011, 0.055, rot=(math.radians(82), math.radians(5), 0), mat=m_glove, verts=8))
    
    # Right Index Trigger Finger (through trigger guard)
    parts.append(add_cyl("RIndex_Finger", (0.026, -0.028, -0.385), 0.010, 0.050, rot=(math.radians(65), math.radians(12), 0), mat=m_glove, verts=8))
    
    # Right Middle, Ring, Pinky Fingers (wrapped around front strap)
    for idx, (fy, fz) in enumerate([(-0.048, -0.365), (-0.064, -0.362), (-0.078, -0.358)]):
        parts.append(add_box(f"RFinger_{idx}", (0.030, fy, fz), (0.040, 0.014, 0.022), m_glove))
        
    # --- LEFT SUPPORT ARM (ANGLED FROM LOWER-LEFT, CUPS RIGHT HAND) ---
    # Rolled sleeve cuff entering camera view
    parts.append(add_cyl("LSleeve", (-0.16, -0.22, -0.12), 0.052, 0.14, rot=(math.radians(-42), math.radians(-28), math.radians(15)), mat=m_sleeve, verts=14))
    
    # Muscular Forearm
    parts.append(add_cyl("LForearm", (-0.12, -0.15, -0.20), 0.044, 0.18, rot=(math.radians(-42), math.radians(-28), math.radians(15)), mat=m_skin, verts=14))
    
    # Left Wrist with Tactical Watch
    parts.append(add_cyl("LWrist", (-0.075, -0.09, -0.27), 0.038, 0.08, rot=(math.radians(-35), math.radians(-18), math.radians(10)), mat=m_skin, verts=12))
    
    # Tactical Digital Watch on Left Wrist
    parts.append(add_box("Watch_Bezel", (-0.078, -0.075, -0.27), (0.038, 0.016, 0.034), m_watch_case, rot=(math.radians(-35), math.radians(-18), math.radians(10))))
    parts.append(add_box("Watch_Display", (-0.078, -0.066, -0.27), (0.024, 0.003, 0.022), m_watch_screen, rot=(math.radians(-35), math.radians(-18), math.radians(10))))
    
    # Left Glove Hand (Cupping the right hand in authentic 2-handed grip)
    parts.append(add_box("LGlove_Palm", (-0.015, -0.052, -0.34), (0.055, 0.072, 0.045), m_glove, rot=(math.radians(12), math.radians(-10), 0)))
    parts.append(add_box("LKnuckle_Plate", (-0.032, -0.050, -0.34), (0.024, 0.062, 0.022), m_carbon, rot=(math.radians(12), math.radians(-10), 0)))
    
    # Left Thumb (pointing forward along left frame under slide)
    parts.append(add_cyl("LThumb", (-0.008, -0.022, -0.355), 0.011, 0.055, rot=(math.radians(82), math.radians(-5), 0), mat=m_glove, verts=8))
    
    # Left Fingers wrapping around front of right hand
    for idx, (fy, fz) in enumerate([(-0.046, -0.380), (-0.062, -0.378), (-0.076, -0.374), (-0.088, -0.370)]):
        parts.append(add_box(f"LFinger_{idx}", (0.010, fy, fz), (0.048, 0.013, 0.018), m_glove))

    arms_obj = join_all(parts, "FPS_CombatArms")
    export_assets(
        'assets/3d/weapons/fps_arms.glb',
        'models/player/fps_arms.obj',
        'tools/blender/generated/fps_arms.blend'
    )
    print("Realistic First-Person FPS Arms successfully generated!")


# ==============================================================================
# 5. CINEMATIC AIRPORT TERMINAL (airport_terminal.glb)
# ==============================================================================

def build_realistic_airport_terminal():
    print("\n--- 5. BUILDING CINEMATIC AIRPORT TERMINAL WITH DEPTH & PROPS ---")
    clear_scene()
    
    # Materials
    m_tiles = create_mat("Mat_AirportFloorTiles", (0.58, 0.62, 0.68, 1.0), metallic=0.05, roughness=0.25)
    m_glass = create_mat("Mat_CurtainWallGlass", (0.35, 0.48, 0.58, 0.85), metallic=0.15, roughness=0.08)
    m_mullion = create_mat("Mat_SteelMullions", (0.12, 0.13, 0.15, 1.0), metallic=0.85, roughness=0.35)
    m_truss = create_mat("Mat_RoofTrussSteel", (0.22, 0.24, 0.26, 1.0), metallic=0.80, roughness=0.40)
    m_counter = create_mat("Mat_CheckinCounter", (0.85, 0.86, 0.88, 1.0), roughness=0.30)
    m_screen = create_mat("Mat_MonitorScreen", (0.15, 0.45, 0.85, 1.0), emission=(0.15, 0.45, 0.85, 1.0), emission_strength=3.0)
    m_xray = create_mat("Mat_XrayScanner", (0.20, 0.24, 0.28, 1.0), metallic=0.3, roughness=0.55)
    m_led = create_mat("Mat_SecurityLED", (1.0, 0.2, 0.1, 1.0), emission=(1.0, 0.2, 0.1, 1.0), emission_strength=4.0)
    m_seat = create_mat("Mat_AirportSeat", (0.12, 0.18, 0.28, 1.0), roughness=0.60)
    m_pillar = create_mat("Mat_PillarConcrete", (0.48, 0.50, 0.52, 1.0), roughness=0.80)
    m_luggage = create_mat("Mat_LuggageLeather", (0.45, 0.15, 0.12, 1.0), roughness=0.50)
    m_fluorescent = create_mat("Mat_FluorescentLight", (0.95, 0.98, 1.0, 1.0), emission=(0.95, 0.98, 1.0, 1.0), emission_strength=4.5)
    m_blood = create_mat("Mat_FloorBloodDecal", (0.45, 0.04, 0.03, 1.0), metallic=0.1, roughness=0.25)
    m_tarmac = create_mat("Mat_DistantTarmac", (0.08, 0.09, 0.11, 1.0), roughness=0.90)
    
    parts = []
    
    # --- TERMINAL MAIN FLOOR PLATE & GROUT LINES ---
    parts.append(add_box("Floor_Tiles", (0, -0.1, 0), (36.0, 0.2, 36.0), m_tiles))
    
    # Directional guide lines on floor
    parts.append(add_box("NavLine_Yellow", (0, 0.002, 0), (0.25, 0.002, 30.0), m_screen))
    
    # --- REAR GLASS FACADE & DISTANT RUNWAY TARMAC (BACKGROUND DEPTH) ---
    # Glass Curtain Wall spanning 34m x 6m
    parts.append(add_box("Glass_Curtain_Wall", (0, 3.0, -17.8), (34.0, 6.0, 0.08), m_glass))
    
    # Steel Mullions & Transoms (Vertical & Horizontal structural framing)
    for x in range(-16, 17, 4):
        parts.append(add_box(f"Mullion_V_{x}", (x, 3.0, -17.75), (0.14, 6.0, 0.16), m_mullion))
    for y in [1.5, 3.0, 4.5, 6.0]:
        parts.append(add_box(f"Mullion_H_{y}", (0, y, -17.75), (34.0, 0.12, 0.14), m_mullion))
        
    # Distant Tarmac apron outside the glass
    parts.append(add_box("Distant_Tarmac", (0, -0.15, -28.0), (44.0, 0.1, 20.0), m_tarmac))
    # Distant Airliner Fuselage Silhouette outside on tarmac
    parts.append(add_cyl("Airliner_Fuselage", (-8.0, 3.2, -26.0), 1.8, 18.0, rot=(0, math.radians(75), 0), mat=m_mullion, verts=14))
    parts.append(add_box("Airliner_Wing", (-7.0, 2.5, -26.0), (12.0, 0.18, 3.5), m_mullion, rot=(0, math.radians(25), 0)))
    
    # --- ROOF SPACE-FRAME TRUSSES & OVERHEAD LIGHTBOXES ---
    for z_truss in [-12.0, -4.0, 4.0, 12.0]:
        # Main cross-beam
        parts.append(add_box(f"Truss_Beam_{z_truss}", (0, 6.0, z_truss), (35.0, 0.28, 0.28), m_truss))
        # Triangular braces
        for x_brace in range(-14, 15, 4):
            parts.append(add_box(f"Truss_Brace_{z_truss}_{x_brace}", (x_brace, 5.7, z_truss), (1.8, 0.08, 0.08), m_truss, rot=(0, 0, math.radians(35))))
            
    # Suspended Fluorescent Lighting Fixtures with Emissive Tubes
    for lx, lz in [(-6, -8), (6, -8), (-6, 0), (6, 0), (-6, 8), (6, 8)]:
        # Hanger cables
        parts.append(add_cyl(f"Hanger_1_{lx}_{lz}", (lx - 1.2, 5.4, lz), 0.008, 1.2, mat=m_mullion, verts=6))
        parts.append(add_cyl(f"Hanger_2_{lx}_{lz}", (lx + 1.2, 5.4, lz), 0.008, 1.2, mat=m_mullion, verts=6))
        # Light housing box
        parts.append(add_box(f"Light_Housing_{lx}_{lz}", (lx, 4.8, lz), (2.8, 0.12, 0.45), m_mullion))
        # Emissive fluorescent diffuser tube
        parts.append(add_box(f"Light_Tube_{lx}_{lz}", (lx, 4.73, lz), (2.6, 0.04, 0.35), m_fluorescent))
        
    # --- STRUCTURAL CONCRETE PILLARS WITH WARNING STRIPES ---
    for px, pz in [(-7, -7), (7, -7), (-7, 7), (7, 7)]:
        parts.append(add_cyl(f"Pillar_Hex_{px}_{pz}", (px, 3.0, pz), 0.65, 6.0, mat=m_pillar, verts=8))
        # Yellow/Black Danger Chevrons band around pillar waist
        parts.append(add_cyl(f"Pillar_Band_{px}_{pz}", (px, 2.0, pz), 0.67, 0.35, mat=m_screen, verts=8))
        # Fire extinguisher wall cabinet
        parts.append(add_box(f"Fire_Cabinet_{px}_{pz}", (px, 1.5, pz + 0.66), (0.28, 0.65, 0.20), m_led))
        
    # --- CHECK-IN COUNTERS ZONE (FOREGROUND) ---
    for cx, cz in [(0, -10.5), (-6.5, -10.5)]:
        # Main Counter Desk
        parts.append(add_box(f"Desk_Base_{cx}", (cx, 0.55, cz), (3.2, 1.10, 0.85), m_counter))
        parts.append(add_box(f"Desk_Top_{cx}", (cx, 1.12, cz), (3.3, 0.05, 0.95), m_counter))
        # Recessed Luggage Scale Conveyor
        parts.append(add_box(f"Baggage_Scale_{cx}", (cx + 1.2, 0.18, cz + 0.1), (0.85, 0.35, 1.2), m_mullion))
        # Computer Monitors on articulating arm
        parts.append(add_box(f"Monitor_Stand_{cx}", (cx - 0.6, 1.30, cz - 0.15), (0.06, 0.35, 0.06), m_mullion))
        parts.append(add_box(f"Monitor_Screen_{cx}", (cx - 0.6, 1.48, cz - 0.15), (0.45, 0.28, 0.04), m_screen))
        
    # Queue Stanchions with Retractable Belts
    for sx, sz in [(-2.0, -8.0), (0.0, -8.0), (2.0, -8.0)]:
        parts.append(add_cyl(f"Stanchion_Post_{sx}", (sx, 0.45, sz), 0.025, 0.90, mat=m_mullion, verts=8))
        parts.append(add_cyl(f"Stanchion_Base_{sx}", (sx, 0.02, sz), 0.16, 0.04, mat=m_mullion, verts=10))
    parts.append(add_box("Queue_Tape", (0, 0.80, -8.0), (4.0, 0.04, 0.005), m_screen))
    
    # --- SECURITY CHECKPOINT (MIDGROUND) ---
    # Walk-through Security Metal Detector Portal Archway
    parts.append(add_box("Scanner_Pillar_L", (2.4, 1.15, -4.0), (0.12, 2.30, 0.65), m_counter))
    parts.append(add_box("Scanner_Pillar_R", (3.6, 1.15, -4.0), (0.12, 2.30, 0.65), m_counter))
    parts.append(add_box("Scanner_Arch_Top", (3.0, 2.25, -4.0), (1.32, 0.15, 0.65), m_counter))
    # Status LED indicator strip
    parts.append(add_box("Scanner_LED", (3.0, 2.15, -3.67), (0.80, 0.03, 0.02), m_led))
    
    # Baggage X-Ray Conveyor Tunnel Machine
    parts.append(add_box("Xray_Tunnel_Body", (5.8, 0.95, -4.0), (1.4, 1.20, 1.6), m_xray))
    parts.append(add_box("Xray_Lead_Flaps", (5.8, 0.95, -3.19), (0.9, 0.80, 0.02), m_mullion))
    # Roller Conveyor Infeed & Outfeed Tracks
    parts.append(add_box("Xray_Track_In", (5.8, 0.55, -2.0), (0.85, 0.12, 1.4), m_mullion))
    parts.append(add_box("Xray_Track_Out", (5.8, 0.55, -6.0), (0.85, 0.12, 1.4), m_mullion))
    
    # --- AIRPORT WAITING LOUNGE SEATING (MIDGROUND) ---
    for sx, sz, srot in [(-4.0, 2.5, 0), (2.0, 4.0, 0), (-1.5, 7.5, math.radians(45))]:
        # 4-gang connected airport seating bench
        parts.append(add_box(f"Bench_Beam_{sx}_{sz}", (sx, 0.40, sz), (2.6, 0.06, 0.06), m_mullion, rot=(0, srot, 0)))
        for i in range(4):
            seat_x = sx - 0.9 + (i * 0.60)
            parts.append(add_box(f"Seat_Cushion_{sx}_{sz}_{i}", (seat_x, 0.46, sz), (0.46, 0.06, 0.44), m_seat, rot=(0, srot, 0)))
            parts.append(add_box(f"Seat_Back_{sx}_{sz}_{i}", (seat_x, 0.72, sz - 0.20), (0.46, 0.46, 0.06), m_seat, rot=(math.radians(-10), srot, 0)))
            
    # Suspended Flight Schedule Monitors (FIDS) arrays
    for fx, fz in [(-3.0, 0.0), (3.0, 0.0)]:
        parts.append(add_cyl(f"FIDS_Pole_{fx}", (fx, 4.2, fz), 0.035, 1.8, mat=m_mullion, verts=8))
        parts.append(add_box(f"FIDS_Screen_{fx}", (fx, 3.2, fz), (2.2, 0.85, 0.15), m_screen))
        
    # --- STORYTELLING SCATTER & DEBRIS ---
    # Discarded Suitcases
    for lx, lz, lrot, lmat in [(-1.5, -9.0, 25, m_luggage), (1.2, -6.5, -45, m_mullion), (4.5, 1.5, 60, m_luggage), (-3.5, 5.0, 15, m_luggage)]:
        parts.append(add_box(f"Suitcase_{lx}_{lz}", (lx, 0.15, lz), (0.55, 0.28, 0.40), lmat, rot=(0, math.radians(lrot), 0)))
        parts.append(add_box(f"Suitcase_Handle_{lx}_{lz}", (lx, 0.30, lz), (0.16, 0.04, 0.03), m_mullion, rot=(0, math.radians(lrot), 0)))
        
    # Blood Smear & Drag Trail decals on floor near security
    parts.append(add_box("Blood_Trail_1", (1.8, 0.003, -4.5), (1.4, 0.002, 2.8), m_blood, rot=(0, math.radians(20), 0)))
    parts.append(add_box("Blood_Trail_2", (0.5, 0.003, -2.5), (0.9, 0.002, 1.6), m_blood, rot=(0, math.radians(-15), 0)))

    terminal_obj = join_all(parts, "AirportTerminalMesh")
    export_assets(
        'assets/3d/environments/airport_terminal.glb',
        'models/environment/airport/airport_terminal.obj',
        'tools/blender/generated/airport_terminal.blend'
    )
    print("Cinematic Airport Terminal successfully generated!")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':
    print("==================================================================")
    print("STARTING MASTER REALISTIC 3D PIPELINE FOR VERTICAL SLICE")
    print("==================================================================")
    build_realistic_soldier()
    build_realistic_normal_zombie()
    build_realistic_tactical_pistol()
    build_realistic_fps_arms()
    build_realistic_airport_terminal()
    print("\n==================================================================")
    print("ALL 5 REALISTIC ASSETS SUCCESSFULLY GENERATED AND EXPORTED!")
    print("==================================================================")
