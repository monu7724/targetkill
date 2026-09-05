"""
Sector Zero: Lockdown - Master Realistic 3D Pipeline (Phase 2 to 10 Assets)
Generates high-fidelity, AAA-inspired, anatomically believable models for:
- Fast Zombie (zombie_fast.glb / .obj)
- Heavy Zombie Brute (zombie_heavy.glb / .obj)
- Boss Alpha Mutant (zombie_boss.glb / .obj)
- M4A1 Sentinel Assault Rifle (rifle.glb / .obj)
- Remington 870 Tactical Shotgun (shotgun.glb / .obj)
- Railway Station Concourse (railway_station.glb)
- Abandoned Train Carriage (train_carriage.glb)
- Industrial Street (industrial_street.glb)
- Quarantine Boss Arena (boss_arena.glb)
"""

import bpy
import bmesh
import math
import os

# ==============================================================================
# UTILITIES
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
# 1. REALISTIC FAST ZOMBIE (zombie_fast.glb / .obj)
# ==============================================================================

def build_realistic_fast_zombie():
    print("\n--- BUILDING REALISTIC FAST ZOMBIE (ATHLETIC RUNNER) ---")
    clear_scene()
    
    m_skin = create_mat("Mat_ZombieFastSkin", (0.54, 0.64, 0.50, 1.0), roughness=0.58)
    m_gore = create_mat("Mat_ZombieBlood", (0.80, 0.08, 0.06, 1.0), roughness=0.22, metallic=0.15)
    m_bone = create_mat("Mat_ZombieBone", (0.90, 0.88, 0.78, 1.0), roughness=0.42)
    m_cloth = create_mat("Mat_FastTornClothes", (0.65, 0.22, 0.18, 1.0), roughness=0.85) # Torn athletic runner top
    m_shorts = create_mat("Mat_FastShorts", (0.15, 0.18, 0.24, 1.0), roughness=0.82)
    m_eye = create_mat("Mat_FeralEye", (1.0, 0.25, 0.12, 1.0), emission=(1.0, 0.25, 0.12, 1.0), emission_strength=3.8)
    m_shoe = create_mat("Mat_RunningShoe", (0.22, 0.24, 0.28, 1.0), roughness=0.65)
    
    parts = []
    
    # Head & Aggressive Screaming Face (tilted forward aggressively)
    parts.append(add_sphere("FHead", (0, 1.55, 0.18), 0.098, m_skin, segs=18, rings=14))
    # Brow & Dual Bloodshot Glowing Feral Eyes
    parts.append(add_box("FBrow", (0, 1.56, 0.27), (0.115, 0.026, 0.035), m_skin))
    parts.append(add_sphere("FEye_L", (-0.034, 1.55, 0.27), 0.016, m_eye, segs=10, rings=8))
    parts.append(add_sphere("FEye_R", (0.034, 1.55, 0.27), 0.016, m_eye, segs=10, rings=8))
    # Wide screaming jaw with exposed sharp teeth
    parts.append(add_box("FJaw", (0, 1.45, 0.24), (0.075, 0.075, 0.085), m_skin, rot=(math.radians(24), 0, 0)))
    parts.append(add_box("FTeeth", (0, 1.48, 0.28), (0.058, 0.024, 0.020), m_bone))
    
    # Lean Forward-Leaning Torso with Tense Shoulder Muscles
    parts.append(add_box("FTorso", (0, 1.20, 0.08), (0.30, 0.40, 0.18), m_cloth, rot=(math.radians(22), 0, 0)))
    # Open Chest Wound
    parts.append(add_box("FWound_Chest", (0.05, 1.22, 0.20), (0.11, 0.14, 0.04), m_gore, rot=(math.radians(22), 0, 0)))
    parts.append(add_box("FRib_1", (0.05, 1.25, 0.22), (0.085, 0.016, 0.018), m_bone, rot=(math.radians(22), 0, 0)))
    parts.append(add_box("FRib_2", (0.05, 1.19, 0.22), (0.080, 0.016, 0.018), m_bone, rot=(math.radians(22), 0, 0)))
    
    # Arms: Dynamic Sprinting Posture (Right arm forward, left arm back)
    # Right Arm (Pumping forward)
    parts.append(add_cyl("FArm_Upper_R", (0.20, 1.22, 0.18), 0.048, 0.26, rot=(math.radians(65), math.radians(15), 0), mat=m_skin, verts=12))
    parts.append(add_cyl("FArm_Fore_R", (0.24, 1.24, 0.38), 0.038, 0.26, rot=(math.radians(88), math.radians(10), 0), mat=m_skin, verts=12))
    parts.append(add_box("FHand_R", (0.26, 1.25, 0.52), (0.065, 0.065, 0.04), m_skin))
    parts.append(add_box("FClaws_R", (0.26, 1.25, 0.56), (0.055, 0.016, 0.035), m_bone))
    
    # Left Arm (Pumping back)
    parts.append(add_cyl("FArm_Upper_L", (-0.20, 1.18, -0.02), 0.048, 0.26, rot=(math.radians(-45), math.radians(-15), 0), mat=m_skin, verts=12))
    parts.append(add_cyl("FArm_Fore_L", (-0.24, 1.05, -0.18), 0.038, 0.26, rot=(math.radians(-65), math.radians(-10), 0), mat=m_skin, verts=12))
    parts.append(add_box("FHand_L", (-0.26, 0.95, -0.30), (0.065, 0.065, 0.04), m_skin))
    parts.append(add_box("FClaws_L", (-0.26, 0.93, -0.34), (0.055, 0.016, 0.035), m_bone))
    
    # Pelvis & Running Shorts
    parts.append(add_box("FPelvis", (0, 0.92, -0.02), (0.28, 0.14, 0.16), m_shorts))
    
    # Legs: Sprint Stride (Left leg driving forward, right leg trailing back)
    # Left Leg (Forward drive)
    parts.append(add_cyl("FLeg_Thigh_L", (-0.10, 0.76, 0.12), 0.070, 0.36, rot=(math.radians(-32), 0, 0), mat=m_shorts, verts=12))
    parts.append(add_cyl("FLeg_Shin_L", (-0.10, 0.46, 0.26), 0.056, 0.34, rot=(math.radians(20), 0, 0), mat=m_skin, verts=12))
    parts.append(add_box("FShoe_L", (-0.10, 0.22, 0.35), (0.095, 0.065, 0.22), m_shoe, rot=(math.radians(20), 0, 0)))
    
    # Right Leg (Trailing push-off)
    parts.append(add_cyl("FLeg_Thigh_R", (0.10, 0.74, -0.14), 0.070, 0.36, rot=(math.radians(45), 0, 0), mat=m_shorts, verts=12))
    parts.append(add_cyl("FLeg_Shin_R", (0.10, 0.44, -0.34), 0.056, 0.34, rot=(math.radians(-25), 0, 0), mat=m_skin, verts=12))
    parts.append(add_box("FShoe_R", (0.10, 0.18, -0.42), (0.095, 0.065, 0.22), m_shoe, rot=(math.radians(-40), 0, 0)))

    fast_obj = join_all(parts, "ZombieFast")
    export_assets('assets/3d/zombies/zombie_fast.glb', 'models/zombies/zombie_fast.obj', 'tools/blender/generated/zombie_fast.blend')
    print("Realistic Fast Zombie generated successfully!")


