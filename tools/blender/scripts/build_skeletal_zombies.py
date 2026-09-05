"""
Sector Zero: Lockdown - Skeletal Zombie Asset Pipeline
Generates 23-bone human-like armatures, high-detail humanoid meshes with multi-material slots,
and full action libraries for Normal, Fast, Heavy, and Boss zombies.
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
    # Reset pose
    for pb in arm_obj.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.location = (0, 0, 0)
        pb.rotation_euler = (0, 0, 0)
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

print("Skeletal pipeline helper defined successfully.")

def build_skeletal_normal_zombie():
    print("\n--- BUILDING RIGGED HUMAN-LIKE NORMAL ZOMBIE ---")
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
    
    # 1. Armature
    arm_obj = create_humanoid_armature("NormalZombieArmature", scale_factor=1.0)
    
    # 2. Geometry with bone vertex groups
    parts = []
    
    # Head & Face
    parts.append(add_part_sphere("ZHead_Cranium", (0.01, 1.63, 0.02), 0.106, "Head", m_flesh, segs=20, rings=16))
    parts.append(add_part_box("ZFace_Brow", (0.01, 1.635, 0.115), (0.125, 0.030, 0.040), "Head", m_flesh))
    parts.append(add_part_sphere("ZEye_L", (-0.038, 1.625, 0.115), 0.017, "Head", m_eye_milky, segs=12, rings=10))
    parts.append(add_part_sphere("ZEye_R", (0.040, 1.625, 0.122), 0.019, "Head", m_eye_blood, segs=12, rings=10))
    parts.append(add_part_box("ZFace_Nose", (0.01, 1.585, 0.132), (0.028, 0.036, 0.030), "Head", m_flesh))
    parts.append(add_part_box("ZNasal_Hole", (0.01, 1.580, 0.142), (0.018, 0.018, 0.015), "Head", m_gore))
    parts.append(add_part_box("ZTeeth_Upper", (0.012, 1.545, 0.128), (0.062, 0.015, 0.020), "Head", m_bone))
    parts.append(add_part_sphere("ZHair_Patch", (0.0, 1.66, 0.01), 0.112, "Head", m_hair, segs=14, rings=10))
    
    # Jaw & Lower Teeth
    parts.append(add_part_box("ZFace_Jaw", (0.018, 1.505, 0.095), (0.080, 0.065, 0.080), "Jaw", m_flesh, rot=(0.18, 0.0, -0.14)))
    parts.append(add_part_box("ZTeeth_Lower", (0.020, 1.520, 0.120), (0.058, 0.015, 0.018), "Jaw", m_bone))
    parts.append(add_part_box("ZWound_Cheek", (0.065, 1.555, 0.095), (0.035, 0.055, 0.045), "Jaw", m_gore))
    parts.append(add_part_box("ZBone_Cheek", (0.062, 1.555, 0.105), (0.015, 0.035, 0.020), "Jaw", m_bone))
    
    # Neck
    parts.append(add_part_cyl("ZNeck", (0.015, 1.46, 0.02), 0.065, 0.14, "Neck", rot=(0.12, 0.0, 0.08), mat=m_flesh, verts=14))
    parts.append(add_part_box("ZNeck_Bite", (-0.042, 1.47, 0.045), (0.035, 0.045, 0.035), "Neck", m_gore))
    
    # Chest & Upper Torso
    parts.append(add_part_box("ZTorso_Main", (0.0, 1.28, 0.03), (0.35, 0.30, 0.22), "Chest", m_shirt, rot=(0.12, -0.05, 0.04)))
    parts.append(add_part_cyl("ZTorn_Collar", (0.01, 1.41, 0.03), 0.082, 0.05, "Chest", mat=m_shirt, verts=14))
    parts.append(add_part_box("ZWound_Chest", (-0.05, 1.34, 0.13), (0.09, 0.06, 0.03), "Chest", m_gore))
    parts.append(add_part_box("ZBone_Clavicle", (-0.05, 1.35, 0.14), (0.08, 0.015, 0.015), "Chest", m_bone))
    parts.append(add_part_box("ZWound_Ribs", (0.12, 1.22, 0.11), (0.12, 0.16, 0.07), "Chest", m_gore))
    parts.append(add_part_box("ZRib_1", (0.12, 1.27, 0.14), (0.095, 0.018, 0.025), "Chest", m_bone))
    parts.append(add_part_box("ZRib_2", (0.12, 1.21, 0.14), (0.090, 0.018, 0.025), "Chest", m_bone))
    parts.append(add_part_box("ZRib_3", (0.12, 1.15, 0.14), (0.085, 0.018, 0.025), "Chest", m_bone))
    
    # Spine & Midriff
    parts.append(add_part_box("ZTorso_Spine", (0.0, 1.11, 0.02), (0.32, 0.18, 0.20), "Spine", m_shirt))
    
    # Pelvis
    parts.append(add_part_box("ZPants_Pelvis", (0.0, 0.94, 0.01), (0.30, 0.14, 0.18), "Pelvis", m_pants))
    
    # Left Arm
    parts.append(add_part_sphere("ZShoulder_L", (-0.23, 1.32, 0.05), 0.072, "Shoulder.L", m_shirt))
    parts.append(add_part_cyl("ZArm_Upper_L", (-0.24, 1.20, 0.06), 0.056, 0.24, "UpperArm.L", rot=(math.radians(35), 0, 0), mat=m_shirt, verts=12))
    parts.append(add_part_cyl("ZTorn_Sleeve_L", (-0.24, 1.10, 0.09), 0.062, 0.03, "UpperArm.L", rot=(math.radians(35), 0, 0), mat=m_shirt, verts=12))
    parts.append(add_part_cyl("ZForearm_L", (-0.24, 0.92, 0.13), 0.046, 0.24, "Forearm.L", rot=(math.radians(45), 0, 0), mat=m_flesh, verts=12))
    parts.append(add_part_box("ZHand_L", (-0.24, 0.77, 0.18), (0.075, 0.075, 0.040), "Hand.L", m_flesh))
    for f_idx, fx in enumerate([-0.27, -0.255, -0.24, -0.225, -0.21]):
        parts.append(add_part_cyl(f"ZClaw_L_{f_idx}", (fx, 0.72, 0.21), 0.009, 0.055, "Hand.L", rot=(math.radians(45), 0, 0), mat=m_flesh, verts=6))
        parts.append(add_part_box(f"ZNail_L_{f_idx}", (fx, 0.69, 0.23), (0.010, 0.006, 0.018), "Hand.L", m_bone))
        
    # Right Arm
    parts.append(add_part_sphere("ZShoulder_R", (0.23, 1.32, 0.02), 0.070, "Shoulder.R", m_shirt))
    parts.append(add_part_cyl("ZArm_Upper_R", (0.24, 1.18, 0.04), 0.054, 0.24, "UpperArm.R", rot=(math.radians(20), 0, 0), mat=m_shirt, verts=12))
    parts.append(add_part_cyl("ZForearm_R", (0.24, 0.92, 0.10), 0.044, 0.24, "Forearm.R", rot=(math.radians(25), 0, 0), mat=m_flesh, verts=12))
    parts.append(add_part_box("ZWound_Forearm_R", (0.25, 0.92, 0.12), (0.025, 0.10, 0.025), "Forearm.R", m_gore))
    parts.append(add_part_box("ZHand_R", (0.24, 0.77, 0.14), (0.070, 0.070, 0.040), "Hand.R", m_flesh))
    
    # Left Leg
    parts.append(add_part_cyl("ZThigh_L", (-0.10, 0.71, 0.01), 0.076, 0.36, "UpperLeg.L", mat=m_pants, verts=12))
    parts.append(add_part_box("ZWound_Knee_L", (-0.10, 0.50, 0.065), (0.085, 0.095, 0.045), "LowerLeg.L", m_gore))
    parts.append(add_part_sphere("ZPatella_L", (-0.10, 0.50, 0.080), 0.028, "LowerLeg.L", m_bone, segs=8, rings=8))
    parts.append(add_part_cyl("ZShin_L", (-0.10, 0.28, 0.0), 0.066, 0.34, "LowerLeg.L", mat=m_pants, verts=12))
    parts.append(add_part_box("ZShoe_L", (-0.10, 0.05, 0.04), (0.105, 0.075, 0.16), "Foot.L", m_shoe))
    parts.append(add_part_box("ZToes_L", (-0.10, 0.035, 0.15), (0.085, 0.040, 0.06), "Toe.L", m_flesh))
    
    # Right Leg
    parts.append(add_part_cyl("ZThigh_R", (0.10, 0.71, 0.01), 0.076, 0.36, "UpperLeg.R", mat=m_pants, verts=12))
    parts.append(add_part_cyl("ZShin_R", (0.10, 0.28, 0.0), 0.062, 0.34, "LowerLeg.R", mat=m_flesh, verts=12))
    parts.append(add_part_box("ZTorn_Pant_R", (0.10, 0.40, 0.0), (0.155, 0.10, 0.155), "LowerLeg.R", m_pants))
    parts.append(add_part_box("ZShoe_R", (0.10, 0.05, 0.04), (0.105, 0.075, 0.16), "Foot.R", m_shoe))
    parts.append(add_part_box("ZToes_R", (0.10, 0.035, 0.15), (0.085, 0.040, 0.06), "Toe.R", m_flesh))
    
    # Join and bind to armature
    zombie_mesh = join_mesh_parts(parts, "NormalZombieMesh")
    bind_mesh_to_armature(zombie_mesh, arm_obj)
    
    # 3. Create all 11 Actions
    
    # Action 1: idle (40 frames, stooped breathing, twitching snarl)
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 20, 40]:
        t = (f / 20.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.015, -abs(math.cos(t))*0.008, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.08 + math.sin(t)*0.03, 0, math.sin(t)*0.02))
        set_key(arm_obj, "Head", f, rot_euler=(0.02, math.sin(t)*0.06, -math.cos(t)*0.03))
        set_key(arm_obj, "Jaw", f, rot_euler=(0.14 + math.sin(t)*0.06, 0, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.85 + math.sin(t)*0.05, 0, 0.15))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.18 - math.sin(t)*0.04, 0, -0.10))
    stash_action(arm_obj, act_idle)
    
    # Action 2: walk (30 frames, realistic human limping zombie gait)
    act_walk = create_action(arm_obj, "walk")
    walk_frames = [
        # (f, pelv_z_rot, pelv_x_loc, l_hip_x, l_knee_x, l_foot_x, r_hip_x, r_knee_x, r_foot_x, chest_y, l_arm_x, r_arm_x)
        (0,  -0.03, -0.02,  0.45, -0.55,  0.20, -0.35, -0.15,  0.25, -0.06,  1.10, -0.25),
        (8,   0.00,  0.00,  0.15, -0.10, -0.10, -0.10, -0.30,  0.10,  0.00,  0.95,  0.10),
        (15,  0.04,  0.02, -0.32, -0.12,  0.20,  0.40, -0.50,  0.18,  0.07,  0.80,  0.45),
        (23,  0.00,  0.00, -0.10, -0.28,  0.10,  0.12, -0.10, -0.10,  0.00,  0.95,  0.10),
        (30, -0.03, -0.02,  0.45, -0.55,  0.20, -0.35, -0.15,  0.25, -0.06,  1.10, -0.25)
    ]
    for (f, pzr, pxl, lhx, lkx, lfx, rhx, rkx, rfx, cy, lax, rax) in walk_frames:
        set_key(arm_obj, "Pelvis", f, loc=(pxl, -0.02, 0), rot_euler=(0.10, 0, pzr))
        set_key(arm_obj, "Spine", f, rot_euler=(0.06, -cy*0.5, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.14, cy, -pzr*0.5))
        set_key(arm_obj, "Head", f, rot_euler=(0.04, -cy*0.6, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(lhx, 0, 0.05))
        set_key(arm_obj, "LowerLeg.L", f, rot_euler=(lkx, 0, 0))
        set_key(arm_obj, "Foot.L", f, rot_euler=(lfx, 0, 0))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(rhx, 0, -0.05))
        set_key(arm_obj, "LowerLeg.R", f, rot_euler=(rkx, 0, 0))
        set_key(arm_obj, "Foot.R", f, rot_euler=(rfx, 0, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(lax, 0, 0.18))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(rax, 0, -0.15))
    stash_action(arm_obj, act_walk)
    
    # Action 3: fast_walk (20 frames)
    act_fwalk = create_action(arm_obj, "fast_walk")
    for f in [0, 5, 10, 15, 20]:
        t = (f / 10.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.03, -0.04, 0), rot_euler=(0.20, 0, math.sin(t)*0.06))
        set_key(arm_obj, "Chest", f, rot_euler=(0.22, -math.sin(t)*0.10, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.55, 0, 0.05))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.55, 0, -0.05))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(1.0 + math.cos(t)*0.35, 0, 0.2))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.2 - math.cos(t)*0.45, 0, -0.2))
    stash_action(arm_obj, act_fwalk)
    
    # Action 4: attack (25 frames, anticipation -> violent down-slash -> recovery)
    act_atk = create_action(arm_obj, "attack")
    # 0: Ready
    set_key(arm_obj, "Chest", 0, rot_euler=(0.10, 0, 0))
    set_key(arm_obj, "UpperArm.L", 0, rot_euler=(0.85, 0, 0.15))
    set_key(arm_obj, "UpperArm.R", 0, rot_euler=(0.20, 0, -0.15))
    # 8: Anticipation / Windup (Torso pulls back, arms raise high, jaw drops)
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.04, -0.08))
    set_key(arm_obj, "Chest", 8, rot_euler=(-0.18, 0.15, 0))
    set_key(arm_obj, "Head", 8, rot_euler=(-0.15, -0.10, 0))
    set_key(arm_obj, "Jaw", 8, rot_euler=(0.42, 0, 0))
    set_key(arm_obj, "UpperArm.L", 8, rot_euler=(1.45, 0, 0.35))
    set_key(arm_obj, "UpperArm.R", 8, rot_euler=(1.25, 0, -0.30))
    # 14: Strike Impact (Torso lunges forward, claws slash down)
    set_key(arm_obj, "Pelvis", 14, loc=(0, -0.06, 0.16))
    set_key(arm_obj, "Chest", 14, rot_euler=(0.42, -0.15, 0))
    set_key(arm_obj, "Head", 14, rot_euler=(0.25, 0.10, 0))
    set_key(arm_obj, "Jaw", 14, rot_euler=(0.08, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(0.25, 0, 0.10))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(0.35, 0, -0.10))
    # 25: Recovery back to ready
    set_key(arm_obj, "Pelvis", 25, loc=(0, 0, 0))
    set_key(arm_obj, "Chest", 25, rot_euler=(0.10, 0, 0))
    set_key(arm_obj, "Head", 25, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Jaw", 25, rot_euler=(0.14, 0, 0))
    set_key(arm_obj, "UpperArm.L", 25, rot_euler=(0.85, 0, 0.15))
    set_key(arm_obj, "UpperArm.R", 25, rot_euler=(0.20, 0, -0.15))
    stash_action(arm_obj, act_atk)
    
    # Action 5: hit_front (12 frames, chest & head knock back)
    act_hf = create_action(arm_obj, "hit_front")
    set_key(arm_obj, "Chest", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0))
    
    set_key(arm_obj, "Chest", 4, rot_euler=(-0.35, 0, 0))
    set_key(arm_obj, "Head", 4, rot_euler=(-0.45, 0, 0))
    set_key(arm_obj, "Jaw", 4, rot_euler=(0.35, 0, 0))
    set_key(arm_obj, "Pelvis", 4, loc=(0, -0.04, -0.10))
    set_key(arm_obj, "UpperArm.L", 4, rot_euler=(1.2, 0, 0.4))
    set_key(arm_obj, "UpperArm.R", 4, rot_euler=(0.8, 0, -0.4))
    
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Jaw", 12, rot_euler=(0.14, 0, 0))
    set_key(arm_obj, "Pelvis", 12, loc=(0, 0, 0))
    set_key(arm_obj, "UpperArm.L", 12, rot_euler=(0.85, 0, 0.15))
    set_key(arm_obj, "UpperArm.R", 12, rot_euler=(0.20, 0, -0.15))
    stash_action(arm_obj, act_hf)
    
    # Action 6: hit_back (12 frames)
    act_hb = create_action(arm_obj, "hit_back")
    set_key(arm_obj, "Chest", 4, rot_euler=(0.40, 0, 0))
    set_key(arm_obj, "Head", 4, rot_euler=(0.35, 0, 0))
    set_key(arm_obj, "Pelvis", 4, loc=(0, -0.03, 0.08))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 12, loc=(0, 0, 0))
    stash_action(arm_obj, act_hb)
    
    # Action 7: hit_left (12 frames)
    act_hl = create_action(arm_obj, "hit_left")
    set_key(arm_obj, "Chest", 4, rot_euler=(0, -0.20, -0.30))
    set_key(arm_obj, "Head", 4, rot_euler=(0, -0.25, -0.35))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hl)
    
    # Action 8: hit_right (12 frames)
    act_hr = create_action(arm_obj, "hit_right")
    set_key(arm_obj, "Chest", 4, rot_euler=(0, 0.20, 0.30))
    set_key(arm_obj, "Head", 4, rot_euler=(0, 0.25, 0.35))
    set_key(arm_obj, "Chest", 12, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 12, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hr)
    
    # Action 9: headshot_reaction (16 frames, violent cranial twist & snap)
    act_head = create_action(arm_obj, "headshot_reaction")
    set_key(arm_obj, "Head", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 3, rot_euler=(-0.70, 0.45, -0.20))
    set_key(arm_obj, "Jaw", 3, rot_euler=(0.55, 0, 0))
    set_key(arm_obj, "Chest", 3, rot_euler=(-0.35, 0.20, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.10, -0.18))
    set_key(arm_obj, "Head", 16, rot_euler=(-0.30, 0.20, 0))
    stash_action(arm_obj, act_head)
    
    # Action 10: stagger (30 frames, stumbles backward 2 paces)
    act_stagger = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.06, -0.22), rot_euler=(0, 0, -0.08))
    set_key(arm_obj, "Chest", 8, rot_euler=(-0.30, 0.15, 0))
    set_key(arm_obj, "UpperArm.L", 8, rot_euler=(1.1, 0, 0.5))
    set_key(arm_obj, "UpperArm.R", 8, rot_euler=(1.0, 0, -0.5))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.06, -0.40), rot_euler=(0, 0, 0.08))
    set_key(arm_obj, "Chest", 18, rot_euler=(0.15, -0.10, 0))
    set_key(arm_obj, "Pelvis", 30, loc=(0, 0, -0.40), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 30, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_stagger)
    
    # Action 11: death (36 frames, collapse to floor)
    act_death = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    # Buckle
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.25, -0.05), rot_euler=(0.20, 0, 0))
    set_key(arm_obj, "UpperLeg.L", 8, rot_euler=(0.55, 0, 0.1))
    set_key(arm_obj, "LowerLeg.L", 8, rot_euler=(-1.10, 0, 0))
    set_key(arm_obj, "UpperLeg.R", 8, rot_euler=(0.50, 0, -0.1))
    set_key(arm_obj, "LowerLeg.R", 8, rot_euler=(-1.05, 0, 0))
    # Torso pitches forward
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.55, 0.10), rot_euler=(0.75, 0, 0.15))
    set_key(arm_obj, "Chest", 18, rot_euler=(0.60, 0.20, 0))
    set_key(arm_obj, "Head", 18, rot_euler=(0.40, -0.20, 0))
    # Full collapse to ground
    set_key(arm_obj, "Pelvis", 30, loc=(0, -0.88, 0.20), rot_euler=(1.50, 0, 0.25))
    set_key(arm_obj, "Chest", 30, rot_euler=(0.25, 0.10, 0))
    set_key(arm_obj, "Head", 30, rot_euler=(-0.30, 0.35, 0))
    set_key(arm_obj, "Pelvis", 36, loc=(0, -0.88, 0.20), rot_euler=(1.50, 0, 0.25))
    stash_action(arm_obj, act_death)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_normal.glb',
        'models/zombies/zombie_normal.obj'
    )
    print("Skeletal Normal Zombie successfully built and exported!")


def build_skeletal_fast_zombie():
    print("\n--- BUILDING RIGGED ATHLETIC FAST ZOMBIE ---")
    clear_scene()
    
    m_flesh = create_mat("Mat_FastFlesh", (0.60, 0.65, 0.50, 1.0), roughness=0.55)
    m_gore = create_mat("Mat_FastGore", (0.82, 0.08, 0.05, 1.0), roughness=0.20, metallic=0.1)
    m_bone = create_mat("Mat_FastBone", (0.90, 0.88, 0.78, 1.0), roughness=0.40)
    m_top = create_mat("Mat_FastAthleticTop", (0.65, 0.15, 0.15, 1.0), roughness=0.75)
    m_shorts = create_mat("Mat_FastTrackShorts", (0.10, 0.10, 0.12, 1.0), roughness=0.80)
    m_eyes = create_mat("Mat_FastEyesGlowing", (1.0, 0.35, 0.10, 1.0), emission=(1.0, 0.35, 0.10, 1.0), emission_strength=4.0)
    m_shoe = create_mat("Mat_FastRunnerShoe", (0.20, 0.22, 0.25, 1.0), roughness=0.60)
    
    arm_obj = create_humanoid_armature("FastZombieArmature", scale_factor=0.95)
    parts = []
    
    # Head (Lean, aerodynamic skull)
    parts.append(add_part_sphere("FHead_Cranium", (0, 1.63, 0.04), 0.098, "Head", m_flesh, segs=16, rings=12))
    parts.append(add_part_box("FFace_Brow", (0, 1.635, 0.125), (0.115, 0.028, 0.038), "Head", m_flesh))
    parts.append(add_part_sphere("FEye_L", (-0.035, 1.625, 0.125), 0.016, "Head", m_eyes, segs=10, rings=8))
    parts.append(add_part_sphere("FEye_R", (0.035, 1.625, 0.125), 0.016, "Head", m_eyes, segs=10, rings=8))
    parts.append(add_part_box("FFace_Jaw", (0, 1.520, 0.095), (0.072, 0.060, 0.075), "Jaw", m_flesh, rot=(0.14, 0, 0)))
    parts.append(add_part_box("FTeeth", (0, 1.535, 0.125), (0.052, 0.014, 0.018), "Jaw", m_bone))
    parts.append(add_part_cyl("FNeck", (0, 1.46, 0.02), 0.058, 0.14, "Neck", rot=(0.18, 0, 0), mat=m_flesh, verts=12))
    
    # Torso (Lean athletic runner torso with exposed ribs)
    parts.append(add_part_box("FTorso_Main", (0, 1.28, 0.02), (0.32, 0.28, 0.18), "Chest", m_top, rot=(0.20, 0, 0)))
    parts.append(add_part_box("FRibs_Exposed", (0.08, 1.24, 0.10), (0.10, 0.12, 0.05), "Chest", m_gore))
    parts.append(add_part_box("FRib_Bones", (0.08, 1.24, 0.12), (0.08, 0.08, 0.02), "Chest", m_bone))
    parts.append(add_part_box("FTorso_Spine", (0, 1.11, 0.01), (0.28, 0.16, 0.17), "Spine", m_top))
    parts.append(add_part_box("FShorts_Pelvis", (0, 0.94, 0.0), (0.28, 0.14, 0.17), "Pelvis", m_shorts))
    
    # Arms (Clawed athletic arms)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_sphere(f"FShoulder_{s}", (sign*0.21, 1.32, 0.02), 0.065, f"Shoulder.{b_side}", m_flesh))
        parts.append(add_part_cyl(f"FArm_Upper_{s}", (sign*0.22, 1.18, 0.04), 0.048, 0.24, f"UpperArm.{b_side}", rot=(math.radians(30), 0, 0), mat=m_flesh, verts=10))
        parts.append(add_part_cyl(f"FForearm_{s}", (sign*0.22, 0.92, 0.10), 0.040, 0.24, f"Forearm.{b_side}", rot=(math.radians(40), 0, 0), mat=m_flesh, verts=10))
        parts.append(add_part_box(f"FHand_{s}", (sign*0.22, 0.77, 0.14), (0.065, 0.065, 0.035), f"Hand.{b_side}", m_flesh))
        for ci, cx in enumerate([-0.02, 0.0, 0.02]):
            parts.append(add_part_cyl(f"FClaw_{s}_{ci}", (sign*0.22 + cx, 0.72, 0.16), 0.007, 0.05, f"Hand.{b_side}", rot=(math.radians(45), 0, 0), mat=m_bone, verts=6))
            
    # Legs (Lean running legs)
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"FThigh_{s}", (sign*0.09, 0.71, 0.0), 0.068, 0.36, f"UpperLeg.{b_side}", mat=m_shorts, verts=10))
        parts.append(add_part_cyl(f"FShin_{s}", (sign*0.09, 0.28, 0.0), 0.055, 0.34, f"LowerLeg.{b_side}", mat=m_flesh, verts=10))
        parts.append(add_part_box(f"FShoe_{s}", (sign*0.09, 0.05, 0.04), (0.095, 0.065, 0.16), f"Foot.{b_side}", m_shoe))
        parts.append(add_part_box(f"FToe_{s}", (sign*0.09, 0.03, 0.14), (0.075, 0.035, 0.05), f"Toe.{b_side}", m_flesh))
        
    fast_mesh = join_mesh_parts(parts, "FastZombieMesh")
    bind_mesh_to_armature(fast_mesh, arm_obj)
    
    # Actions for Fast Zombie
    # 1. idle (twitchy crouch, 24 frames)
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 12, 24]:
        t = (f / 12.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(0, -0.05 + math.sin(t)*0.01, 0), rot_euler=(0.20, 0, 0))
        set_key(arm_obj, "Chest", f, rot_euler=(0.25 + math.sin(t)*0.04, 0, 0))
        set_key(arm_obj, "Head", f, rot_euler=(-0.10, math.sin(t)*0.12, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.85 + math.sin(t)*0.08, 0, 0.2))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.85 - math.sin(t)*0.08, 0, -0.2))
    stash_action(arm_obj, act_idle)
    
    # 2. run (16 frames, aggressive sprint)
    act_run = create_action(arm_obj, "run")
    for f in [0, 4, 8, 12, 16]:
        t = (f / 8.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.02, -0.06 - abs(math.sin(t))*0.03, 0), rot_euler=(0.40, 0, math.sin(t)*0.08))
        set_key(arm_obj, "Chest", f, rot_euler=(0.35, -math.sin(t)*0.15, 0))
        set_key(arm_obj, "Head", f, rot_euler=(-0.20, 0, 0))
        # High knee drive
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.85, 0, 0.05))
        set_key(arm_obj, "LowerLeg.L", f, rot_euler=(-abs(math.sin(t))*0.75, 0, 0))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.85, 0, -0.05))
        set_key(arm_obj, "LowerLeg.R", f, rot_euler=(-abs(math.cos(t))*0.75, 0, 0))
        # Pumping arms
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.6 - math.sin(t)*0.75, 0, 0.2))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.6 + math.sin(t)*0.75, 0, -0.2))
    stash_action(arm_obj, act_run)
    # Also add "walk" alias pointing to run for generic callers
    stash_action(arm_obj, act_run)
    
    # 3. turn (12 frames)
    act_turn = create_action(arm_obj, "turn")
    set_key(arm_obj, "Pelvis", 0, rot_euler=(0.3, 0, 0))
    set_key(arm_obj, "Pelvis", 6, rot_euler=(0.3, 0.4, -0.2))
    set_key(arm_obj, "Chest", 6, rot_euler=(0.3, 0.5, -0.25))
    set_key(arm_obj, "Pelvis", 12, rot_euler=(0.3, 0, 0))
    stash_action(arm_obj, act_turn)
    
    # 4. attack (18 frames, pounce leap)
    act_atk = create_action(arm_obj, "attack")
    set_key(arm_obj, "Pelvis", 0, loc=(0, -0.05, 0))
    set_key(arm_obj, "Pelvis", 6, loc=(0, -0.15, -0.10), rot_euler=(0.4, 0, 0))
    set_key(arm_obj, "UpperArm.L", 6, rot_euler=(1.4, 0, 0.4))
    set_key(arm_obj, "UpperArm.R", 6, rot_euler=(1.4, 0, -0.4))
    # Strike
    set_key(arm_obj, "Pelvis", 11, loc=(0, 0.05, 0.25), rot_euler=(0.5, 0, 0))
    set_key(arm_obj, "Chest", 11, rot_euler=(0.55, 0, 0))
    set_key(arm_obj, "UpperArm.L", 11, rot_euler=(0.2, 0, 0.1))
    set_key(arm_obj, "UpperArm.R", 11, rot_euler=(0.2, 0, -0.1))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.05, 0), rot_euler=(0.2, 0, 0))
    stash_action(arm_obj, act_atk)
    
    # 5. hit (10 frames)
    act_hit = create_action(arm_obj, "hit")
    set_key(arm_obj, "Chest", 3, rot_euler=(-0.30, 0, 0))
    set_key(arm_obj, "Head", 3, rot_euler=(-0.40, 0, 0))
    set_key(arm_obj, "Chest", 10, rot_euler=(0.20, 0, 0))
    set_key(arm_obj, "Head", 10, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hit)
    
    # 6. stagger (20 frames)
    act_stag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 6, loc=(0, -0.15, -0.25), rot_euler=(0.2, 0, -0.15))
    set_key(arm_obj, "Chest", 6, rot_euler=(-0.25, 0.2, 0))
    set_key(arm_obj, "Pelvis", 20, loc=(0, -0.05, -0.25), rot_euler=(0.2, 0, 0))
    stash_action(arm_obj, act_stag)
    
    # 7. death (25 frames, forward slide-collapse)
    act_death = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, -0.05, 0))
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.40, 0.15), rot_euler=(0.6, 0, 0))
    set_key(arm_obj, "Chest", 8, rot_euler=(0.7, 0, 0))
    set_key(arm_obj, "Pelvis", 18, loc=(0, -0.85, 0.45), rot_euler=(1.55, 0, 0))
    set_key(arm_obj, "Chest", 18, rot_euler=(0.1, 0, 0))
    set_key(arm_obj, "Pelvis", 25, loc=(0, -0.85, 0.50), rot_euler=(1.55, 0, 0))
    stash_action(arm_obj, act_death)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_fast.glb',
        'models/zombies/zombie_fast.obj'
    )
    print("Skeletal Fast Zombie built and exported successfully!")


def build_skeletal_heavy_zombie():
    print("\n--- BUILDING RIGGED BRUTE HEAVY ZOMBIE ---")
    clear_scene()
    
    m_flesh = create_mat("Mat_HeavyFlesh", (0.46, 0.52, 0.44, 1.0), roughness=0.68)
    m_gore = create_mat("Mat_HeavyGore", (0.70, 0.05, 0.05, 1.0), roughness=0.25, metallic=0.1)
    m_vest = create_mat("Mat_HeavyVest", (0.92, 0.70, 0.08, 1.0), roughness=0.70)
    m_stripe = create_mat("Mat_ReflectiveStripe", (0.95, 0.95, 0.95, 1.0), roughness=0.15, emission=(0.95, 0.95, 0.95, 1.0), emission_strength=1.5)
    m_pants = create_mat("Mat_HeavyWorkPants", (0.16, 0.15, 0.14, 1.0), roughness=0.85)
    m_rebar = create_mat("Mat_RebarSpike", (0.18, 0.14, 0.12, 1.0), metallic=0.85, roughness=0.45)
    m_boots = create_mat("Mat_HeavyWorkBoots", (0.08, 0.08, 0.09, 1.0), roughness=0.60)
    
    arm_obj = create_humanoid_armature("HeavyZombieArmature", scale_factor=1.2)
    parts = []
    
    # Head (Massive thick cranium and jaw)
    parts.append(add_part_sphere("HHead_Cranium", (0, 1.64, 0.02), 0.125, "Head", m_flesh, segs=18, rings=14))
    parts.append(add_part_box("HFace_Brow", (0, 1.645, 0.125), (0.145, 0.038, 0.045), "Head", m_flesh))
    parts.append(add_part_box("HFace_Jaw", (0, 1.505, 0.095), (0.105, 0.075, 0.095), "Jaw", m_flesh))
    parts.append(add_part_cyl("HNeck", (0, 1.45, 0.01), 0.092, 0.16, "Neck", mat=m_flesh, verts=14))
    
    # Torso (Massive construction brute torso with high-vis vest and rebar spike)
    parts.append(add_part_box("HTorso_Main", (0, 1.28, 0.03), (0.46, 0.34, 0.30), "Chest", m_vest))
    parts.append(add_part_box("HVest_Stripe1", (0, 1.34, 0.182), (0.42, 0.035, 0.01), "Chest", m_stripe))
    parts.append(add_part_box("HVest_Stripe2", (0, 1.22, 0.182), (0.42, 0.035, 0.01), "Chest", m_stripe))
    # Rebar spike impaled through right shoulder
    parts.append(add_part_cyl("HRebar_Spike", (0.24, 1.40, 0.05), 0.018, 0.75, "Chest", rot=(0.3, 0.2, 0.4), mat=m_rebar, verts=8))
    parts.append(add_part_box("HRebar_Wound", (0.24, 1.40, 0.05), (0.08, 0.08, 0.08), "Chest", m_gore))
    parts.append(add_part_box("HTorso_Spine", (0, 1.10, 0.02), (0.44, 0.18, 0.28), "Spine", m_vest))
    parts.append(add_part_box("HPants_Pelvis", (0, 0.94, 0.01), (0.42, 0.16, 0.26), "Pelvis", m_pants))
    
    # Heavy Arms
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_sphere(f"HShoulder_{s}", (sign*0.29, 1.34, 0.02), 0.098, f"Shoulder.{b_side}", m_vest))
        parts.append(add_part_cyl(f"HArm_Upper_{s}", (sign*0.31, 1.16, 0.04), 0.082, 0.28, f"UpperArm.{b_side}", mat=m_flesh, verts=12))
        parts.append(add_part_cyl(f"HForearm_{s}", (sign*0.31, 0.88, 0.08), 0.072, 0.28, f"Forearm.{b_side}", mat=m_flesh, verts=12))
        parts.append(add_part_box(f"HHand_{s}", (sign*0.31, 0.70, 0.12), (0.10, 0.10, 0.06), f"Hand.{b_side}", m_flesh))
        
    # Heavy Legs
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"HThigh_{s}", (sign*0.14, 0.71, 0.01), 0.105, 0.38, f"UpperLeg.{b_side}", mat=m_pants, verts=12))
        parts.append(add_part_cyl(f"HShin_{s}", (sign*0.14, 0.28, 0.0), 0.092, 0.36, f"LowerLeg.{b_side}", mat=m_pants, verts=12))
        parts.append(add_part_box(f"HBoot_{s}", (sign*0.14, 0.06, 0.05), (0.14, 0.10, 0.24), f"Foot.{b_side}", m_boots))
        parts.append(add_part_box(f"HToe_{s}", (sign*0.14, 0.04, 0.18), (0.12, 0.05, 0.06), f"Toe.{b_side}", m_boots))
        
    heavy_mesh = join_mesh_parts(parts, "HeavyZombieMesh")
    bind_mesh_to_armature(heavy_mesh, arm_obj)
    
    # Heavy Actions
    # 1. idle (45 frames, hulking menacing breathing)
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 22, 45]:
        t = (f / 22.5) * math.pi
        set_key(arm_obj, "Chest", f, rot_euler=(0.10 + math.sin(t)*0.03, 0, 0), scale=(1.0 + math.sin(t)*0.02, 1.0, 1.0))
        set_key(arm_obj, "Head", f, rot_euler=(0.05, math.sin(t)*0.04, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.3 + math.sin(t)*0.04, 0, 0.25))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.3 - math.sin(t)*0.04, 0, -0.25))
    stash_action(arm_obj, act_idle)
    
    # 2. heavy_walk (40 frames, ground-shaking stomping gait)
    act_hwalk = create_action(arm_obj, "heavy_walk")
    for f in [0, 10, 20, 30, 40]:
        t = (f / 20.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.06, -0.04, 0), rot_euler=(0.12, 0, math.sin(t)*0.06))
        set_key(arm_obj, "Chest", f, rot_euler=(0.14, -math.sin(t)*0.08, -math.sin(t)*0.04))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.45, 0, 0.10))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.45, 0, -0.10))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.4 - math.sin(t)*0.35, 0, 0.25))
        set_key(arm_obj, "UpperArm.R", f, rot_euler=(0.4 + math.sin(t)*0.35, 0, -0.25))
    stash_action(arm_obj, act_hwalk)
    # Also stash as "walk" for default walk calls
    stash_action(arm_obj, act_hwalk)
    
    # 3. heavy_attack (35 frames, devastating two-handed ground slam)
    act_hatk = create_action(arm_obj, "heavy_attack")
    # Windup overhead
    set_key(arm_obj, "Pelvis", 14, loc=(0, -0.06, -0.10), rot_euler=(-0.15, 0, 0))
    set_key(arm_obj, "Chest", 14, rot_euler=(-0.30, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(1.65, 0, 0.2))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(1.65, 0, -0.2))
    # Slam down
    set_key(arm_obj, "Pelvis", 22, loc=(0, -0.18, 0.20), rot_euler=(0.50, 0, 0))
    set_key(arm_obj, "Chest", 22, rot_euler=(0.60, 0, 0))
    set_key(arm_obj, "UpperArm.L", 22, rot_euler=(-0.20, 0, 0.1))
    set_key(arm_obj, "UpperArm.R", 22, rot_euler=(-0.20, 0, -0.1))
    # Recover
    set_key(arm_obj, "Pelvis", 35, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 35, rot_euler=(0.10, 0, 0))
    stash_action(arm_obj, act_hatk)
    # Also add "attack" alias
    stash_action(arm_obj, act_hatk)
    
    # 4. impact (20 frames, brace stance)
    act_imp = create_action(arm_obj, "impact")
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.10, 0), rot_euler=(0.25, 0, 0))
    set_key(arm_obj, "Pelvis", 20, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_imp)
    
    # 5. stagger (28 frames)
    act_hstag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 8, loc=(0, -0.08, -0.30), rot_euler=(-0.20, 0, 0))
    set_key(arm_obj, "Chest", 8, rot_euler=(-0.35, 0, 0))
    set_key(arm_obj, "Pelvis", 28, loc=(0, 0, -0.30), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hstag)
    
    # 6. death (45 frames, tree-fall backward topple)
    act_hdeath = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 16, loc=(0, -0.20, -0.25), rot_euler=(-0.45, 0, 0))
    set_key(arm_obj, "Pelvis", 34, loc=(0, -0.85, -0.75), rot_euler=(-1.55, 0, 0))
    set_key(arm_obj, "Chest", 34, rot_euler=(0.15, 0, 0))
    set_key(arm_obj, "Pelvis", 45, loc=(0, -0.85, -0.75), rot_euler=(-1.55, 0, 0))
    stash_action(arm_obj, act_hdeath)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_heavy.glb',
        'models/zombies/zombie_heavy.obj'
    )
    print("Skeletal Heavy Zombie built and exported successfully!")


def build_skeletal_boss_zombie():
    print("\n--- BUILDING RIGGED ALPHA MUTANT BOSS ZOMBIE ---")
    clear_scene()
    
    m_carapace = create_mat("Mat_BossCarapace", (0.16, 0.18, 0.15, 1.0), roughness=0.35, metallic=0.25)
    m_flesh = create_mat("Mat_BossFlesh", (0.35, 0.42, 0.32, 1.0), roughness=0.60)
    m_gore = create_mat("Mat_BossGore", (0.75, 0.05, 0.05, 1.0), roughness=0.15, metallic=0.1)
    m_veins = create_mat("Mat_BossVeinsToxic", (0.15, 0.95, 0.25, 1.0), emission=(0.15, 0.95, 0.25, 1.0), emission_strength=7.5)
    m_bone = create_mat("Mat_BossSpikeBone", (0.85, 0.82, 0.70, 1.0), roughness=0.30)
    m_blade = create_mat("Mat_BossScytheBlade", (0.12, 0.14, 0.12, 1.0), metallic=0.85, roughness=0.20)
    m_eyes = create_mat("Mat_BossQuadEyes", (1.0, 0.15, 0.05, 1.0), emission=(1.0, 0.15, 0.05, 1.0), emission_strength=5.0)
    
    arm_obj = create_humanoid_armature("BossZombieArmature", scale_factor=1.45, has_extra_scythe=True)
    parts = []
    
    # Head (Alien mutated apex predator skull with 4 glowing eyes and mandible fangs)
    parts.append(add_part_sphere("BHead_Cranium", (0, 1.68, 0.04), 0.14, "Head", m_carapace, segs=18, rings=14))
    for ey, ez in [(1.69, 0.16), (1.64, 0.15)]:
        parts.append(add_part_sphere(f"BEye_L_{ey}", (-0.05, ey, ez), 0.018, "Head", m_eyes, segs=10, rings=8))
        parts.append(add_part_sphere(f"BEye_R_{ey}", (0.05, ey, ez), 0.018, "Head", m_eyes, segs=10, rings=8))
    parts.append(add_part_box("BFangs", (0, 1.55, 0.15), (0.09, 0.06, 0.04), "Jaw", m_bone))
    parts.append(add_part_box("BFace_Jaw", (0, 1.52, 0.11), (0.12, 0.08, 0.10), "Jaw", m_carapace))
    parts.append(add_part_cyl("BNeck", (0, 1.48, 0.02), 0.105, 0.18, "Neck", mat=m_flesh, verts=14))
    
    # Torso (Heavy carapace with dorsal spikes and glowing toxic bio-luminescent vents)
    parts.append(add_part_box("BTorso_Main", (0, 1.28, 0.04), (0.52, 0.40, 0.35), "Chest", m_carapace))
    parts.append(add_part_box("BVein_Chest_1", (0, 1.34, 0.22), (0.34, 0.04, 0.015), "Chest", m_veins))
    parts.append(add_part_box("BVein_Chest_2", (0, 1.22, 0.22), (0.38, 0.04, 0.015), "Chest", m_veins))
    # Dorsal Carapace Spikes
    for sy, sz in [(1.42, -0.15), (1.30, -0.17), (1.18, -0.15)]:
        parts.append(add_part_box(f"BSpike_{sy}", (0, sy, sz), (0.05, 0.18, 0.20), "Chest", m_bone, rot=(-0.4, 0, 0)))
    parts.append(add_part_box("BTorso_Spine", (0, 1.08, 0.03), (0.48, 0.20, 0.32), "Spine", m_carapace))
    parts.append(add_part_box("BPelvis", (0, 0.94, 0.02), (0.46, 0.18, 0.30), "Pelvis", m_carapace))
    
    # Left Arm: Massive Chitinous Scythe Arm Blade
    parts.append(add_part_sphere("BShoulder_L", (-0.34, 1.36, 0.03), 0.12, "Shoulder.L", m_carapace))
    parts.append(add_part_cyl("BArm_Upper_L", (-0.36, 1.14, 0.06), 0.10, 0.32, "UpperArm.L", mat=m_carapace, verts=12))
    parts.append(add_part_cyl("BForearm_L", (-0.36, 0.82, 0.12), 0.09, 0.34, "Forearm.L", mat=m_carapace, verts=12))
    # Massive 1.2m Curved Scythe Arm Blade
    parts.append(add_part_box("BScythe_Base", (-0.36, 0.60, 0.25), (0.12, 0.16, 0.25), "ScytheBlade", m_carapace))
    parts.append(add_part_box("BScythe_BladeMain", (-0.37, 0.40, 0.60), (0.04, 0.18, 0.85), "ScytheBlade", m_blade, rot=(0.55, 0, 0)))
    parts.append(add_part_box("BScythe_EdgeGlow", (-0.37, 0.38, 0.65), (0.015, 0.04, 0.80), "ScytheBlade", m_veins, rot=(0.55, 0, 0)))
    
    # Right Arm: Heavy Crushing Claws
    parts.append(add_part_sphere("BShoulder_R", (0.34, 1.36, 0.03), 0.11, "Shoulder.R", m_carapace))
    parts.append(add_part_cyl("BArm_Upper_R", (0.36, 1.14, 0.06), 0.095, 0.32, "UpperArm.R", mat=m_carapace, verts=12))
    parts.append(add_part_cyl("BForearm_R", (0.36, 0.82, 0.12), 0.085, 0.34, "Forearm.R", mat=m_carapace, verts=12))
    parts.append(add_part_box("BHand_R", (0.36, 0.62, 0.18), (0.12, 0.12, 0.08), "Hand.R", m_carapace))
    
    # Legs: Heavy Pillar Legs
    for s, sign, b_side in [("L", -1, "L"), ("R", 1, "R")]:
        parts.append(add_part_cyl(f"BThigh_{s}", (sign*0.16, 0.71, 0.02), 0.12, 0.40, f"UpperLeg.{b_side}", mat=m_carapace, verts=12))
        parts.append(add_part_cyl(f"BShin_{s}", (sign*0.16, 0.28, 0.01), 0.105, 0.38, f"LowerLeg.{b_side}", mat=m_carapace, verts=12))
        parts.append(add_part_box(f"BFoot_{s}", (sign*0.16, 0.07, 0.08), (0.16, 0.12, 0.28), f"Foot.{b_side}", m_carapace))
        parts.append(add_part_box(f"BToe_{s}", (sign*0.16, 0.05, 0.24), (0.14, 0.07, 0.08), f"Toe.{b_side}", m_bone))
        
    boss_mesh = join_mesh_parts(parts, "BossZombieMesh")
    bind_mesh_to_armature(boss_mesh, arm_obj)
    
    # Actions for Boss
    # 1. idle (48 frames)
    act_idle = create_action(arm_obj, "idle")
    for f in [0, 24, 48]:
        t = (f / 24.0) * math.pi
        set_key(arm_obj, "Chest", f, rot_euler=(0.12 + math.sin(t)*0.04, 0, 0))
        set_key(arm_obj, "Head", f, rot_euler=(0.04, math.sin(t)*0.05, 0))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.45 + math.sin(t)*0.05, 0, 0.30))
        set_key(arm_obj, "ScytheBlade", f, rot_euler=(0.10 - math.sin(t)*0.05, 0, 0))
    stash_action(arm_obj, act_idle)
    
    # 2. walk (36 frames)
    act_walk = create_action(arm_obj, "walk")
    for f in [0, 9, 18, 27, 36]:
        t = (f / 18.0) * math.pi
        set_key(arm_obj, "Pelvis", f, loc=(math.sin(t)*0.08, -0.05, 0), rot_euler=(0.15, 0, math.sin(t)*0.06))
        set_key(arm_obj, "Chest", f, rot_euler=(0.18, -math.sin(t)*0.10, 0))
        set_key(arm_obj, "UpperLeg.L", f, rot_euler=(math.sin(t)*0.45, 0, 0.08))
        set_key(arm_obj, "UpperLeg.R", f, rot_euler=(-math.sin(t)*0.45, 0, -0.08))
        set_key(arm_obj, "UpperArm.L", f, rot_euler=(0.5 - math.sin(t)*0.3, 0, 0.3))
    stash_action(arm_obj, act_walk)
    
    # 3. attack_windup (24 frames)
    act_windup = create_action(arm_obj, "attack_windup")
    set_key(arm_obj, "Chest", 24, rot_euler=(-0.25, 0.45, 0))
    set_key(arm_obj, "UpperArm.L", 24, rot_euler=(1.45, 0.4, 0.4))
    set_key(arm_obj, "ScytheBlade", 24, rot_euler=(0.5, 0, 0))
    stash_action(arm_obj, act_windup)
    
    # 4. heavy_attack (28 frames, catastrophic 180-degree horizontal scythe cleave)
    act_cleave = create_action(arm_obj, "heavy_attack")
    set_key(arm_obj, "Chest", 0, rot_euler=(-0.25, 0.45, 0))
    set_key(arm_obj, "UpperArm.L", 0, rot_euler=(1.45, 0.4, 0.4))
    # Cleave swing
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.10, 0.30), rot_euler=(0.3, 0, -0.2))
    set_key(arm_obj, "Chest", 10, rot_euler=(0.40, -0.85, 0))
    set_key(arm_obj, "UpperArm.L", 10, rot_euler=(0.20, -0.6, 0.1))
    set_key(arm_obj, "ScytheBlade", 10, rot_euler=(-0.4, 0, 0))
    # Settle
    set_key(arm_obj, "Pelvis", 28, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 28, rot_euler=(0.12, 0, 0))
    stash_action(arm_obj, act_cleave)
    # Also add "attack" alias
    stash_action(arm_obj, act_cleave)
    
    # 5. roar (36 frames, head back, ultrasonic roar)
    act_roar = create_action(arm_obj, "roar")
    set_key(arm_obj, "Chest", 14, rot_euler=(-0.45, 0, 0))
    set_key(arm_obj, "Head", 14, rot_euler=(-0.65, 0, 0))
    set_key(arm_obj, "Jaw", 14, rot_euler=(0.75, 0, 0))
    set_key(arm_obj, "UpperArm.L", 14, rot_euler=(1.6, 0, 0.5))
    set_key(arm_obj, "UpperArm.R", 14, rot_euler=(1.6, 0, -0.5))
    set_key(arm_obj, "Chest", 36, rot_euler=(0.12, 0, 0))
    set_key(arm_obj, "Head", 36, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Jaw", 36, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_roar)
    
    # 6. hit (14 frames)
    act_bhit = create_action(arm_obj, "hit")
    set_key(arm_obj, "Chest", 4, rot_euler=(-0.15, 0, 0))
    set_key(arm_obj, "Chest", 14, rot_euler=(0.12, 0, 0))
    stash_action(arm_obj, act_bhit)
    
    # 7. stagger (32 frames)
    act_bstag = create_action(arm_obj, "stagger")
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.15, -0.45), rot_euler=(-0.25, 0, 0))
    set_key(arm_obj, "Chest", 10, rot_euler=(-0.35, 0, 0))
    set_key(arm_obj, "Pelvis", 32, loc=(0, 0, -0.45), rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_bstag)
    
    # 8. death (50 frames, meltdown collapse)
    act_bdeath = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0))
    set_key(arm_obj, "Pelvis", 16, loc=(0, -0.45, -0.1), rot_euler=(0.35, 0, 0))
    set_key(arm_obj, "UpperLeg.L", 16, rot_euler=(0.8, 0, 0))
    set_key(arm_obj, "LowerLeg.L", 16, rot_euler=(-1.3, 0, 0))
    set_key(arm_obj, "Pelvis", 36, loc=(0, -1.05, 0.40), rot_euler=(1.50, 0, 0))
    set_key(arm_obj, "ScytheBlade", 36, rot_euler=(-0.5, 0, 0))
    set_key(arm_obj, "Pelvis", 50, loc=(0, -1.05, 0.40), rot_euler=(1.50, 0, 0))
    stash_action(arm_obj, act_bdeath)
    
    export_rigged_glb_and_obj(
        'assets/3d/zombies/zombie_boss.glb',
        'models/zombies/zombie_boss.obj'
    )
    print("Skeletal Boss Zombie built and exported successfully!")

if __name__ == '__main__':
    print("=== STARTING FULL SKELETAL ZOMBIE GENERATION ===")
    build_skeletal_normal_zombie()
    build_skeletal_fast_zombie()
    build_skeletal_heavy_zombie()
    build_skeletal_boss_zombie()
    print("=== COMPLETED ALL 4 SKELETAL ZOMBIE GENERATIONS ===")
