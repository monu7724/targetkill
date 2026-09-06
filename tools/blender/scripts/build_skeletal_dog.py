"""
Sector Zero: Lockdown - Skeletal Infected Dog Asset Pipeline
Generates 18-bone quadruped armature, detailed canine mesh with PBR materials,
and full action library (run, attack, hit_head, hit_body, death, idle, walk).
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

def add_part_cyl(name, loc, r, d, bone_name, rot=(0,0,0), mat=None, verts=12, smooth=True):
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

def add_part_cone(name, loc, r1, d, bone_name, rot=(0,0,0), mat=None, verts=8, smooth=True):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, depth=d, location=loc, rotation=rot, vertices=verts)
    obj = bpy.context.active_object
    obj.name = name
    if smooth:
        for p in obj.data.polygons: p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    vg = obj.vertex_groups.new(name=bone_name)
    vg.add(range(len(obj.data.vertices)), 1.0, 'REPLACE')
    return obj

def add_part_sphere(name, loc, r, bone_name, mat=None, segs=14, rings=10, smooth=True):
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

def create_dog_armature(arm_name="DogArmature"):
    arm_data = bpy.data.armatures.new(f"{arm_name}Data")
    arm_obj = bpy.data.objects.new(arm_name, arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm_data.edit_bones
    
    def nb(name, head, tail, parent_name=None):
        b = eb.new(name)
        b.head = head
        b.tail = tail
        if parent_name and parent_name in eb:
            b.parent = eb[parent_name]
        return b
        
    # Exactly 18 bones:
    # 6 Axial bones
    nb("Root", (0, 0, 0), (0, 0.1, 0))
    nb("Pelvis", (0, 0.45, 0.35), (0, 0.48, 0.10), "Root")
    nb("Spine", (0, 0.48, 0.10), (0, 0.50, -0.15), "Pelvis")
    nb("Chest", (0, 0.50, -0.15), (0, 0.56, -0.32), "Spine")
    nb("Neck", (0, 0.56, -0.32), (0, 0.65, -0.46), "Chest")
    nb("Head", (0, 0.65, -0.46), (0, 0.68, -0.68), "Neck")
    
    # 6 Front Leg bones
    nb("UpperLeg.FL", (-0.14, 0.48, -0.18), (-0.14, 0.26, -0.16), "Chest")
    nb("LowerLeg.FL", (-0.14, 0.26, -0.16), (-0.14, 0.08, -0.18), "UpperLeg.FL")
    nb("Paw.FL", (-0.14, 0.08, -0.18), (-0.14, 0.0, -0.25), "LowerLeg.FL")
    
    nb("UpperLeg.FR", (0.14, 0.48, -0.18), (0.14, 0.26, -0.16), "Chest")
    nb("LowerLeg.FR", (0.14, 0.26, -0.16), (0.14, 0.08, -0.18), "UpperLeg.FR")
    nb("Paw.FR", (0.14, 0.08, -0.18), (0.14, 0.0, -0.25), "LowerLeg.FR")
    
    # 6 Back Leg bones
    nb("UpperLeg.BL", (-0.14, 0.45, 0.32), (-0.14, 0.25, 0.38), "Pelvis")
    nb("LowerLeg.BL", (-0.14, 0.25, 0.38), (-0.14, 0.08, 0.32), "UpperLeg.BL")
    nb("Paw.BL", (-0.14, 0.08, 0.32), (-0.14, 0.0, 0.25), "LowerLeg.BL")
    
    nb("UpperLeg.BR", (0.14, 0.45, 0.32), (0.14, 0.25, 0.38), "Pelvis")
    nb("LowerLeg.BR", (0.14, 0.25, 0.38), (0.14, 0.08, 0.32), "UpperLeg.BR")
    nb("Paw.BR", (0.14, 0.08, 0.32), (0.14, 0.0, 0.25), "LowerLeg.BR")
    
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
    return act

def stash_action(arm_obj, act):
    track = arm_obj.animation_data.nla_tracks.new()
    track.name = act.name
    start_f = int(act.frame_range[0])
    track.strips.new(act.name, start_f, act)

def export_rigged_glb(glb_path):
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

def build_infected_dog():
    print("\n--- BUILDING RIGGED SKELETAL INFECTED DOG ---")
    clear_scene()
    
    # Materials
    m_fur = create_mat("Mat_DogFur", (0.16, 0.14, 0.13, 1.0), roughness=0.85)
    m_flesh = create_mat("Mat_DogFlesh", (0.58, 0.16, 0.14, 1.0), roughness=0.45)
    m_eyes = create_mat("Mat_DogEyes", (0.85, 0.95, 0.15, 1.0), emission=(0.7, 0.9, 0.1, 1.0), emission_strength=2.0)
    m_teeth = create_mat("Mat_DogTeeth", (0.85, 0.82, 0.72, 1.0), roughness=0.3)
    
    parts = []
    
    # Pelvis / Hindquarters
    parts.append(add_part_box("DogPelvis", (0, 0.45, 0.28), (0.26, 0.22, 0.26), "Pelvis", mat=m_fur))
    
    # Mid-Spine
    parts.append(add_part_box("DogSpine", (0, 0.48, 0.05), (0.24, 0.22, 0.28), "Spine", mat=m_fur))
    
    # Chest / Ribcage
    parts.append(add_part_box("DogChest", (0, 0.50, -0.18), (0.30, 0.32, 0.32), "Chest", mat=m_fur))
    # Exposed rib lesion (wound)
    parts.append(add_part_box("DogLesion", (0.15, 0.50, -0.15), (0.04, 0.18, 0.16), "Chest", mat=m_flesh))
    
    # Neck
    parts.append(add_part_cyl("DogNeck", (0, 0.58, -0.36), 0.11, 0.22, "Neck", rot=(math.radians(35), 0, 0), mat=m_fur))
    
    # Head / Cranium
    parts.append(add_part_box("DogCranium", (0, 0.65, -0.50), (0.22, 0.18, 0.20), "Head", mat=m_fur))
    # Snout
    parts.append(add_part_box("DogSnout", (0, 0.61, -0.62), (0.14, 0.12, 0.18), "Head", mat=m_flesh))
    # Lower Jaw
    parts.append(add_part_box("DogJaw", (0, 0.54, -0.60), (0.12, 0.06, 0.16), "Head", mat=m_flesh))
    
    # Fangs (Upper & Lower)
    parts.append(add_part_cone("FangUL", (-0.05, 0.56, -0.65), 0.016, 0.045, "Head", rot=(math.radians(180), 0, 0), mat=m_teeth))
    parts.append(add_part_cone("FangUR", (0.05, 0.56, -0.65), 0.016, 0.045, "Head", rot=(math.radians(180), 0, 0), mat=m_teeth))
    parts.append(add_part_cone("FangLL", (-0.04, 0.57, -0.63), 0.015, 0.04, "Head", mat=m_teeth))
    parts.append(add_part_cone("FangLR", (0.04, 0.57, -0.63), 0.015, 0.04, "Head", mat=m_teeth))
    
    # Ears
    parts.append(add_part_cone("EarL", (-0.10, 0.74, -0.48), 0.045, 0.12, "Head", rot=(math.radians(-25), 0, math.radians(-30)), mat=m_fur))
    parts.append(add_part_cone("EarR", (0.10, 0.74, -0.48), 0.045, 0.12, "Head", rot=(math.radians(-25), 0, math.radians(30)), mat=m_fur))
    
    # Infected Glowing Eyes
    parts.append(add_part_sphere("EyeL", (-0.09, 0.66, -0.56), 0.026, "Head", mat=m_eyes))
    parts.append(add_part_sphere("EyeR", (0.09, 0.66, -0.56), 0.026, "Head", mat=m_eyes))
    
    # Front Left Leg
    parts.append(add_part_cyl("UpperLeg_FL", (-0.15, 0.38, -0.17), 0.065, 0.22, "UpperLeg.FL", mat=m_fur))
    parts.append(add_part_cyl("LowerLeg_FL", (-0.15, 0.17, -0.17), 0.048, 0.20, "LowerLeg.FL", mat=m_fur))
    parts.append(add_part_box("Paw_FL", (-0.15, 0.04, -0.21), (0.09, 0.07, 0.12), "Paw.FL", mat=m_flesh))
    
    # Front Right Leg
    parts.append(add_part_cyl("UpperLeg_FR", (0.15, 0.38, -0.17), 0.065, 0.22, "UpperLeg.FR", mat=m_fur))
    parts.append(add_part_cyl("LowerLeg_FR", (0.15, 0.17, -0.17), 0.048, 0.20, "LowerLeg.FR", mat=m_fur))
    parts.append(add_part_box("Paw_FR", (0.15, 0.04, -0.21), (0.09, 0.07, 0.12), "Paw.FR", mat=m_flesh))
    
    # Rear Left Leg
    parts.append(add_part_cyl("UpperLeg_BL", (-0.15, 0.36, 0.34), 0.075, 0.22, "UpperLeg.BL", rot=(math.radians(18), 0, 0), mat=m_fur))
    parts.append(add_part_cyl("LowerLeg_BL", (-0.15, 0.17, 0.34), 0.052, 0.20, "LowerLeg.BL", rot=(math.radians(-15), 0, 0), mat=m_fur))
    parts.append(add_part_box("Paw_BL", (-0.15, 0.04, 0.28), (0.09, 0.07, 0.12), "Paw.BL", mat=m_flesh))
    
    # Rear Right Leg
    parts.append(add_part_cyl("UpperLeg_BR", (0.15, 0.36, 0.34), 0.075, 0.22, "UpperLeg.BR", rot=(math.radians(18), 0, 0), mat=m_fur))
    parts.append(add_part_cyl("LowerLeg_BR", (0.15, 0.17, 0.34), 0.052, 0.20, "LowerLeg.BR", rot=(math.radians(-15), 0, 0), mat=m_fur))
    parts.append(add_part_box("Paw_BR", (0.15, 0.04, 0.28), (0.09, 0.07, 0.12), "Paw.BR", mat=m_flesh))
    
    mesh_obj = join_mesh_parts(parts, "InfectedDogMesh")
    arm_obj = create_dog_armature("DogArmature")
    bind_mesh_to_armature(mesh_obj, arm_obj)
    
    # Verify 18 bones
    b_count = len(arm_obj.data.bones)
    print(f"Dog Armature Bone Count: {b_count}")
    assert b_count == 18, f"Expected 18 bones, got {b_count}"
    
    # ANIMATIONS
    
    # 1. idle (30 frames)
    act_idle = create_action(arm_obj, "idle")
    set_key(arm_obj, "Chest", 0, rot_euler=(0, 0, 0), scale=(1, 1, 1))
    set_key(arm_obj, "Chest", 15, rot_euler=(-0.04, 0, 0), scale=(1.04, 1.04, 1.02))
    set_key(arm_obj, "Chest", 30, rot_euler=(0, 0, 0), scale=(1, 1, 1))
    set_key(arm_obj, "Head", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 15, rot_euler=(0.06, 0.08, 0))
    set_key(arm_obj, "Head", 30, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_idle)
    
    # 2. walk (24 frames)
    act_walk = create_action(arm_obj, "walk")
    for f, rfl, rfr, rbl, rbr, py in [
        (0, -0.3, 0.3, 0.3, -0.3, 0.0),
        (6, 0.0, 0.0, 0.0, 0.0, 0.02),
        (12, 0.3, -0.3, -0.3, 0.3, 0.0),
        (18, 0.0, 0.0, 0.0, 0.0, 0.02),
        (24, -0.3, 0.3, 0.3, -0.3, 0.0),
    ]:
        set_key(arm_obj, "UpperLeg.FL", f, rot_euler=(rfl, 0, 0))
        set_key(arm_obj, "UpperLeg.FR", f, rot_euler=(rfr, 0, 0))
        set_key(arm_obj, "UpperLeg.BL", f, rot_euler=(rbl, 0, 0))
        set_key(arm_obj, "UpperLeg.BR", f, rot_euler=(rbr, 0, 0))
        set_key(arm_obj, "Pelvis", f, loc=(0, py, 0))
    stash_action(arm_obj, act_walk)
    
    # 3. run (20 frames, rapid quadruped bounding gallop)
    act_run = create_action(arm_obj, "run")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0.04, 0), rot_euler=(-0.15, 0, 0))
    set_key(arm_obj, "UpperLeg.FL", 0, rot_euler=(-0.65, 0, 0))
    set_key(arm_obj, "UpperLeg.FR", 0, rot_euler=(-0.55, 0, 0))
    set_key(arm_obj, "UpperLeg.BL", 0, rot_euler=(0.60, 0, 0))
    set_key(arm_obj, "UpperLeg.BR", 0, rot_euler=(0.50, 0, 0))
    
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.06, 0), rot_euler=(0.18, 0, 0))
    set_key(arm_obj, "UpperLeg.FL", 10, rot_euler=(0.60, 0, 0))
    set_key(arm_obj, "UpperLeg.FR", 10, rot_euler=(0.50, 0, 0))
    set_key(arm_obj, "UpperLeg.BL", 10, rot_euler=(-0.60, 0, 0))
    set_key(arm_obj, "UpperLeg.BR", 10, rot_euler=(-0.50, 0, 0))
    
    set_key(arm_obj, "Pelvis", 20, loc=(0, 0.04, 0), rot_euler=(-0.15, 0, 0))
    set_key(arm_obj, "UpperLeg.FL", 20, rot_euler=(-0.65, 0, 0))
    set_key(arm_obj, "UpperLeg.FR", 20, rot_euler=(-0.55, 0, 0))
    set_key(arm_obj, "UpperLeg.BL", 20, rot_euler=(0.60, 0, 0))
    set_key(arm_obj, "UpperLeg.BR", 20, rot_euler=(0.50, 0, 0))
    stash_action(arm_obj, act_run)
    
    # 4. attack (18 frames, vicious lunging bite snap)
    act_atk = create_action(arm_obj, "attack")
    # Windup
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0.1), rot_euler=(0.1, 0, 0))
    set_key(arm_obj, "Chest", 0, rot_euler=(-0.1, 0, 0))
    # Strike / Snap
    set_key(arm_obj, "Pelvis", 8, loc=(0, 0.08, -0.25), rot_euler=(-0.25, 0, 0))
    set_key(arm_obj, "Chest", 8, rot_euler=(0.35, 0, 0))
    set_key(arm_obj, "Neck", 8, rot_euler=(-0.45, 0, 0))
    set_key(arm_obj, "Head", 8, rot_euler=(0.50, 0, 0))
    set_key(arm_obj, "UpperLeg.FL", 8, rot_euler=(-0.7, 0, -0.2))
    set_key(arm_obj, "UpperLeg.FR", 8, rot_euler=(-0.7, 0, 0.2))
    # Settle
    set_key(arm_obj, "Pelvis", 18, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 18, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Neck", 18, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 18, rot_euler=(0, 0, 0))
    set_key(arm_obj, "UpperLeg.FL", 18, rot_euler=(0, 0, 0))
    set_key(arm_obj, "UpperLeg.FR", 18, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_atk)
    
    # 5. hit_head (14 frames, cranial headshot recoil)
    act_hit_head = create_action(arm_obj, "hit_head")
    set_key(arm_obj, "Neck", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 0, rot_euler=(0, 0, 0))
    # Recoil back & up
    set_key(arm_obj, "Neck", 4, rot_euler=(-0.45, 0.2, 0))
    set_key(arm_obj, "Head", 4, rot_euler=(-0.70, 0.35, 0))
    set_key(arm_obj, "Chest", 4, rot_euler=(-0.15, 0, 0))
    # Recovery
    set_key(arm_obj, "Neck", 14, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Head", 14, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Chest", 14, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hit_head)
    
    # 6. hit_body (16 frames, torso flinch)
    act_hit_body = create_action(arm_obj, "hit_body")
    set_key(arm_obj, "Chest", 0, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Spine", 0, rot_euler=(0, 0, 0))
    # Flinch
    set_key(arm_obj, "Chest", 5, rot_euler=(0.10, 0.40, 0.25))
    set_key(arm_obj, "Spine", 5, rot_euler=(0.0, 0.25, 0.15))
    # Recovery
    set_key(arm_obj, "Chest", 16, rot_euler=(0, 0, 0))
    set_key(arm_obj, "Spine", 16, rot_euler=(0, 0, 0))
    stash_action(arm_obj, act_hit_body)
    
    # 7. death (32 frames, legs give way, roll & collapse)
    act_death = create_action(arm_obj, "death")
    set_key(arm_obj, "Pelvis", 0, loc=(0, 0, 0), rot_euler=(0, 0, 0))
    # Collapse
    set_key(arm_obj, "Pelvis", 10, loc=(0, -0.22, 0), rot_euler=(0.2, 0, 0.5))
    set_key(arm_obj, "UpperLeg.FL", 10, rot_euler=(0.3, 0, 0.8))
    set_key(arm_obj, "UpperLeg.FR", 10, rot_euler=(0.3, 0, -0.8))
    # Flat on ground
    set_key(arm_obj, "Pelvis", 24, loc=(0, -0.42, 0), rot_euler=(0, 0, 1.55))
    set_key(arm_obj, "Head", 24, rot_euler=(-0.3, 0, 0))
    set_key(arm_obj, "Pelvis", 32, loc=(0, -0.42, 0), rot_euler=(0, 0, 1.55))
    stash_action(arm_obj, act_death)
    
    # Export
    export_rigged_glb('assets/3d/zombies/infected_dog.glb')
    print("Skeletal Infected Dog built and exported successfully!")

if __name__ == '__main__':
    build_infected_dog()
