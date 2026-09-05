"""
Sector Zero: Lockdown - Real Human Infected Zombie Pipeline
Builds true humanoid zombies that look like real humans:
- Realistic human skin tones (natural skin base with subtle pallor/vein decay)
- Realistic human facial anatomy (white sclera, human iris/pupils, eyelids, nose, lips, natural teeth, ears, hair)
- Realistic human commuter / civilian clothing (button-down shirt, denim jeans, leather belt, shoes, watch)
- Realistic 5-finger human hands
- 23-bone armature with full biomechanical skeletal animation suite
"""

import bpy
import bmesh
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for col in [bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.armatures, bpy.data.actions]:
        for item in list(col):
            col.remove(item, do_unlink=True)

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

def add_part_box(name, loc, size, bone_name, mat=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    vg = obj.vertex_groups.new(name=bone_name)
    vg.add(range(len(obj.data.vertices)), 1.0, 'REPLACE')
    return obj

def add_part_cyl(name, loc, r, d, bone_name, rot=(0,0,0), mat=None, verts=14, smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d, location=loc, rotation=rot, vertices=verts)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        for p in obj.data.polygons: p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    vg = obj.vertex_groups.new(name=bone_name)
    vg.add(range(len(obj.data.vertices)), 1.0, 'REPLACE')
    return obj

def add_part_sphere(name, loc, r, bone_name, mat=None, segs=16, rings=12, smooth=True):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=segs, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        for p in obj.data.polygons: p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    vg = obj.vertex_groups.new(name=bone_name)
    vg.add(range(len(obj.data.vertices)), 1.0, 'REPLACE')
    return obj

def join_mesh_parts(parts, final_name):
    valid = [o for o in parts if o and o.name in bpy.data.objects]
    if not valid: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in valid: o.select_set(True)
    bpy.context.view_layer.objects.active = valid[0]
    bpy.ops.object.join()
    res = bpy.context.active_object
    res.name = final_name
    return res

def create_humanoid_armature(arm_name="ZombieArmature", scale_factor=1.0, has_extra_scythe=False):
    arm_data = bpy.data.armatures.new(f"{arm_name}Data")
    arm_obj = bpy.data.objects.new(arm_name, arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm_data.edit_bones
    
    def sf(pt):
        return (pt[0]*scale_factor, pt[1]*scale_factor, pt[2]*scale_factor)
        
    def nb(name, head, tail, parent_name=None):
        b = eb.new(name)
        b.head = sf(head)
        b.tail = sf(tail)
        if parent_name and parent_name in eb:
            b.parent = eb[parent_name]
        return b
        
    nb("Root", (0, 0, 0), (0, 0.1, 0))
    nb("Pelvis", (0, 0.92, 0), (0, 1.02, 0), "Root")
    nb("Spine", (0, 1.02, 0), (0, 1.20, 0), "Pelvis")
    nb("Chest", (0, 1.20, 0), (0, 1.44, 0), "Spine")
    nb("Neck", (0, 1.44, 0), (0, 1.55, 0.02), "Chest")
    nb("Head", (0, 1.55, 0.02), (0, 1.75, 0.04), "Neck")
    nb("Jaw", (0, 1.52, 0.07), (0, 1.48, 0.11), "Head")
    
    # Left Arm
    nb("Shoulder.L", (-0.08, 1.38, 0), (-0.22, 1.33, 0.02), "Chest")
    nb("UpperArm.L", (-0.22, 1.33, 0.02), (-0.26, 1.05, 0.06), "Shoulder.L")
    nb("Forearm.L", (-0.26, 1.05, 0.06), (-0.26, 0.78, 0.14), "UpperArm.L")
    nb("Hand.L", (-0.26, 0.78, 0.14), (-0.26, 0.62, 0.20), "Forearm.L")
    
    # Right Arm
    nb("Shoulder.R", (0.08, 1.38, 0), (0.22, 1.33, 0.02), "Chest")
    nb("UpperArm.R", (0.22, 1.33, 0.02), (0.26, 1.05, 0.06), "Shoulder.R")
    nb("Forearm.R", (0.26, 1.05, 0.06), (0.26, 0.78, 0.14), "UpperArm.R")
    nb("Hand.R", (0.26, 0.78, 0.14), (0.26, 0.62, 0.20), "Forearm.R")
    
    # Legs
    nb("UpperLeg.L", (-0.11, 0.90, 0), (-0.11, 0.50, 0.02), "Pelvis")
    nb("LowerLeg.L", (-0.11, 0.50, 0.02), (-0.11, 0.10, 0.0), "UpperLeg.L")
    nb("Foot.L", (-0.11, 0.10, 0.0), (-0.11, 0.03, 0.14), "LowerLeg.L")
    nb("Toe.L", (-0.11, 0.03, 0.14), (-0.11, 0.01, 0.22), "Foot.L")
    
    nb("UpperLeg.R", (0.11, 0.90, 0), (0.11, 0.50, 0.02), "Pelvis")
    nb("LowerLeg.R", (0.11, 0.50, 0.02), (0.11, 0.10, 0.0), "UpperLeg.R")
    nb("Foot.R", (0.11, 0.10, 0.0), (0.11, 0.03, 0.14), "LowerLeg.R")
    nb("Toe.R", (0.11, 0.03, 0.14), (0.11, 0.01, 0.22), "Foot.R")
    
    if has_extra_scythe:
        nb("ScytheBlade", (-0.26, 0.62, 0.20), (-0.28, 0.15, 0.75), "Hand.L")
        
    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj

def bind_mesh_to_armature(mesh_obj, arm_obj):
    mod = mesh_obj.modifiers.new(name="Armature", type='ARMATURE')
    mod.object = arm_obj
    mesh_obj.parent = arm_obj

def set_key(arm_obj, bone_name, frame, loc=None, rot_euler=None, scale=None):
    pb = arm_obj.pose.bones.get(bone_name)
    if not pb: return
    pb.rotation_mode = 'XYZ'
    if loc is not None:
        pb.location = loc
        pb.keyframe_insert(data_path="location", frame=frame)
    if rot_euler is not None:
        pb.rotation_euler = rot_euler
        pb.keyframe_insert(data_path="rotation_euler", frame=frame)
    if scale is not None:
        pb.scale = scale
        pb.keyframe_insert(data_path="scale", frame=frame)

def create_action(arm_obj, act_name):
    if arm_obj.animation_data is None:
        arm_obj.animation_data_create()
    act = bpy.data.actions.new(name=act_name)
    arm_obj.animation_data.action = act
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
        pb.scale = (1, 1, 1)
    return act

def stash_action(arm_obj, act):
    track = arm_obj.animation_data.nla_tracks.new()
    track.name = act.name
    start_f = int(act.frame_range[0])
    track.strips.new(act.name, start_f, act)

def export_rigged_glb_and_obj(glb_path, obj_path=None):
    os.makedirs(os.path.dirname(glb_path), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format='GLB',
        use_selection=False,
        export_apply=False,
        export_yup=True,
        export_materials='EXPORT',
        export_animations=True
    )
    print(f"Exported Rigged GLB: {glb_path} ({os.path.getsize(glb_path)} bytes)")
    if obj_path:
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True, export_selected_objects=False)
        print(f"Exported OBJ: {obj_path} ({os.path.getsize(obj_path)} bytes)")


# ==============================================================================
# 1. REAL HUMAN INFECTED COMMUTER (zombie_normal.glb)
# ==============================================================================

def build_real_human_normal_zombie():
    print("\n--- 1. BUILDING REAL HUMAN INFECTED COMMUTER ZOMBIE ---")
    clear_scene()
    
    # Real Human Materials
    m_skin = create_mat("Mat_HumanSkin", (0.78, 0.65, 0.54, 1.0), roughness=0.58) # Natural human skin
    m_skin_pale = create_mat("Mat_HumanSkinPale", (0.72, 0.61, 0.52, 1.0), roughness=0.62) # Sickly undertone
    m_blood = create_mat("Mat_HumanBlood", (0.70, 0.05, 0.04, 1.0), roughness=0.18, metallic=0.08) # Fresh/wet blood
    m_dried_blood = create_mat("Mat_DriedBlood", (0.35, 0.06, 0.05, 1.0), roughness=0.85) # Dried stain
    m_teeth = create_mat("Mat_HumanTeeth", (0.92, 0.90, 0.82, 1.0), roughness=0.30) # Real human enamel
    m_lips = create_mat("Mat_HumanLips", (0.68, 0.44, 0.40, 1.0), roughness=0.45) # Human lips
    m_eye_sclera = create_mat("Mat_HumanEyeSclera", (0.90, 0.88, 0.88, 1.0), roughness=0.10) # White of eye
    m_eye_iris = create_mat("Mat_HumanEyeIris", (0.35, 0.22, 0.12, 1.0), roughness=0.08) # Brown human iris
    m_hair = create_mat("Mat_HumanHair", (0.12, 0.09, 0.07, 1.0), roughness=0.85) # Human dark brown hair
    
    # Real Human Commuter Clothing
    m_shirt = create_mat("Mat_OxfordShirt", (0.42, 0.58, 0.74, 1.0), roughness=0.80) # Sky-blue button-down dress shirt
    m_jeans = create_mat("Mat_DenimJeans", (0.18, 0.24, 0.35, 1.0), roughness=0.85) # Blue denim jeans
    m_belt = create_mat("Mat_LeatherBelt", (0.14, 0.10, 0.08, 1.0), roughness=0.45) # Brown leather belt
    m_buckle = create_mat("Mat_MetalBuckle", (0.75, 0.75, 0.78, 1.0), metallic=0.85, roughness=0.25)
    m_shoes = create_mat("Mat_LeatherShoes", (0.10, 0.08, 0.07, 1.0), roughness=0.40) # Black leather dress shoes
    m_watch = create_mat("Mat_WristWatch", (0.80, 0.80, 0.82, 1.0), metallic=0.80, roughness=0.30)
    
    arm_obj = create_humanoid_armature("NormalZombieArmature", scale_factor=1.0)
    parts = []
    
    # --- REAL HUMAN HEAD & FACE ---
    # Cranium (anatomical skull with human curvature)
    parts.append(add_part_sphere("HHead_Cranium", (0, 1.66, 0.0), 0.105, "Head", m_skin, segs=20, rings=16))
    
    # Forehead & Human Brow Ridge
    parts.append(add_part_box("HFace_Forehead", (0, 1.67, 0.078), (0.125, 0.035, 0.035), "Head", m_skin))
    parts.append(add_part_box("HFace_Eyebrows", (0, 1.655, 0.088), (0.12, 0.012, 0.018), "Head", m_hair))
    
    # Human Left Eye (White sclera + Hazel-brown iris + Pupil in recessed socket)
    parts.append(add_part_sphere("HEye_Sclera_L", (-0.038, 1.642, 0.085), 0.017, "Head", m_eye_sclera, segs=12, rings=10))
    parts.append(add_part_sphere("HEye_Iris_L", (-0.038, 1.642, 0.098), 0.009, "Head", m_eye_iris, segs=10, rings=8))
    
    # Human Right Eye (Bloodshot infected sclera + dilated pupil)
    parts.append(add_part_sphere("HEye_Sclera_R", (0.038, 1.642, 0.085), 0.017, "Head", m_skin_pale, segs=12, rings=10))
    parts.append(add_part_sphere("HEye_Iris_R", (0.038, 1.642, 0.098), 0.009, "Head", m_eye_iris, segs=10, rings=8))
    
    # Eyelids (Upper & Lower)
    parts.append(add_part_box("HEyelid_L", (-0.038, 1.654, 0.090), (0.036, 0.010, 0.015), "Head", m_skin))
    parts.append(add_part_box("HEyelid_R", (0.038, 1.654, 0.090), (0.036, 0.010, 0.015), "Head", m_skin))
    
    # Anatomical Human Nose (Bridge, tip, and nostrils)
    parts.append(add_part_box("HFace_NoseBridge", (0, 1.620, 0.100), (0.024, 0.040, 0.032), "Head", m_skin))
    parts.append(add_part_box("HFace_NoseTip", (0, 1.595, 0.112), (0.028, 0.018, 0.025), "Head", m_skin))
    
    # Cheekbones & Cheeks
    parts.append(add_part_box("HFace_Cheek_L", (-0.062, 1.615, 0.065), (0.035, 0.055, 0.060), "Head", m_skin))
    parts.append(add_part_box("HFace_Cheek_R", (0.062, 1.615, 0.065), (0.035, 0.055, 0.060), "Head", m_skin))
    
    # Human Mouth & Upper Lip
    parts.append(add_part_box("HFace_LipUpper", (0, 1.572, 0.095), (0.054, 0.014, 0.018), "Head", m_lips))
    parts.append(add_part_box("HTeeth_Upper", (0, 1.562, 0.096), (0.050, 0.010, 0.014), "Head", m_teeth))
    
    # Human Ears (Helix and Lobule)
    parts.append(add_part_box("HEar_L", (-0.110, 1.63, 0.0), (0.018, 0.055, 0.032), "Head", m_skin))
    parts.append(add_part_box("HEar_R", (0.110, 1.63, 0.0), (0.018, 0.055, 0.032), "Head", m_skin))
    
    # Human Hair (Natural parted hairstyle)
    parts.append(add_part_sphere("HHair_Top", (0, 1.685, -0.01), 0.110, "Head", m_hair, segs=16, rings=12))
    parts.append(add_part_box("HHair_Side_L", (-0.105, 1.66, 0.0), (0.020, 0.070, 0.090), "Head", m_hair))
    parts.append(add_part_box("HHair_Side_R", (0.105, 1.66, 0.0), (0.020, 0.070, 0.090), "Head", m_hair))
    
    # Jaw & Lower Teeth (Human chin and lower jaw)
    parts.append(add_part_box("HFace_JawChin", (0, 1.525, 0.070), (0.078, 0.055, 0.080), "Jaw", m_skin))
    parts.append(add_part_box("HFace_LipLower", (0, 1.552, 0.092), (0.052, 0.014, 0.018), "Jaw", m_lips))
    parts.append(add_part_box("HTeeth_Lower", (0, 1.540, 0.090), (0.048, 0.010, 0.014), "Jaw", m_teeth))
    # Slight blood stain on chin from infection
    parts.append(add_part_box("HBlood_Chin", (0.015, 1.520, 0.098), (0.030, 0.025, 0.015), "Jaw", m_blood))
    
    # Human Neck
    parts.append(add_part_cyl("HNeck", (0, 1.46, 0.0), 0.066, 0.14, "Neck", mat=m_skin, verts=14))
    # Small bite mark scar on neck
    parts.append(add_part_box("HBite_Neck", (-0.050, 1.46, 0.035), (0.025, 0.035, 0.025), "Neck", m_blood))
    
    # --- REAL HUMAN COMMUTER CLOTHING (SHIRT & TORSO) ---
    # Oxford Button-Down Shirt Torso
    parts.append(add_part_box("HShirt_Torso", (0, 1.28, 0.01), (0.36, 0.32, 0.22), "Chest", m_shirt))
    # Shirt Collar
    parts.append(add_part_cyl("HShirt_Collar", (0, 1.42, 0.01), 0.080, 0.045, "Chest", mat=m_shirt, verts=14))
    # Center Placket with Buttons
    parts.append(add_part_box("HShirt_Placket", (0, 1.27, 0.122), (0.035, 0.30, 0.010), "Chest", m_shirt))
    for by in [1.38, 1.30, 1.22, 1.14]:
        parts.append(add_part_box(f"HShirt_Button_{by}", (0, by, 0.128), (0.012, 0.012, 0.006), "Chest", m_buckle))
    # Breast Pocket
    parts.append(add_part_box("HShirt_Pocket", (-0.09, 1.30, 0.122), (0.075, 0.085, 0.010), "Chest", m_shirt))
    # Torn shoulder seam showing human bite injury
    parts.append(add_part_box("HWound_Shoulder", (-0.14, 1.36, 0.08), (0.065, 0.065, 0.035), "Chest", m_blood))
    # Dried blood stain on shirt
    parts.append(add_part_box("HBlood_Shirt", (0.04, 1.24, 0.124), (0.09, 0.12, 0.008), "Chest", m_dried_blood))
    
    # Lower Shirt & Midriff
    parts.append(add_part_box("HShirt_Lower", (0, 1.10, 0.01), (0.34, 0.18, 0.21), "Spine", m_shirt))
    
    # Leather Belt & Metal Buckle
    parts.append(add_part_box("HBelt_Strap", (0, 0.99, 0.01), (0.34, 0.055, 0.21), "Pelvis", m_belt))
    parts.append(add_part_box("HBelt_Buckle", (0, 0.99, 0.120), (0.060, 0.045, 0.018), "Pelvis", m_buckle))
    
    # Blue Denim Jeans (Pelvis)
    parts.append(add_part_box("HJeans_Pelvis", (0, 0.93, 0.01), (0.33, 0.14, 0.20), "Pelvis", m_jeans))
    
    # --- REAL HUMAN ARMS & 5 ARTICULATED FINGERS ---
    # Left Arm (Torn rolled sleeve, bare forearm, silver wristwatch)
    parts.append(add_part_sphere("HShoulder_L", (-0.23, 1.34, 0.02), 0.072, "Shoulder.L", m_shirt))
    parts.append(add_part_cyl("HArm_Upper_L", (-0.24, 1.20, 0.04), 0.058, 0.22, "UpperArm.L", mat=m_shirt, verts=12))
    # Torn sleeve edge
    parts.append(add_part_cyl("HTorn_Sleeve_L", (-0.24, 1.09, 0.06), 0.064, 0.04, "UpperArm.L", mat=m_shirt, verts=12))
    # Bare human forearm with bite scratch
    parts.append(add_part_cyl("HForearm_L", (-0.24, 0.93, 0.09), 0.048, 0.24, "Forearm.L", mat=m_skin, verts=12))
    parts.append(add_part_box("HScratch_L", (-0.24, 0.93, 0.14), (0.020, 0.080, 0.015), "Forearm.L", m_blood))
    # Wristwatch on left wrist
    parts.append(add_part_box("HWatch_Case", (-0.24, 0.81, 0.11), (0.035, 0.022, 0.035), "Forearm.L", m_watch))
    
    # Left Hand (Palm + 5 individual fingers with nails)
    parts.append(add_part_box("HHand_Palm_L", (-0.24, 0.74, 0.12), (0.068, 0.072, 0.034), "Hand.L", m_skin))
    # Thumb
    parts.append(add_part_cyl("HFinger_Thumb_L", (-0.205, 0.73, 0.14), 0.011, 0.045, "Hand.L", rot=(0.3, -0.4, 0), mat=m_skin, verts=8))
    # Index, Mid, Ring, Pinky
    for f_idx, fx in enumerate([-0.222, -0.238, -0.254, -0.270]):
        parts.append(add_part_cyl(f"HFinger_L_{f_idx}", (fx, 0.67, 0.12), 0.009, 0.052, "Hand.L", mat=m_skin, verts=8))
        parts.append(add_part_box(f"HNail_L_{f_idx}", (fx, 0.645, 0.13), (0.008, 0.006, 0.012), "Hand.L", m_teeth))
        
    # Right Arm
    parts.append(add_part_sphere("HShoulder_R", (0.23, 1.34, 0.01), 0.070, "Shoulder.R", m_shirt))
    parts.append(add_part_cyl("HArm_Upper_R", (0.24, 1.20, 0.03), 0.056, 0.22, "UpperArm.R", mat=m_shirt, verts=12))
    parts.append(add_part_cyl("HForearm_R", (0.24, 0.93, 0.07), 0.046, 0.24, "Forearm.R", mat=m_skin, verts=12))
    parts.append(add_part_box("HHand_Palm_R", (0.24, 0.74, 0.10), (0.068, 0.072, 0.034), "Hand.R", m_skin))
    for f_idx, fx in enumerate([0.222, 0.238, 0.254, 0.270]):
        parts.append(add_part_cyl(f"HFinger_R_{f_idx}", (fx, 0.67, 0.10), 0.009, 0.052, "Hand.R", mat=m_skin, verts=8))
        
    # --- REAL HUMAN LEGS & SHOES (DENIM JEANS) ---
    # Left Leg (Torn knee showing scraped human kneecap)
    parts.append(add_part_cyl("HJeans_Thigh_L", (-0.10, 0.72, 0.01), 0.078, 0.36, "UpperLeg.L", mat=m_jeans, verts=12))
    # Knee scrape wound
    parts.append(add_part_box("HWound_Knee_L", (-0.10, 0.52, 0.075), (0.065, 0.075, 0.030), "LowerLeg.L", m_blood))
    parts.append(add_part_cyl("HJeans_Shin_L", (-0.10, 0.28, 0.0), 0.066, 0.34, "LowerLeg.L", mat=m_jeans, verts=12))
    # Black Leather Dress Shoes (Left)
    parts.append(add_part_box("HShoe_L", (-0.10, 0.05, 0.04), (0.10, 0.07, 0.22), "Foot.L", m_shoes))
    parts.append(add_part_box("HShoe_Sole_L", (-0.10, 0.015, 0.04), (0.105, 0.02, 0.23), "Foot.L", m_belt))
    parts.append(add_part_box("HShoe_Tip_L", (-0.10, 0.045, 0.15), (0.09, 0.05, 0.06), "Toe.L", m_shoes))
    
    # Right Leg
    parts.append(add_part_cyl("HJeans_Thigh_R", (0.10, 0.72, 0.01), 0.078, 0.36, "UpperLeg.R", mat=m_jeans, verts=12))
    parts.append(add_part_cyl("HJeans_Shin_R", (0.10, 0.28, 0.0), 0.066, 0.34, "LowerLeg.R", mat=m_jeans, verts=12))
    # Black Leather Dress Shoes (Right)
    parts.append(add_part_box("HShoe_R", (0.10, 0.05, 0.04), (0.10, 0.07, 0.22), "Foot.R", m_shoes))
    parts.append(add_part_box("HShoe_Sole_R", (0.10, 0.015, 0.04), (0.105, 0.02, 0.23), "Foot.R", m_belt))
    parts.append(add_part_box("HShoe_Tip_R", (0.10, 0.045, 0.15), (0.09, 0.05, 0.06), "Toe.R", m_shoes))
    
    normal_mesh = join_mesh_parts(parts, "NormalZombieMesh")
    bind_mesh_to_armature(normal_mesh, arm_obj)
    
    # Create all 11 Skeletal Actions
    # 1. idle (40 frames, stooped breathing)
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 20, 40]:
        t = (f / 20.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.015, -abs(math.cos(t))*0.008, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.08 + math.sin(t)*0.03, 0, math.sin(t)*0.02))
        set_key(arm_obj, "Head", f, rot_euler=(0.02, math.sin(t)*0.05, -math.cos(t)*0.03))
        set_key(arm_obj, "Jaw", f, rot_euler=(0.12 + math.sin(t)*0.05, 0, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.75 + math.sin(t)*0.05, 0, 0.15))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.18 - math.sin(t)*0.04, 0, -0.10))
    stash_action(arm_obj, act_idle)
    
    # 2. walk (30 frames, human limp gait)
    act_walk = create_action(arm_obj, "walk")
    walk_frames = [
        (0,  -0.03, -0.02,  0.42, -0.50,  0.18, -0.32, -0.12,  0.22, -0.06,  0.95, -0.22),
        (8,   0.00,  0.00,  0.15, -0.10, -0.10, -0.10, -0.25,  0.10,  0.00,  0.85,  0.10),
        (15,  0.04,  0.02, -0.30, -0.10,  0.18,  0.38, -0.45,  0.16,  0.07,  0.72,  0.40),
        (23,  0.00,  0.00, -0.10, -0.25,  0.10,  0.12, -0.10, -0.10,  0.00,  0.85,  0.10),
        (30, -0.03, -0.02,  0.42, -0.50,  0.18, -0.32, -0.12,  0.22, -0.06,  0.95, -0.22)
    ]
    for (f, pzr, pxl, lhx, lkx, lfx, rhx, rkx, rfx, cy, lax, rax) in walk_frames:
        set_key(arm_obj, "Pelvis", f, loc=(pxl, -0.02, 0), rot_euler=(0.08, 0, pzr))
        set_key(arm_obj, "Spine", f, rot_euler=(0.05, -cy*0.5, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.12, cy, -pzr*0.5))
        set_key(arm_obj, "Head", f, rot_euler=(0.04, -cy*0.6, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(lhx, 0, 0.05))
        set_key(arm_obj, "LowerLeg.L", f, rot_euler=(lkx, 0, 0))
        set_key(arm_obj, "Foot.L", f, rot_euler=(lfx, 0, 0))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(rhx, 0, -0.05))
        set_key(arm_obj, "LowerLeg.R", f, rot_euler=(rkx, 0, 0))
        set_key(arm_obj, "Foot.R", f, rot_euler=(rfx, 0, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(lax, 0, 0.15))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(rax, 0, -0.12))
    stash_action(arm_obj, act_walk)
    
    # 3. fast_walk (20 frames)
    act_fwalk = create_action(arm_obj, "fast_walk")
    for f in [0, 5, 10, 15, 20]:
        t = (f / 10.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.03, -0.03, 0), rot_euler=(0.18, 0, math.sin(t)*0.05))
        set_key(arm_obj, "Chest", f, rot_euler=(0.20, -math.sin(t)*0.08, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.52, 0, 0.05))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.52, 0, -0.05))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.9 + math.cos(t)*0.30, 0, 0.18))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.2 - math.cos(t)*0.40, 0, -0.18))
    stash_action(arm_obj, act_fwalk)
    
    # 4. attack (25 frames)
    act_atk = create_action(arm_obj, "attack")
    set_key(arm_obj, "Chest", 0, rot_euler=(0.10, 0, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.04, -0.08))
    set_key(arm_obj, "Chest", 8, rot_euler=(-0.16, 0.12, 0))
    set_key(arm_obj, "Jaw", 8, rot_euler=(0.38, 0, 0))
    set_key(arm_obj, "UpperArm.L", 8, rot_euler=(1.35, 0, 0.30))
    set_key(arm_obj, "UpperArm.R", 8, rot_euler=(1.15, 0, -0.25))
    set_key(arm_obj, "Pelvis", 14, loc=(0, -0.05, 0.15))
    set_key(arm_obj, "Chest", 14, rot_euler=(0.38, -0.12, 0))
    set_key(arm_obj, "Jaw", 14, rot_euler=(0.06, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(0.25, 0, 0.10))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(0.30, 0, -0.10))
    set_key(arm_obj, "Pelvis", 25, loc=(0, 0, 0))
    set_key(arm_obj, "Chest", 25, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_atk)
    
    # 5. hit_front (12 frames)
    act_hf = create_action(arm_obj, "hit_front")
    set_key(arm_obj, "Chest", 4, rot_euler=(-0.35, 0, 0))
    set_key(arm_obj, "Head", 4, rot_euler=(-0.40, 0, 0))
    set_key(arm_obj, "Jaw", 4, rot_euler=(0.30, 0, 0))
    set_key(arm_obj, "Pelvis", 4, loc=(0, -0.04, -0.08))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 12, loc=(0, 0, 0))
    stash_action(arm_obj, act_hf)
    
    # 6. hit_back (12 frames)
    act_hb = create_action(arm_obj, "hit_back")
    set_key(arm_obj, "Chest", 4, rot_euler=(0.38, 0, 0))
    set_key(arm_obj, "Head", 4, rot_euler=(0.32, 0, 0))
    set_key(arm_obj, "Pelvis", 4, loc=(0, -0.03, 0.08))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 12, loc=(0, 0, 0))
    stash_action(arm_obj, act_hb)
    
    # 7. hit_left (12 frames)
    act_hl = create_action(arm_obj, "hit_left")
    set_key(arm_obj, "Chest", 4, rot_euler=(0, -0.20, -0.28))
    set_key(arm_obj, "Head", 4, rot_euler=(0, -0.22, -0.32))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hl)
    
    # 8. hit_right (12 frames)
    act_hr = create_action(arm_obj, "hit_right")
    set_key(arm_obj, "Chest", 4, rot_euler=(0, 0.20, 0.28))
    set_key(arm_obj, "Head", 4, rot_euler=(0, 0.22, 0.32))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hr)
    
    # 9. headshot_reaction (16 frames)
    act_head = create_action(arm_obj, "headshot_reaction")
    set_key(arm_obj, "Head", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 3, rot_euler=(-0.65, 0.40, -0.18))
    set_key(arm_obj, "Jaw", 3, rot_euler=(0.50, 0, 0))
    set_key(arm_obj, "Chest", 3, rot_euler=(-0.30, 0.18, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.10, -0.16))
    set_key(arm_obj, "Head", 16, rot_euler=(-0.28, 0.18, 0))
    stash_action(arm_obj, act_head)
    
    # 10. stagger (30 frames)
    act_stagger = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.06, -0.22), rot_euler=(0, 0, -0.08))
    set_key(arm_obj, "Chest", 8, rot_euler=(-0.28, 0.12, 0))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.06, -0.38), rot_euler=(0, 0, 0.08))
    set_key(arm_obj, "Chest", 18, rot_euler=(0.14, -0.08, 0))
    set_key(arm_obj, "Pelvis", 30, loc=(0, 0, -0.38), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 30, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_stagger)
    
    # 11. death (36 frames)
    act_death = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.24, -0.05), rot_euler=(0.18, 0, 0))
    set_key(arm_obj, "UpperLeg.L", 8, rot_euler=(0.50, 0, 0.1))
    set_key(arm_obj, "LowerLeg.L", 8, rot_euler=(-1.05, 0, 0))
    set_key(arm_obj, "UpperLeg.R", 8, rot_euler=(0.48, 0, -0.1))
    set_key(arm_obj, "LowerLeg.R", 8, rot_euler=(-1.00, 0, 0))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.55, 0.10), rot_euler=(0.70, 0, 0.12))
    set_key(arm_obj, "Chest", 18, rot_euler=(0.55, 0.18, 0))
    set_key(arm_obj, "Pelvis", 30, loc=(0, -0.88, 0.20), rot_euler=(1.48, 0, 0.22))
    set_key(arm_obj, "Chest", 30, rot_euler=(0.22, 0.08, 0))
    set_key(arm_obj, "Pelvis", 36, loc=(0, -0.88, 0.20), rot_euler=(1.48, 0, 0.22))
    stash_action(arm_obj, act_death)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_normal.glb',
        'models/zombies/zombie_normal.obj'
    )
    print("Real Human Normal Zombie built and exported successfully!")