# ==============================================================================
# 2. REALISTIC HEAVY ZOMBIE BRUTE (zombie_heavy.glb / .obj)
# ==============================================================================

def build_realistic_heavy_zombie():
    print("\n--- BUILDING REALISTIC HEAVY BRUTE ZOMBIE ---")
    clear_scene()
    
    m_skin = create_mat("Mat_BruteSkin", (0.48, 0.58, 0.46, 1.0), roughness=0.65)
    m_vest = create_mat("Mat_BruteVest", (0.85, 0.45, 0.05, 1.0), roughness=0.75) # Heavy construction safety vest
    m_stripe = create_mat("Mat_ReflectiveStripe", (0.92, 0.95, 0.96, 1.0), metallic=0.2, roughness=0.3, emission=(0.92, 0.95, 0.96, 1.0), emission_strength=1.8)
    m_pants = create_mat("Mat_BruteDenim", (0.14, 0.18, 0.26, 1.0), roughness=0.88)
    m_boots = create_mat("Mat_SteelToeBoots", (0.08, 0.08, 0.09, 1.0), roughness=0.65)
    m_rebar = create_mat("Mat_RebarSpike", (0.35, 0.36, 0.38, 1.0), metallic=0.85, roughness=0.45)
    m_gore = create_mat("Mat_BruteGore", (0.75, 0.06, 0.05, 1.0), roughness=0.20, metallic=0.15)
    m_eye = create_mat("Mat_BruteEyes", (1.0, 0.15, 0.10, 1.0), emission=(1.0, 0.15, 0.10, 1.0), emission_strength=4.0)
    
    parts = []
    
    # Giant Heavy Cranium & Crushed Jaw
    parts.append(add_sphere("BHead", (0, 1.76, 0.05), 0.138, m_skin, segs=20, rings=16))
    parts.append(add_box("BBrow", (0, 1.77, 0.17), (0.165, 0.038, 0.055), m_skin))
    parts.append(add_sphere("BEye_L", (-0.048, 1.75, 0.17), 0.022, m_eye, segs=10, rings=8))
    parts.append(add_sphere("BEye_R", (0.048, 1.75, 0.17), 0.022, m_eye, segs=10, rings=8))
    parts.append(add_box("BJaw", (0, 1.63, 0.14), (0.125, 0.095, 0.115), m_skin))
    parts.append(add_cyl("BNeck", (0, 1.54, 0.02), 0.105, 0.16, mat=m_skin, verts=16))
    
    # Massive Barrel Torso with Torn Safety Vest
    parts.append(add_box("BTorso", (0, 1.24, 0.02), (0.58, 0.52, 0.36), m_vest))
    # Dual Silver Reflective Safety Stripes across chest and back
    parts.append(add_box("BStripe_1", (0, 1.34, 0.205), (0.54, 0.045, 0.015), m_stripe))
    parts.append(add_box("BStripe_2", (0, 1.20, 0.205), (0.54, 0.045, 0.015), m_stripe))
    
    # Industrial Rebar Spike Embedded through Left Shoulder
    parts.append(add_cyl("Rebar_Spike", (-0.38, 1.48, 0.06), 0.022, 0.72, rot=(math.radians(35), math.radians(25), math.radians(-45)), mat=m_rebar, verts=8))
    parts.append(add_box("Rebar_Wound", (-0.38, 1.42, 0.06), (0.12, 0.12, 0.10), m_gore))
    
    # Huge Muscular Arms
    for side, sign in [("L", -1), ("R", 1)]:
        parts.append(add_sphere(f"BDeltoid_{side}", (sign * 0.38, 1.42, 0.02), 0.125, m_skin))
        parts.append(add_cyl(f"BArm_Up_{side}", (sign * 0.42, 1.20, 0.06), 0.095, 0.32, rot=(math.radians(35), sign * math.radians(15), 0), mat=m_skin, verts=14))
        parts.append(add_cyl(f"BArm_Fore_{side}", (sign * 0.44, 0.90, 0.18), 0.082, 0.32, rot=(math.radians(50), sign * math.radians(10), 0), mat=m_skin, verts=14))
        parts.append(add_box(f"BHand_{side}", (sign * 0.45, 0.70, 0.28), (0.135, 0.135, 0.085), m_skin))
        
    # Heavy Duty Work Pants & Thick Steel-Toed Boots
    parts.append(add_box("BPelvis", (0, 0.92, 0.0), (0.48, 0.18, 0.30), m_pants))
    for side, sign in [("L", -1), ("R", 1)]:
        parts.append(add_cyl(f"BLeg_Thigh_{side}", (sign * 0.16, 0.68, 0.0), 0.125, 0.42, mat=m_pants, verts=14))
        parts.append(add_cyl(f"BLeg_Shin_{side}", (sign * 0.16, 0.26, 0.0), 0.108, 0.40, mat=m_pants, verts=14))
        parts.append(add_box(f"BBoot_{side}", (sign * 0.16, 0.045, 0.06), (0.165, 0.095, 0.33), m_boots))

    heavy_obj = join_all(parts, "ZombieHeavy")
    export_assets('assets/3d/zombies/zombie_heavy.glb', 'models/zombies/zombie_heavy.obj', 'tools/blender/generated/zombie_heavy.blend')
    print("Realistic Heavy Brute Zombie generated successfully!")


