import bpy
import math
import os

def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Ensure all existing objects, meshes, materials, armatures are removed
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh, do_unlink=True)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat, do_unlink=True)
    for arm in list(bpy.data.armatures):
        bpy.data.armatures.remove(arm, do_unlink=True)
    for act in list(bpy.data.actions):
        bpy.data.actions.remove(act, do_unlink=True)

def create_pbr_material(name, base_color=(0.5, 0.5, 0.5, 1.0), metallic=0.0, roughness=0.5, emission=None, emission_strength=1.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = base_color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        if emission:
            # In Blender 4.0, Emission Color is 'Emission Color'
            if 'Emission Color' in bsdf.inputs:
                bsdf.inputs['Emission Color'].default_value = emission
            elif 'Emission' in bsdf.inputs:
                bsdf.inputs['Emission'].default_value = emission
            if 'Emission Strength' in bsdf.inputs:
                bsdf.inputs['Emission Strength'].default_value = emission_strength
    return mat

def add_box(name, location, size, material=None):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    return obj

def add_cylinder(name, location, radius, depth, rotation=(0,0,0), material=None, vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def add_cone(name, location, radius1, depth, rotation=(0,0,0), material=None, vertices=12):
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, depth=depth, location=location, rotation=rotation, vertices=vertices)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def add_uv_sphere(name, location, radius, material=None, segments=16, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=segments, ring_count=rings)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    return obj

def join_objects(obj_list, final_name):
    if not obj_list:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in obj_list:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obj_list[0]
    bpy.ops.object.join()
    final_obj = bpy.context.active_object
    final_obj.name = final_name
    return final_obj

def export_glb(filepath, blend_backup_path=None):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if blend_backup_path:
        os.makedirs(os.path.dirname(blend_backup_path), exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=blend_backup_path)
        print(f"Saved Blend file: {blend_backup_path}")
        
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_yup=True,
        export_materials='EXPORT',
        export_animations=True
    )
    print(f"Successfully exported GLB: {filepath} ({os.path.getsize(filepath)} bytes)")

def export_obj(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.ops.wm.obj_export(filepath=filepath, export_materials=True, export_selected_objects=False)
    print(f"Successfully exported OBJ: {filepath} ({os.path.getsize(filepath)} bytes)")