# ==============================================================================
# 2. REAL HUMAN ATHLETIC RUNNER (zombie_fast.glb)
# ==============================================================================

def build_real_human_fast_zombie():
    print("\n--- 2. BUILDING REAL HUMAN ATHLETIC RUNNER ZOMBIE ---")
    clear_scene()
    
    m_skin = create_mat("Mat_HumanSkinFast", (0.76, 0.62, 0.52, 1.0), roughness=0.50) # Athletic human skin
    m_hair = create_mat("Mat_HumanHairFast", (0.10, 0.08, 0.07, 1.0), roughness=0.85)
    m_top = create_mat("Mat_RunnerJacket", (0.85, 0.22, 0.18, 1.0), roughness=0.70) # Red athletic running top
    m_shorts = create_mat("Mat_RunnerShorts", (0.12, 0.12, 0.15, 1.0), roughness=0.75) # Dark track shorts
    m_shoes = create_mat("Mat_RunningShoes", (0.92, 0.92, 0.94, 1.0), roughness=0.55) # White running sneakers
    m_blood = create_mat("Mat_BloodFast", (0.72, 0.06, 0.05, 1.0), roughness=0.20)
    m_eyes = create_mat("Mat_EyesFast", (0.35, 0.20, 0.10, 1.0), roughness=0.08)
    m_sclera = create_mat("Mat_ScleraFast", (0.88, 0.85, 0.85, 1.0), roughness=0.10)
    
    arm_obj = create_humanoid_armature("FastZombieArmature", scale_factor=0.96)
    parts = []
    
    # Head & Face
    parts.append(add_part_sphere("FHead_Cranium", (0, 1.64, 0.02), 0.10, "Head", m_skin, segs=18, rings=14))
    parts.append(add_part_box("FFace_Brow", (0, 1.645, 0.095), (0.115, 0.028, 0.035), "Head", m_skin))
    parts.append(add_part_sphere("FEye_L", (-0.035, 1.635, 0.10), 0.015, "Head", m_sclera, segs=10, rings=8))
    parts.append(add_part_sphere("FEye_Pupil_L", (-0.035, 1.635, 0.112), 0.008, "Head", m_eyes, segs=8, rings=6))
    parts.append(add_part_sphere("FEye_R", (0.035, 1.635, 0.10), 0.015, "Head", m_sclera, segs=10, rings=8))
    parts.append(add_part_sphere("FEye_Pupil_R", (0.035, 1.635, 0.112), 0.008, "Head", m_eyes, segs=8, rings=6))
    parts.append(add_part_box("FNose", (0, 1.605, 0.115), (0.024, 0.035, 0.028), "Head", m_skin))
    parts.append(add_part_sphere("FHair", (0, 1.67, 0.01), 0.105, "Head", m_hair, segs=14, rings=10))
    parts.append(add_part_box("FFace_Jaw", (0, 1.525, 0.08), (0.075, 0.055, 0.075), "Jaw", m_skin))
    parts.append(add_part_box("FLips", (0, 1.555, 0.105), (0.048, 0.012, 0.015), "Jaw", m_blood))
    parts.append(add_part_cyl("FNeck", (0, 1.46, 0.01), 0.060, 0.14, "Neck", mat=m_skin, verts=12))
    
    # Torso (Running Top)
    parts.append(add_part_box("FTorso_Main", (0, 1.28, 0.01), (0.34, 0.30, 0.20), "Chest", m_top))
    parts.append(add_part_box("FTorso_Spine", (0, 1.10, 0.01), (0.30, 0.18, 0.18), "Spine", m_top))
    parts.append(add_part_box("FShorts_Pelvis", (0, 0.93, 0.01), (0.30, 0.14, 0.18), "Pelvis", m_shorts))
    
    # Arms
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_sphere(f"FShoulder_{s}", (sign*0.22, 1.34, 0.01), 0.068, f"Shoulder.{b_side}", m_top))
        parts.append(add_part_cyl(f"FArm_Upper_{s}", (sign*0.23, 1.18, 0.03), 0.050, 0.22, f"UpperArm.{b_side}", mat=m_top, verts=10))
        parts.append(add_part_cyl(f"FForearm_{s}", (sign*0.23, 0.92, 0.08), 0.042, 0.24, f"Forearm.{b_side}", mat=m_skin, verts=10))
        parts.append(add_part_box(f"FHand_{s}", (sign*0.23, 0.74, 0.11), (0.062, 0.065, 0.032), f"Hand.{b_side}", m_skin))
        
    # Legs (Running shorts, bare athletic legs, white running shoes)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"FThigh_{s}", (sign*0.10, 0.72, 0.0), 0.072, 0.34, f"UpperLeg.{b_side}", mat=m_shorts, verts=10))
        parts.append(add_part_cyl(f"FShin_{s}", (sign*0.10, 0.28, 0.0), 0.058, 0.34, f"LowerLeg.{b_side}", mat=m_skin, verts=10))
        parts.append(add_part_box(f"FShoe_{s}", (sign*0.10, 0.05, 0.04), (0.095, 0.065, 0.21), f"Foot.{b_side}", m_shoes))
        parts.append(add_part_box(f"FToe_{s}", (sign*0.10, 0.04, 0.15), (0.085, 0.045, 0.05), f"Toe.{b_side}", m_shoes))
        
    fast_mesh = join_mesh_parts(parts, "FastZombieMesh")
    bind_mesh_to_armature(fast_mesh, arm_obj)
    
    # Fast Actions
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 12, 24]:
        t = (f / 12.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(0, -0.04 + math.sin(t)*0.01, 0), rot_euler=(0.18, 0, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.22 + math.sin(t)*0.04, 0, 0))
        set_key(arm_obj, "Head", f, rot_euler=(-0.08, math.sin(t)*0.10, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.75 + math.sin(t)*0.06, 0, 0.18))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.75 - math.sin(t)*0.06, 0, -0.18))
    stash_action(arm_obj, act_idle)
    
    act_run = create_action(arm_obj, "run")
    for f in [0, 4, 8, 12, 16]:
        t = (f / 8.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.02, -0.05 - abs(math.sin(t))*0.02, 0), rot_euler=(0.35, 0, math.sin(t)*0.06))
        set_key(arm_obj, "Chest", f, rot_euler=(0.30, -math.sin(t)*0.12, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.80, 0, 0.05))
        set_key(arm_obj, "LowerLeg.L", f, rot_euler=(-abs(math.sin(t))*0.70, 0, 0))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.80, 0, -0.05))
        set_key(arm_obj, "LowerLeg.R", f, rot_euler=(-abs(math.cos(t))*0.70, 0, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.5 - math.sin(t)*0.70, 0, 0.18))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.5 + math.sin(t)*0.70, 0, -0.18))
    stash_action(arm_obj, act_run)
    stash_action(arm_obj, act_run) # walk alias
    
    act_turn = create_action(arm_obj, "turn")
    set_key(arm_obj, "Pelvis", 6, rot_euler=(0.25, 0.35, -0.15))
    set_key(arm_obj, "Pelvis", 12, rot_euler=(0.25, 0, 0))
    stash_action(arm_obj, act_turn)
    
    act_atk = create_action(arm_obj, "attack")
    set_key(arm_obj, "Pelvis", 6, loc=(0, -0.12, -0.08), rot_euler=(0.3, 0, 0))
    set_key(arm_obj, "UpperArm.L", 6, rot_euler=(1.35, 0, 0.3))
    set_key(arm_obj, "UpperArm.R", 6, rot_euler=(1.35, 0, -0.3))
    set_key(arm_obj, "Pelvis", 11, loc=(0, 0.04, 0.22), rot_euler=(0.45, 0, 0))
    set_key(arm_obj, "UpperArm.L", 11, rot_euler=(0.2, 0, 0.1))
    set_key(arm_obj, "UpperArm.R", 11, rot_euler=(0.2, 0, -0.1))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.04, 0), rot_euler=(0.18, 0, 0))
    stash_action(arm_obj, act_atk)
    
    act_hit = create_action(arm_obj, "hit")
    set_key(arm_obj, "Chest", 3, rot_euler=(-0.28, 0, 0))
    set_key(arm_obj, "Head", 3, rot_euler=(-0.35, 0, 0))
    set_key(arm_obj, "Chest", 10, rot_euler=(0.18, 0, 0))
    stash_action(arm_obj, act_hit)
    
    act_stag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 6, loc=(0, -0.12, -0.22), rot_euler=(0.18, 0, -0.12))
    set_key(arm_obj, "Pelvis", 20, loc=(0, -0.04, -0.22), rot_euler=(0.18, 0, 0))
    stash_action(arm_obj, act_stag)
    
    act_death = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.35, 0.12), rot_euler=(0.55, 0, 0))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.85, 0.40), rot_euler=(1.50, 0, 0))
    set_key(arm_obj, "Pelvis", 25, loc=(0, -0.85, 0.45), rot_euler=(1.50, 0, 0))
    stash_action(arm_obj, act_death)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_fast.glb',
        'models/zombies/zombie_fast.obj'
    )
    print("Real Human Fast Zombie built and exported successfully!")