# ==============================================================================
# 3. REALISTIC BOSS ALPHA MUTANT (zombie_boss.glb / .obj)
# ==============================================================================

def build_realistic_boss():
    print("\n--- BUILDING REALISTIC BOSS ALPHA MUTANT ---")
    clear_scene()
    
    m_flesh = create_mat("Mat_BossFlesh", (0.42, 0.52, 0.40, 1.0), roughness=0.60)
    m_armor = create_mat("Mat_BossArmorCarapace", (0.15, 0.18, 0.16, 1.0), metallic=0.25, roughness=0.35)
    m_spike = create_mat("Mat_BossBoneSpikes", (0.92, 0.90, 0.78, 1.0), roughness=0.38)
    m_vein = create_mat("Mat_BossToxicVeins", (0.15, 1.0, 0.35, 1.0), emission=(0.15, 1.0, 0.35, 1.0), emission_strength=7.5)
    m_eye = create_mat("Mat_BossGlowingEyes", (1.0, 0.15, 0.08, 1.0), emission=(1.0, 0.15, 0.08, 1.0), emission_strength=5.5)
    m_gore = create_mat("Mat_BossGore", (0.82, 0.06, 0.04, 1.0), roughness=0.20, metallic=0.15)
    m_hazmat = create_mat("Mat_TornHazmat", (0.85, 0.72, 0.12, 1.0), roughness=0.75) # Torn yellow containment suit scraps
    
    parts = []
    
    # Horrifying Mutant Skull with Quadruple Glowing Eyes & Fangs
    parts.append(add_sphere("Boss_Head", (0, 1.95, 0.08), 0.155, m_flesh, segs=22, rings=18))
    # Carapace Brow Plates
    parts.append(add_box("Boss_BrowArmor", (0, 1.98, 0.21), (0.22, 0.055, 0.065), m_armor))
    # 4 Glowing Mutant Eyes
    parts.append(add_sphere("Boss_Eye_1", (-0.055, 1.96, 0.21), 0.024, m_eye, segs=10, rings=8))
    parts.append(add_sphere("Boss_Eye_2", (0.055, 1.96, 0.21), 0.024, m_eye, segs=10, rings=8))
    parts.append(add_sphere("Boss_Eye_3", (-0.025, 1.91, 0.22), 0.018, m_eye, segs=8, rings=6))
    parts.append(add_sphere("Boss_Eye_4", (0.025, 1.91, 0.22), 0.018, m_eye, segs=8, rings=6))
    # Massive Predatory Jaw with Bone Spikes
    parts.append(add_box("Boss_Jaw", (0, 1.78, 0.18), (0.165, 0.125, 0.145), m_flesh, rot=(math.radians(18), 0, 0)))
    parts.append(add_box("Boss_Fangs", (0, 1.83, 0.25), (0.125, 0.045, 0.035), m_spike))
    
    # Massive Upper Body with Chitinous Back Carapace & Toxic Veins
    parts.append(add_box("Boss_Torso", (0, 1.40, 0.05), (0.72, 0.65, 0.46), m_flesh))
    parts.append(add_box("Boss_Carapace_Back", (0, 1.44, -0.16), (0.68, 0.60, 0.18), m_armor))
    # 4 Protruding Dorsal Bone Spikes on back
    for s_idx, (sx, sy, sz) in enumerate([(-0.20, 1.55, -0.25), (0.20, 1.55, -0.25), (-0.15, 1.35, -0.25), (0.15, 1.35, -0.25)]):
        parts.append(add_cyl(f"DorsalSpike_{s_idx}", (sx, sy, sz), 0.032, 0.42, rot=(math.radians(-55), sx * 1.5, 0), mat=m_spike, verts=8))
        
    # Bioluminescent Toxic Veins running across chest and shoulders
    for v_idx, vy in enumerate([1.52, 1.40, 1.28]):
        parts.append(add_box(f"Toxic_Vein_{v_idx}", (0, vy, 0.285), (0.42, 0.028, 0.015), m_vein))
        
    # Massive Mutated Right Arm (Giant Crab/Bone Blade Mutation)
    parts.append(add_sphere("Boss_Shoulder_R", (0.52, 1.58, 0.08), 0.20, m_armor))
    parts.append(add_cyl("Boss_Bicep_R", (0.62, 1.28, 0.16), 0.155, 0.48, rot=(math.radians(45), math.radians(18), 0), mat=m_flesh, verts=16))
    # Giant Chitinous Arm Blade Spike
    parts.append(add_box("Boss_Blade_R", (0.70, 0.95, 0.45), (0.12, 0.25, 0.75), m_spike, rot=(math.radians(45), 0, 0)))
    parts.append(add_box("Boss_Claw_R", (0.70, 0.75, 0.68), (0.18, 0.18, 0.22), m_flesh))
    
    # Left Arm (Heavy Humanoid Arm with Spiked Knuckles)
    parts.append(add_sphere("Boss_Shoulder_L", (-0.48, 1.52, 0.05), 0.16, m_flesh))
    parts.append(add_cyl("Boss_Bicep_L", (-0.54, 1.26, 0.10), 0.125, 0.42, rot=(math.radians(35), math.radians(-15), 0), mat=m_flesh, verts=14))
    parts.append(add_cyl("Boss_Forearm_L", (-0.56, 0.95, 0.20), 0.108, 0.38, rot=(math.radians(50), math.radians(-10), 0), mat=m_flesh, verts=14))
    parts.append(add_box("Boss_Hand_L", (-0.58, 0.72, 0.32), (0.16, 0.16, 0.12), m_flesh))
    
    # Lower Body with Torn Yellow Hazmat Scraps & Massive Stomp Legs
    parts.append(add_box("Boss_Pelvis", (0, 0.98, 0.02), (0.58, 0.24, 0.38), m_hazmat))
    for side, sign in [("L", -1), ("R", 1)]:
        parts.append(add_cyl(f"Boss_Thigh_{side}", (sign * 0.22, 0.70, 0.04), 0.155, 0.48, mat=m_flesh, verts=16))
        parts.append(add_cyl(f"Boss_Shin_{side}", (sign * 0.22, 0.26, 0.04), 0.135, 0.46, mat=m_armor, verts=16))
        parts.append(add_box(f"Boss_Foot_{side}", (sign * 0.22, 0.06, 0.12), (0.22, 0.12, 0.44), m_armor))

    boss_obj = join_all(parts, "ZombieBoss")
    export_assets('assets/3d/zombies/zombie_boss.glb', 'models/zombies/zombie_boss.obj', 'tools/blender/generated/zombie_boss.blend')
    print("Realistic Boss Alpha Mutant generated successfully!")


