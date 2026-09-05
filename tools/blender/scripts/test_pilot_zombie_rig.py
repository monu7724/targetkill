import bpy
import bmesh
import math
import os

print("--- BUILDING PILOT RIGGED ZOMBIE NORMAL ---")
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Materials
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

m_flesh = create_mat("Mat_ZombieFlesh", (0.52, 0.62, 0.48, 1.0), roughness=0.62)
m_gore = create_mat("Mat_ZombieGore", (0.78, 0.06, 0.05, 1.0), roughness=0.22, metallic=0.12)
m_bone = create_mat("Mat_ZombieBone", (0.88, 0.85, 0.74, 1.0), roughness=0.45)
m_shirt = create_mat("Mat_ZombieTornShirt", (0.38, 0.40, 0.42, 1.0), roughness=0.88)
m_pants = create_mat("Mat_ZombieTornPants", (0.14, 0.16, 0.20, 1.0), roughness=0.85)
m_eye_blood = create_mat("Mat_ZombieEyeBlood", (0.95, 0.15, 0.10, 1.0), emission=(0.95, 0.15, 0.10, 1.0), emission_strength=3.2)
m_eye_milky = create_mat("Mat_ZombieEyeMilky", (0.72, 0.76, 0.72, 1.0), roughness=0.35)
m_hair = create_mat("Mat_ZombieHair", (0.10, 0.09, 0.08, 1.0), roughness=0.90)
m_shoe = create_mat("Mat_ZombieShoe", (0.08, 0.07, 0.07, 1.0), roughness=0.75)

# 2. Armature
arm_data = bpy.data.armatures.new("ZombieArmatureData")
arm_obj = bpy.data.objects.new("ZombieArmature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj

bpy.ops.object.mode_set(mode='EDIT')
eb = arm_data.edit_bones

def make_bone(name, head, tail, parent=None):
    b = eb.new(name)
    b.head = head
    b.tail = tail
    if parent:
        b.parent = eb[parent]
    return b

make_bone("Root", (0, 0, 0), (0, 0.1, 0))
make_bone("Pelvis", (0, 0.92, 0), (0, 1.02, 0), "Root")
make_bone("Spine", (0, 1.02, 0), (0, 1.20, 0), "Pelvis")
make_bone("Chest", (0, 1.20, 0), (0, 1.44, 0), "Spine")
make_bone("Neck", (0, 1.44, 0), (0, 1.55, 0.02), "Chest")
make_bone("Head", (0, 1.55, 0.02), (0, 1.75, 0.04), "Neck")
make_bone("Jaw", (0, 1.52, 0.07), (0, 1.48, 0.11), "Head")

# Left Arm
make_bone("Shoulder.L", (-0.08, 1.38, 0), (-0.22, 1.33, 0.02), "Chest")
make_bone("UpperArm.L", (-0.22, 1.33, 0.02), (-0.26, 1.05, 0.06), "Shoulder.L")
make_bone("Forearm.L", (-0.26, 1.05, 0.06), (-0.26, 0.78, 0.14), "UpperArm.L")
make_bone("Hand.L", (-0.26, 0.78, 0.14), (-0.26, 0.62, 0.20), "Forearm.L")

# Right Arm
make_bone("Shoulder.R", (0.08, 1.38, 0), (0.22, 1.33, 0.02), "Chest")
make_bone("UpperArm.R", (0.22, 1.33, 0.02), (0.26, 1.05, 0.06), "Shoulder.R")
make_bone("Forearm.R", (0.26, 1.05, 0.06), (0.26, 0.78, 0.14), "UpperArm.R")
make_bone("Hand.R", (0.26, 0.78, 0.14), (0.26, 0.62, 0.20), "Forearm.R")

# Legs
make_bone("UpperLeg.L", (-0.11, 0.90, 0), (-0.11, 0.50, 0.02), "Pelvis")
make_bone("LowerLeg.L", (-0.11, 0.50, 0.02), (-0.11, 0.10, 0.0), "UpperLeg.L")
make_bone("Foot.L", (-0.11, 0.10, 0.0), (-0.11, 0.03, 0.14), "LowerLeg.L")
make_bone("Toe.L", (-0.11, 0.03, 0.14), (-0.11, 0.01, 0.22), "Foot.L")

make_bone("UpperLeg.R", (0.11, 0.90, 0), (0.11, 0.50, 0.02), "Pelvis")
make_bone("LowerLeg.R", (0.11, 0.50, 0.02), (0.11, 0.10, 0.0), "UpperLeg.R")
make_bone("Foot.R", (0.11, 0.10, 0.0), (0.11, 0.03, 0.14), "LowerLeg.R")
make_bone("Toe.R", (0.11, 0.03, 0.14), (0.11, 0.01, 0.22), "Foot.R")

bpy.ops.object.mode_set(mode='OBJECT')

print(f"Armature created with {len(arm_data.bones)} bones.")