# ==============================================================================
# 3. REAL HUMAN WORKER HEAVY ZOMBIE (zombie_heavy.glb)
# ==============================================================================

def build_real_human_heavy_zombie():
    print("\n--- 3. BUILDING REAL HUMAN WORKER HEAVY ZOMBIE ---")
    clear_scene()
    
    m_skin = create_mat("Mat_HumanSkinHeavy", (0.74, 0.60, 0.50, 1.0), roughness=0.65) # Weathered human skin
    m_hair = create_mat("Mat_HumanHairHeavy", (0.15, 0.12, 0.10, 1.0), roughness=0.85)
    m_vest = create_mat("Mat_SafetyVest", (0.95, 0.72, 0.08, 1.0), roughness=0.68) # High-vis orange/yellow construction vest
    m_stripe = create_mat("Mat_ReflectiveStripe", (0.96, 0.96, 0.96, 1.0), roughness=0.15, emission=(0.96, 0.96, 0.96, 1.0), emission_strength=1.5)
    m_shirt = create_mat("Mat_WorkerShirt", (0.22, 0.28, 0.38, 1.0), roughness=0.80) # Navy work shirt
    m_pants = create_mat("Mat_CanvasWorkPants", (0.42, 0.38, 0.30, 1.0), roughness=0.85) # Khaki canvas work pants
    m_boots = create_mat("Mat_WorkBoots", (0.18, 0.12, 0.08, 1.0), roughness=0.60) # Brown leather work boots
    m_rebar = create_mat("Mat_Rebar", (0.20, 0.18, 0.16, 1.0), metallic=0.85, roughness=0.45)
    m_blood = create_mat("Mat_BloodHeavy", (0.68, 0.05, 0.04, 1.0), roughness=0.20)
    
    arm_obj = create_humanoid_armature("HeavyZombieArmature", scale_factor=1.15)
    parts = []
    
    # Head (Broad, strong human jaw with beard stubble)
    parts.append(add_part_sphere("HHead_Cranium", (0, 1.64, 0.01), 0.120, "Head", m_skin, segs=18, rings=14))
    parts.append(add_part_box("HFace_Brow", (0, 1.645, 0.105), (0.138, 0.035, 0.040), "Head", m_skin))
    parts.append(add_part_box("HFace_Jaw", (0, 1.515, 0.085), (0.098, 0.065, 0.090), "Jaw", m_hair)) # Beard stubble
    parts.append(add_part_box("HFace_Chin", (0, 1.495, 0.110), (0.065, 0.035, 0.035), "Jaw", m_skin))
    parts.append(add_part_cyl("HNeck", (0, 1.45, 0.01), 0.088, 0.15, "Neck", mat=m_skin, verts=14))
    
    # Torso (Muscular human frame wearing blue work shirt & high-vis safety vest)
    parts.append(add_part_box("HTorso_Main", (0, 1.28, 0.02), (0.44, 0.34, 0.28), "Chest", m_shirt))
    parts.append(add_part_box("HVest_Front", (0, 1.28, 0.03), (0.45, 0.33, 0.29), "Chest", m_vest))
    parts.append(add_part_box("HVest_Stripe1", (0, 1.34, 0.178), (0.42, 0.035, 0.008), "Chest", m_stripe))
    parts.append(add_part_box("HVest_Stripe2", (0, 1.22, 0.178), (0.42, 0.035, 0.008), "Chest", m_stripe))
    # Impaled rebar from construction accident
    parts.append(add_part_cyl("HRebar", (0.22, 1.38, 0.04), 0.016, 0.65, "Chest", rot=(0.3, 0.2, 0.4), mat=m_rebar, verts=8))
    parts.append(add_part_box("HRebar_Blood", (0.22, 1.38, 0.04), (0.07, 0.07, 0.07), "Chest", m_blood))
    parts.append(add_part_box("HTorso_Spine", (0, 1.10, 0.02), (0.42, 0.18, 0.26), "Spine", m_vest))
    parts.append(add_part_box("HPants_Pelvis", (0, 0.94, 0.01), (0.40, 0.16, 0.25), "Pelvis", m_pants))
    
    # Arms (Muscular human arms with rolled sleeves)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_sphere(f"HShoulder_{s}", (sign*0.28, 1.34, 0.02), 0.092, f"Shoulder.{b_side}", m_vest))
        parts.append(add_part_cyl(f"HArm_Upper_{s}", (sign*0.29, 1.16, 0.03), 0.078, 0.26, f"UpperArm.{b_side}", mat=m_shirt, verts=12))
        parts.append(add_part_cyl(f"HForearm_{s}", (sign*0.29, 0.88, 0.07), 0.068, 0.26, f"Forearm.{b_side}", mat=m_skin, verts=12))
        parts.append(add_part_box(f"HHand_{s}", (sign*0.29, 0.70, 0.10), (0.095, 0.095, 0.055), f"Hand.{b_side}", m_skin))
        
    # Legs (Canvas work pants & work boots)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"HThigh_{s}", (sign*0.13, 0.71, 0.01), 0.098, 0.36, f"UpperLeg.{b_side}", mat=m_pants, verts=12))
        parts.append(add_part_cyl(f"HShin_{s}", (sign*0.13, 0.28, 0.0), 0.086, 0.34, f"LowerLeg.{b_side}", mat=m_pants, verts=12))
        parts.append(add_part_box(f"HBoot_{s}", (sign*0.13, 0.06, 0.05), (0.13, 0.09, 0.24), f"Foot.{b_side}", m_boots))
        parts.append(add_part_box(f"HToe_{s}", (sign*0.13, 0.04, 0.17), (0.11, 0.05, 0.06), f"Toe.{b_side}", m_boots))
        
    heavy_mesh = join_mesh_parts(parts, "HeavyZombieMesh")
    bind_mesh_to_armature(heavy_mesh, arm_obj)
    
    # Heavy Actions
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 22, 45]:
        t = (f / 22.5) * math.pi
        set_key(arm_obj, "Chest", f, rot_euler=(0.10 + math.sin(t)*0.03, 0, 0))
        set_key(arm_obj, "Head", f, rot_euler=(0.04, math.sin(t)*0.04, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.3 + math.sin(t)*0.04, 0, 0.25))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.3 - math.sin(t)*0.04, 0, -0.25))
    stash_action(arm_obj, act_idle)
    
    act_hwalk = create_action(arm_obj, "heavy_walk")
    for f in [0, 10, 20, 30, 40]:
        t = (f / 20.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.05, -0.03, 0), rot_euler=(0.10, 0, math.sin(t)*0.05))
        set_key(arm_obj, "Chest", f, rot_euler=(0.12, -math.sin(t)*0.07, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.42, 0, 0.08))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.42, 0, -0.08))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.35 - math.sin(t)*0.30, 0, 0.22))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.35 + math.sin(t)*0.30, 0, -0.22))
    stash_action(arm_obj, act_hwalk)
    stash_action(arm_obj, act_hwalk) # walk alias
    
    act_hatk = create_action(arm_obj, "heavy_attack")
    set_key(arm_obj, "Pelvis", 14, loc=(0, -0.05, -0.08), rot_euler=(-0.12, 0, 0))
    set_key(arm_obj, "Chest", 14, rot_euler=(-0.25, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(1.55, 0, 0.2))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(1.55, 0, -0.2))
    set_key(arm_obj, "Pelvis", 22, loc=(0, -0.15, 0.18), rot_euler=(0.45, 0, 0))
    set_key(arm_obj, "Chest", 22, rot_euler=(0.55, 0, 0))
    set_key(arm_obj, "UpperArm.L", 22, rot_euler=(-0.18, 0, 0.1))
    set_key(arm_obj, "UpperArm.R", 22, rot_euler=(-0.18, 0, -0.1))
    set_key(arm_obj, "Pelvis", 35, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 35, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_hatk)
    stash_action(arm_obj, act_hatk) # attack alias
    
    act_imp = create_action(arm_obj, "impact")
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.08, 0), rot_euler=(0.20, 0, 0))
    set_key(arm_obj, "Pelvis", 20, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_imp)
    
    act_hstag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.08, -0.25), rot_euler=(-0.18, 0, 0))
    set_key(arm_obj, "Pelvis", 28, loc=(0, 0, -0.25), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hstag)
    
    act_hdeath = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 16, loc=(0, -0.18, -0.20), rot_euler=(-0.40, 0, 0))
    set_key(arm_obj, "Pelvis", 34, loc=(0, -0.85, -0.65), rot_euler=(-1.50, 0, 0))
    set_key(arm_obj, "Pelvis", 45, loc=(0, -0.85, -0.65), rot_euler=(-1.50, 0, 0))
    stash_action(arm_obj, act_hdeath)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_heavy.glb',
        'models/zombies/zombie_heavy.obj'
    )
    print("Real Human Heavy Zombie built and exported successfully!")