# ==============================================================================
# 4. REALISTIC M4A1 SENTINEL ASSAULT RIFLE (rifle.glb / .obj)
# ==============================================================================

def build_realistic_rifle():
    print("\n--- BUILDING REALISTIC M4A1 SENTINEL ASSAULT RIFLE ---")
    clear_scene()
    
    m_steel = create_mat("Mat_RifleSteel", (0.36, 0.38, 0.42, 1.0), metallic=0.88, roughness=0.28)
    m_poly = create_mat("Mat_RiflePolymer", (0.14, 0.15, 0.16, 1.0), metallic=0.05, roughness=0.75)
    m_anodized = create_mat("Mat_RifleAnodized", (0.22, 0.24, 0.28, 1.0), metallic=0.85, roughness=0.35)
    m_reticle = create_mat("Mat_RedDotReticle", (1.0, 0.1, 0.1, 1.0), emission=(1.0, 0.1, 0.1, 1.0), emission_strength=6.5)
    
    parts = []
    
    # Upper & Lower Receiver
    parts.append(add_box("Rifle_Receiver", (0, 0.045, -0.05), (0.042, 0.075, 0.22), m_anodized))
    parts.append(add_box("Brass_Deflector", (0.024, 0.058, -0.04), (0.014, 0.018, 0.025), m_steel))
    parts.append(add_box("Forward_Assist", (0.026, 0.065, 0.02), (0.016, 0.016, 0.035), m_steel, rot=(math.radians(25), 0, 0)))
    
    # Tactical Red Dot Holographic Sight with Sunshade & Glowing Reticle
    parts.append(add_box("Optic_Base", (0, 0.092, -0.05), (0.032, 0.018, 0.095), m_anodized))
    parts.append(add_cyl("Optic_Tube", (0, 0.125, -0.05), 0.018, 0.095, rot=(math.radians(90), 0, 0), mat=m_anodized, verts=16))
    parts.append(add_sphere("Red_Dot_Reticle", (0, 0.125, -0.05), 0.0035, m_reticle, segs=8, rings=6))
    
    # Free-Float M-LOK Rail Handguard with Cooling Slots
    parts.append(add_cyl("Handguard", (0, 0.052, -0.26), 0.026, 0.24, rot=(math.radians(90), 0, 0), mat=m_anodized, verts=8))
    # Top Picatinny Rail
    parts.append(add_box("Top_Rail", (0, 0.082, -0.18), (0.022, 0.010, 0.38), m_steel))
    
    # M4 Carbine Steel Barrel & Birdcage Flash Hider
    parts.append(add_cyl("Rifle_Barrel", (0, 0.052, -0.42), 0.009, 0.14, rot=(math.radians(90), 0, 0), mat=m_steel, verts=14))
    parts.append(add_cyl("Flash_Hider", (0, 0.052, -0.50), 0.012, 0.038, rot=(math.radians(90), 0, 0), mat=m_steel, verts=12))
    
    # Curved 30-round STANAG Magazine
    parts.append(add_box("STANAG_Mag", (0, -0.065, -0.09), (0.026, 0.165, 0.065), m_steel, rot=(math.radians(-14), 0, 0)))
    
    # Ergonomic A2 Pistol Grip
    parts.append(add_box("Rifle_Grip", (0, -0.038, 0.02), (0.032, 0.115, 0.045), m_poly, rot=(math.radians(22), 0, 0)))
    parts.append(add_box("Rifle_Trigger", (0, 0.012, -0.02), (0.006, 0.024, 0.012), m_steel, rot=(math.radians(-15), 0, 0)))
    
    # Collapsible Crane Combat Buttstock & Buffer Tube
    parts.append(add_cyl("Buffer_Tube", (0, 0.052, 0.13), 0.015, 0.16, rot=(math.radians(90), 0, 0), mat=m_steel, verts=12))
    parts.append(add_box("Crane_Stock", (0, 0.045, 0.20), (0.045, 0.115, 0.14), m_poly))
    parts.append(add_box("Recoil_Pad", (0, 0.045, 0.272), (0.046, 0.118, 0.015), m_poly))

    rifle_obj = join_all(parts, "Rifle_M4A1")
    export_assets('assets/3d/weapons/rifle.glb', 'models/weapons/rifle.obj', 'tools/blender/generated/rifle.blend')
    print("Realistic M4A1 Sentinel Assault Rifle generated successfully!")


# ==============================================================================
# 5. REALISTIC REMINGTON 870 TACTICAL SHOTGUN (shotgun.glb / .obj)
# ==============================================================================

def build_realistic_shotgun():
    print("\n--- BUILDING REALISTIC REMINGTON 870 SHOTGUN ---")
    clear_scene()
    
    m_steel = create_mat("Mat_ShotgunSteel", (0.34, 0.36, 0.40, 1.0), metallic=0.90, roughness=0.25)
    m_poly = create_mat("Mat_ShotgunStock", (0.15, 0.16, 0.17, 1.0), metallic=0.05, roughness=0.72)
    m_bead = create_mat("Mat_BeadSight", (0.95, 0.85, 0.35, 1.0), metallic=0.8, roughness=0.2)
    m_pad = create_mat("Mat_RecoilPad", (0.08, 0.08, 0.09, 1.0), roughness=0.85)
    
    parts = []
    
    # Heavy Steel Receiver & Loading Gate
    parts.append(add_box("Shotgun_Receiver", (0, 0.040, -0.06), (0.038, 0.068, 0.20), m_steel))
    parts.append(add_box("Ejection_Port", (0.0185, 0.048, -0.07), (0.005, 0.024, 0.065), m_steel))
    
    # 18.5" Heavy Combat Barrel & Magazine Tube
    parts.append(add_cyl("Shotgun_Barrel", (0, 0.058, -0.38), 0.014, 0.48, rot=(math.radians(90), 0, 0), mat=m_steel, verts=16))
    parts.append(add_cyl("Mag_Tube", (0, 0.032, -0.34), 0.013, 0.42, rot=(math.radians(90), 0, 0), mat=m_steel, verts=14))
    parts.append(add_cyl("Mag_Cap", (0, 0.032, -0.55), 0.014, 0.022, rot=(math.radians(90), 0, 0), mat=m_steel, verts=12))
    
    # Gold Bead Front Sight
    parts.append(add_sphere("Bead_Sight", (0, 0.076, -0.61), 0.0035, m_bead, segs=8, rings=6))
    
    # Ribbed Tactical Polymer Pump Forend with Grooves
    parts.append(add_cyl("Pump_Forend", (0, 0.032, -0.30), 0.024, 0.18, rot=(math.radians(90), 0, 0), mat=m_poly, verts=14))
    
    # Tactical Polymer Stock & Rubber Recoil Pad
    parts.append(add_box("Stock_Grip", (0, -0.025, 0.06), (0.034, 0.095, 0.055), m_poly, rot=(math.radians(28), 0, 0)))
    parts.append(add_box("Stock_Body", (0, 0.015, 0.18), (0.038, 0.095, 0.22), m_poly))
    parts.append(add_box("Recoil_Cushion", (0, 0.015, 0.292), (0.040, 0.105, 0.024), m_pad))

    shotgun_obj = join_all(parts, "Shotgun_Remington870")
    export_assets('assets/3d/weapons/shotgun.glb', 'models/weapons/shotgun.obj', 'tools/blender/generated/shotgun.blend')
    print("Realistic Remington 870 Shotgun generated successfully!")