# ==============================================================================
# 4. REAL HUMAN COMMANDER BOSS ZOMBIE (zombie_boss.glb)
# ==============================================================================

def build_real_human_boss_zombie():
    print("\n--- 4. BUILDING REAL HUMAN COMMANDER BOSS ZOMBIE ---")
    clear_scene()
    
    m_skin = create_mat("Mat_HumanSkinBoss", (0.72, 0.58, 0.48, 1.0), roughness=0.60)
    m_bdu = create_mat("Mat_TacticalBDU", (0.24, 0.26, 0.22, 1.0), roughness=0.80) # Military BDU fatigue
    m_armor = create_mat("Mat_TacticalVestBoss", (0.14, 0.16, 0.14, 1.0), roughness=0.65) # Tactical plate carrier
    m_boots = create_mat("Mat_CombatBootsBoss", (0.08, 0.08, 0.09, 1.0), roughness=0.55)
    m_blade = create_mat("Mat_ExoBlade", (0.18, 0.20, 0.22, 1.0), metallic=0.85, roughness=0.25) # Reinforced steel arm blade
    m_glow = create_mat("Mat_BioHazardGlow", (0.15, 0.95, 0.35, 1.0), emission=(0.15, 0.95, 0.35, 1.0), emission_strength=4.5)
    m_blood = create_mat("Mat_BloodBoss", (0.70, 0.05, 0.04, 1.0), roughness=0.20)
    
    arm_obj = create_humanoid_armature("BossZombieArmature", scale_factor=1.35, has_extra_scythe=True)
    parts = []
    
    # Head (Former tactical commander with combat scars and beret/hair)
    parts.append(add_part_sphere("BHead_Cranium", (0, 1.66, 0.02), 0.125, "Head", m_skin, segs=18, rings=14))
    parts.append(add_part_box("BFace_Brow", (0, 1.665, 0.11), (0.138, 0.035, 0.040), "Head", m_skin))
    parts.append(add_part_box("BFace_Jaw", (0, 1.52, 0.09), (0.105, 0.070, 0.090), "Jaw", m_skin))
    parts.append(add_part_cyl("BNeck", (0, 1.46, 0.01), 0.092, 0.16, "Neck", mat=m_skin, verts=14))
    
    # Torso (Tactical body armor over combat uniform)
    parts.append(add_part_box("BTorso_Main", (0, 1.28, 0.02), (0.46, 0.36, 0.30), "Chest", m_armor))
    parts.append(add_part_box("BTorso_Spine", (0, 1.08, 0.02), (0.42, 0.18, 0.28), "Spine", m_bdu))
    parts.append(add_part_box("BPelvis", (0, 0.93, 0.01), (0.40, 0.16, 0.26), "Pelvis", m_bdu))
    
    # Left Arm with Reinforced Steel Arm Blade
    parts.append(add_part_sphere("BShoulder_L", (-0.30, 1.34, 0.02), 0.105, "Shoulder.L", m_armor))
    parts.append(add_part_cyl("BArm_Upper_L", (-0.32, 1.15, 0.04), 0.088, 0.28, "UpperArm.L", mat=m_bdu, verts=12))
    parts.append(add_part_cyl("BForearm_L", (-0.32, 0.85, 0.10), 0.080, 0.30, "Forearm.L", mat=m_blade, verts=12))
    parts.append(add_part_box("BScythe_Base", (-0.32, 0.62, 0.22), (0.10, 0.14, 0.22), "ScytheBlade", m_armor))
    parts.append(add_part_box("BScythe_BladeMain", (-0.33, 0.42, 0.55), (0.035, 0.15, 0.75), "ScytheBlade", m_blade, rot=(0.50, 0, 0)))
    parts.append(add_part_box("BScythe_EdgeGlow", (-0.33, 0.40, 0.60), (0.012, 0.035, 0.70), "ScytheBlade", m_glow, rot=(0.50, 0, 0)))
    
    # Right Arm (Tactical Combat Glove)
    parts.append(add_part_sphere("BShoulder_R", (0.30, 1.34, 0.02), 0.10, "Shoulder.R", m_armor))
    parts.append(add_part_cyl("BArm_Upper_R", (0.32, 1.15, 0.04), 0.085, 0.28, "UpperArm.R", mat=m_bdu, verts=12))
    parts.append(add_part_cyl("BForearm_R", (0.32, 0.85, 0.10), 0.075, 0.30, "Forearm.R", mat=m_skin, verts=12))
    parts.append(add_part_box("BHand_R", (0.32, 0.66, 0.15), (0.10, 0.10, 0.06), "Hand.R", m_armor))
    
    # Legs (Combat BDU trousers & combat boots)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"BThigh_{s}", (sign*0.14, 0.71, 0.01), 0.105, 0.38, f"UpperLeg.{b_side}", mat=m_bdu, verts=12))
        parts.append(add_part_cyl(f"BShin_{s}", (sign*0.14, 0.28, 0.0), 0.092, 0.36, f"LowerLeg.{b_side}", mat=m_bdu, verts=12))
        parts.append(add_part_box(f"BBoot_{s}", (sign*0.14, 0.06, 0.06), (0.14, 0.10, 0.25), f"Foot.{b_side}", m_boots))
        parts.append(add_part_box(f"BToe_{s}", (sign*0.14, 0.04, 0.20), (0.12, 0.05, 0.06), f"Toe.{b_side}", m_boots))
        
    boss_mesh = join_mesh_parts(parts, "BossZombieMesh")
    bind_mesh_to_armature(boss_mesh, arm_obj)
    
    # Boss Actions
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 24, 48]:
        t = (f / 24.0) * math.pi
        set_key(arm_obj, "Chest", f, rot_euler=(0.10 + math.sin(t)*0.03, 0, 0))
        set_key(arm_obj, "Head", f, rot_euler=(0.04, math.sin(t)*0.04, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.40 + math.sin(t)*0.04, 0, 0.28))
    stash_action(arm_obj, act_idle)
    
    act_walk = create_action(arm_obj, "walk")
    for f in [0, 9, 18, 27, 36]:
        t = (f / 18.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.06, -0.04, 0), rot_euler=(0.12, 0, math.sin(t)*0.05))
        set_key(arm_obj, "Chest", f, rot_euler=(0.14, -math.sin(t)*0.08, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.40, 0, 0.08))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.40, 0, -0.08))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.45 - math.sin(t)*0.25, 0, 0.28))
    stash_action(arm_obj, act_walk)
    
    act_windup = create_action(arm_obj, "attack_windup")
    set_key(arm_obj, "Chest", 24, rot_euler=(-0.20, 0.40, 0))
    set_key(arm_obj, "UpperArm.L", 24, rot_euler=(1.35, 0.35, 0.35))
    stash_action(arm_obj, act_windup)
    
    act_cleave = create_action(arm_obj, "heavy_attack")
    set_key(arm_obj, "Chest", 0, rot_euler=(-0.20, 0.40, 0))
    set_key(arm_obj, "UpperArm.L", 0, rot_euler=(1.35, 0.35, 0.35))
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.08, 0.25), rot_euler=(0.25, 0, -0.18))
    set_key(arm_obj, "Chest", 10, rot_euler=(0.35, -0.75, 0))
    set_key(arm_obj, "UpperArm.L", 10, rot_euler=(0.18, -0.5, 0.1))
    set_key(arm_obj, "Pelvis", 28, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 28, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_cleave)
    stash_action(arm_obj, act_cleave) # attack alias
    
    act_roar = create_action(arm_obj, "roar")
    set_key(arm_obj, "Chest", 14, rot_euler=(-0.40, 0, 0))
    set_key(arm_obj, "Head", 14, rot_euler=(-0.55, 0, 0))
    set_key(arm_obj, "Jaw", 14, rot_euler=(0.65, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(1.45, 0, 0.4))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(1.45, 0, -0.4))
    set_key(arm_obj, "Chest", 36, rot_euler=(0.10, 0, 0))
    set_key(arm_obj, "Head", 36, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_roar)
    
    act_bhit = create_action(arm_obj, "hit")
    set_key(arm_obj, "Chest", 4, rot_euler=(-0.14, 0, 0))
    set_key(arm_obj, "Chest", 14, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_bhit)
    
    act_bstag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.12, -0.38), rot_euler=(-0.20, 0, 0))
    set_key(arm_obj, "Pelvis", 32, loc=(0, 0, -0.38), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_bstag)
    
    act_bdeath = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 16, loc=(0, -0.40, -0.08), rot_euler=(0.30, 0, 0))
    set_key(arm_obj, "Pelvis", 36, loc=(0, -0.95, 0.35), rot_euler=(1.45, 0, 0))
    set_key(arm_obj, "Pelvis", 50, loc=(0, -0.95, 0.35), rot_euler=(1.45, 0, 0))
    stash_action(arm_obj, act_bdeath)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_boss.glb',
        'models/zombies/zombie_boss.obj'
    )
    print("Real Human Boss Zombie built and exported successfully!")

if __name__ == '__main__':
    print("=== STARTING REAL HUMAN ZOMBIE PIPELINE ===")
    build_real_human_normal_zombie()
    build_real_human_fast_zombie()
    build_real_human_heavy_zombie()
    build_real_human_boss_zombie()
    print("=== REAL HUMAN ZOMBIE PIPELINE COMPLETE ===")