# ==============================================================================
# 6. REALISTIC RAILWAY STATION CONCOURSE (railway_station.glb)
# ==============================================================================

def build_realistic_railway_station():
    print("\n--- BUILDING REALISTIC RAILWAY / METRO STATION CONCOURSE ---")
    clear_scene()
    
    m_platform = create_mat("Mat_StationPlatform", (0.72, 0.74, 0.76, 1.0), roughness=0.65)
    m_tactile = create_mat("Mat_TactilePaving", (0.85, 0.72, 0.15, 1.0), roughness=0.60) # Yellow tactile warning pavers
    m_rail = create_mat("Mat_SteelRail", (0.35, 0.38, 0.42, 1.0), metallic=0.90, roughness=0.25)
    m_sleepers = create_mat("Mat_WoodSleepers", (0.22, 0.18, 0.14, 1.0), roughness=0.85)
    m_pillar = create_mat("Mat_ConcretePillar", (0.45, 0.48, 0.50, 1.0), roughness=0.80)
    m_sign = create_mat("Mat_TransitSign", (0.10, 0.45, 0.85, 1.0), emission=(0.10, 0.45, 0.85, 1.0), emission_strength=2.5)
    m_bench = create_mat("Mat_PlatformBench", (0.15, 0.20, 0.25, 1.0), roughness=0.55)
    m_light = create_mat("Mat_StationLight", (0.95, 0.98, 1.0, 1.0), emission=(0.95, 0.98, 1.0, 1.0), emission_strength=4.0)
    
    parts = []
    
    # High-level Passenger Platform (Y=0.0)
    parts.append(add_box("Platform_Floor", (4.0, 0.0, 0.0), (14.0, 0.20, 36.0), m_platform))
    # Yellow Tactile Warning Paver Edge strip
    parts.append(add_box("Tactile_Edge", (-2.8, 0.105, 0.0), (0.45, 0.015, 36.0), m_tactile))
    
    # Lower Track Bed (Y=-1.10)
    parts.append(add_box("Track_Bed", (-8.0, -1.20, 0.0), (12.0, 0.20, 36.0), m_platform))
    # Dual Steel Rails & Wooden Sleepers
    for r_x in [-6.5, -9.5]:
        parts.append(add_box(f"Rail_L_{r_x}", (r_x - 0.7, -1.03, 0.0), (0.08, 0.14, 36.0), m_rail))
        parts.append(add_box(f"Rail_R_{r_x}", (r_x + 0.7, -1.03, 0.0), (0.08, 0.14, 36.0), m_rail))
        for sz in range(-16, 17, 2):
            parts.append(add_box(f"Sleeper_{r_x}_{sz}", (r_x, -1.13, sz), (2.0, 0.10, 0.25), m_sleepers))
            
    # Deep Tunnel Portal Archway in the distance
    parts.append(add_box("Tunnel_Portal", (-8.0, 2.0, -18.0), (12.0, 6.0, 0.8), m_pillar))
    
    # Overhead Structural Steel Canopy Roof & Pillars
    for pz in [-10, 0, 10]:
        parts.append(add_cyl(f"Platform_Pillar_{pz}", (4.0, 2.5, pz), 0.45, 5.0, mat=m_pillar, verts=12))
        parts.append(add_box(f"Canopy_Truss_{pz}", (0.0, 5.0, pz), (22.0, 0.35, 0.35), m_rail))
        parts.append(add_box(f"Station_Light_{pz}", (4.0, 4.7, pz), (2.4, 0.12, 0.35), m_light))
        
    # Station Transit Signs & Waiting Benches
    parts.append(add_box("Transit_Sign", (4.0, 3.4, 0.0), (3.6, 0.75, 0.12), m_sign))
    parts.append(add_box("Bench_1", (4.0, 0.35, -5.0), (2.6, 0.45, 0.65), m_bench))
    parts.append(add_box("Bench_2", (4.0, 0.35, 5.0), (2.6, 0.45, 0.65), m_bench))

    station_obj = join_all(parts, "RailwayStationMesh")
    export_assets('assets/3d/environments/railway_station.glb', 'models/environment/railway/railway_station.obj', 'tools/blender/generated/railway_station.blend')
    print("Realistic Railway Station Concourse generated successfully!")


# ==============================================================================
# 7. REALISTIC ABANDONED TRAIN CARRIAGE (train_carriage.glb)
# ==============================================================================

def build_realistic_train():
    print("\n--- BUILDING REALISTIC ABANDONED TRAIN CARRIAGE ---")
    clear_scene()
    
    m_body = create_mat("Mat_TrainSteel", (0.55, 0.58, 0.62, 1.0), metallic=0.75, roughness=0.35)
    m_accent = create_mat("Mat_TrainStripe", (0.15, 0.40, 0.80, 1.0), roughness=0.45)
    m_glass = create_mat("Mat_TrainWindowGlass", (0.25, 0.35, 0.45, 0.85), metallic=0.2, roughness=0.08)
    m_seat = create_mat("Mat_TrainSeats", (0.12, 0.22, 0.35, 1.0), roughness=0.75)
    m_light = create_mat("Mat_TrainCeilingLight", (0.95, 0.98, 1.0, 1.0), emission=(0.95, 0.98, 1.0, 1.0), emission_strength=4.0)
    m_handrail = create_mat("Mat_StainlessHandrail", (0.82, 0.84, 0.86, 1.0), metallic=0.92, roughness=0.18)
    
    parts = []
    
    # Outer Carriage Body Shell: Length 18m, Width 3.2m, Height 2.8m
    parts.append(add_box("Carriage_Floor", (0, 0.0, 0), (3.2, 0.15, 18.0), m_body))
    parts.append(add_box("Carriage_Roof", (0, 2.75, 0), (3.2, 0.15, 18.0), m_body))
    parts.append(add_box("Wall_Left", (-1.55, 1.35, 0), (0.12, 2.7, 18.0), m_body))
    parts.append(add_box("Wall_Right", (1.55, 1.35, 0), (0.12, 2.7, 18.0), m_body))
    
    # Exterior Color Accent Stripe
    parts.append(add_box("Stripe_L", (-1.62, 1.10, 0), (0.015, 0.25, 18.0), m_accent))
    parts.append(add_box("Stripe_R", (1.62, 1.10, 0), (0.015, 0.25, 18.0), m_accent))
    
    # Windows along the walls
    for wz in range(-7, 8, 3):
        parts.append(add_box(f"Window_L_{wz}", (-1.55, 1.55, wz), (0.14, 0.85, 1.6), m_glass))
        parts.append(add_box(f"Window_R_{wz}", (1.55, 1.55, wz), (0.14, 0.85, 1.6), m_glass))
        
    # Interior Commuter Passenger Seats
    for sz in range(-7, 8, 2):
        parts.append(add_box(f"Seat_L_{sz}", (-1.05, 0.45, sz), (0.75, 0.45, 0.75), m_seat))
        parts.append(add_box(f"Seat_R_{sz}", (1.05, 0.45, sz), (0.75, 0.45, 0.75), m_seat))
        
    # Center Overhead Stainless Steel Handrail Pole & Ceiling Lights
    parts.append(add_cyl("Center_Handrail", (0, 2.30, 0), 0.022, 17.0, rot=(math.radians(90), 0, 0), mat=m_handrail, verts=10))
    for lz in [-6, 0, 6]:
        parts.append(add_box(f"Ceiling_Light_{lz}", (0, 2.65, lz), (0.45, 0.06, 2.4), m_light))

    train_obj = join_all(parts, "TrainCarriageMesh")
    export_assets('assets/3d/environments/train_carriage.glb', 'models/environment/train/train_carriage.obj', 'tools/blender/generated/train_carriage.blend')
    print("Realistic Abandoned Train Carriage generated successfully!")


# ==============================================================================
# 8. REALISTIC INDUSTRIAL STREET (industrial_street.glb)
# ==============================================================================

def build_realistic_industrial_street():
    print("\n--- BUILDING REALISTIC INDUSTRIAL STREET ---")
    clear_scene()
    
    m_asphalt = create_mat("Mat_AsphaltRoad", (0.35, 0.36, 0.38, 1.0), roughness=0.80)
    m_sidewalk = create_mat("Mat_ConcreteSidewalk", (0.70, 0.72, 0.74, 1.0), roughness=0.70)
    m_warehouse = create_mat("Mat_CorrugatedMetal", (0.35, 0.38, 0.42, 1.0), metallic=0.75, roughness=0.45)
    m_dumpster = create_mat("Mat_CommercialDumpster", (0.12, 0.32, 0.18, 1.0), roughness=0.65)
    m_lamp = create_mat("Mat_StreetLampLight", (1.0, 0.85, 0.45, 1.0), emission=(1.0, 0.85, 0.45, 1.0), emission_strength=4.5)
    m_metal = create_mat("Mat_IndustrialPipes", (0.28, 0.30, 0.32, 1.0), metallic=0.85, roughness=0.35)
    
    parts = []
    
    # Asphalt Roadway: 12m wide, 36m long
    parts.append(add_box("Street_Asphalt", (0, 0, 0), (12.0, 0.20, 36.0), m_asphalt))
    # Sidewalks with Curbs on both sides
    parts.append(add_box("Sidewalk_L", (-8.5, 0.15, 0), (5.0, 0.30, 36.0), m_sidewalk))
    parts.append(add_box("Sidewalk_R", (8.5, 0.15, 0), (5.0, 0.30, 36.0), m_sidewalk))
    
    # Corrugated Metal Warehouse Facade on Left
    parts.append(add_box("Warehouse_Facade", (-11.5, 4.0, 0), (1.0, 8.0, 36.0), m_warehouse))
    # Overhead Industrial Conduit Pipes
    parts.append(add_cyl("Industrial_Pipe_1", (-10.5, 6.5, 0), 0.18, 36.0, rot=(math.radians(90), 0, 0), mat=m_metal, verts=12))
    
    # Commercial Dumpsters & Industrial Street Lamp Poles
    for dz in [-8.0, 8.0]:
        parts.append(add_box(f"Dumpster_{dz}", (-7.5, 0.85, dz), (1.8, 1.4, 2.4), m_dumpster))
        parts.append(add_cyl(f"Lamp_Post_{dz}", (6.5, 3.2, dz), 0.12, 6.2, mat=m_metal, verts=10))
        parts.append(add_box(f"Lamp_Housing_{dz}", (5.8, 6.2, dz), (1.2, 0.25, 0.45), m_metal))
        parts.append(add_box(f"Lamp_Bulb_{dz}", (5.8, 6.05, dz), (0.85, 0.08, 0.35), m_lamp))

    street_obj = join_all(parts, "IndustrialStreetMesh")
    export_assets('assets/3d/environments/industrial_street.glb', 'models/environment/industrial/industrial_street.obj', 'tools/blender/generated/industrial_street.blend')
    print("Realistic Industrial Street generated successfully!")


# ==============================================================================
# 9. REALISTIC QUARANTINE BOSS ARENA (boss_arena.glb)
# ==============================================================================

def build_realistic_boss_arena():
    print("\n--- BUILDING REALISTIC QUARANTINE BOSS ARENA ---")
    clear_scene()
    
    m_floor = create_mat("Mat_ArenaFloor", (0.65, 0.68, 0.70, 1.0), roughness=0.45)
    m_hazard = create_mat("Mat_HazardStripe", (0.95, 0.82, 0.10, 1.0), roughness=0.55) # Yellow hazard border
    m_wall = create_mat("Mat_ReinforcedContainment", (0.25, 0.26, 0.28, 1.0), metallic=0.65, roughness=0.45)
    m_catwalk = create_mat("Mat_SteelCatwalk", (0.18, 0.20, 0.22, 1.0), metallic=0.88, roughness=0.30)
    m_alarm = create_mat("Mat_AlarmLight", (1.0, 0.15, 0.05, 1.0), emission=(1.0, 0.15, 0.05, 1.0), emission_strength=5.0)
    
    parts = []
    
    # Central Containment Arena Floor: 34m x 34m
    parts.append(add_box("Arena_Floor", (0, 0, 0), (34.0, 0.20, 34.0), m_floor))
    # Perimeter Yellow/Black Hazard Caution Border
    parts.append(add_box("Hazard_Border_N", (0, 0.105, -16.0), (33.0, 0.015, 0.8), m_hazard))
    parts.append(add_box("Hazard_Border_S", (0, 0.105, 16.0), (33.0, 0.015, 0.8), m_hazard))
    parts.append(add_box("Hazard_Border_W", (-16.0, 0.105, 0), (0.8, 0.015, 33.0), m_hazard))
    parts.append(add_box("Hazard_Border_E", (16.0, 0.105, 0), (0.8, 0.015, 33.0), m_hazard))
    
    # 8m Reinforced Perimeter Blast Walls
    parts.append(add_box("Wall_North", (0, 4.0, -17.2), (35.0, 8.0, 0.6), m_wall))
    parts.append(add_box("Wall_South", (0, 4.0, 17.2), (35.0, 8.0, 0.6), m_wall))
    parts.append(add_box("Wall_West", (-17.2, 4.0, 0), (0.6, 8.0, 35.0), m_wall))
    parts.append(add_box("Wall_East", (17.2, 4.0, 0), (0.6, 8.0, 35.0), m_wall))
    
    # Overhead Perimeter Observation Catwalk at Y=5.5m
    for cw_z in [-15.0, 15.0]:
        parts.append(add_box(f"Catwalk_{cw_z}", (0, 5.5, cw_z), (32.0, 0.18, 2.2), m_catwalk))
        parts.append(add_box(f"Railing_{cw_z}", (0, 6.2, cw_z), (32.0, 1.1, 0.05), m_catwalk))
        
    # Central Shattered Bio-Containment Pod Frame in center of arena
    for c_ang in [0, 90, 180, 270]:
        rad = math.radians(c_ang)
        parts.append(add_cyl(f"BioPod_Pillar_{c_ang}", (math.cos(rad)*3.5, 2.5, math.sin(rad)*3.5), 0.15, 5.0, mat=m_wall, verts=10))
    parts.append(add_cyl("BioPod_Ring", (0, 4.8, 0), 3.6, 0.35, mat=m_wall, verts=16))
    
    # 4 Flashing Emergency Alarm Beacons
    for ax, az in [(-10, -10), (10, -10), (-10, 10), (10, 10)]:
        parts.append(add_box(f"Alarm_Housing_{ax}_{az}", (ax, 5.2, az), (0.45, 0.35, 0.45), m_wall))
        parts.append(add_sphere(f"Alarm_Strobe_{ax}_{az}", (ax, 4.9, az), 0.14, m_alarm, segs=8, rings=6))

    arena_obj = join_all(parts, "BossArenaMesh")
    export_assets('assets/3d/environments/boss_arena.glb', 'models/environment/boss_arena/boss_arena.obj', 'tools/blender/generated/boss_arena.blend')
    print("Realistic Quarantine Boss Arena generated successfully!")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':
    print("==================================================================")
    print("GENERATING REALISTIC 3D ASSETS (PHASE 2 - 10)")
    print("==================================================================")
    build_realistic_fast_zombie()
    build_realistic_heavy_zombie()
    build_realistic_boss()
    build_realistic_rifle()
    build_realistic_shotgun()
    build_realistic_railway_station()
    build_realistic_train()
    build_realistic_industrial_street()
    build_realistic_boss_arena()
    print("\n==================================================================")
    print("ALL REMAINING REALISTIC ASSETS GENERATED & EXPORTED!")
    print("==================================================================")
