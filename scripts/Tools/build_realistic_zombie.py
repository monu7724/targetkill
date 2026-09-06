import bpy
import mathutils
import numpy as np
import os

print("=== STARTING REALISTIC ZOMBIE MODEL BUILD ===")

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Texture Generation with NumPy
# Load original 2048 textures
src_face_png = os.path.abspath('assets/external/vitruvian/vit_face_bc.png')
src_body_png = os.path.abspath('assets/external/vitruvian/vit_body_bc.png')

def make_zombie_texture(src_path, out_path, desat_factor=0.6, greenish_tint=(0.92, 1.05, 0.95), darken=0.9):
    img = bpy.data.images.load(src_path)
    # Downscale to 1024x1024 for mobile
    img.scale(1024, 1024)
    w, h = img.size
    pixels = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(pixels)
    
    # Reshape to (N, 4)
    rgba = pixels.reshape((-1, 4))
    r = rgba[:, 0]
    g = rgba[:, 1]
    b = rgba[:, 2]
    
    # Compute luminance
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    
    # Desaturate towards sickly pale tone
    r_pale = lum * (1 - desat_factor) + r * desat_factor
    g_pale = lum * (1 - desat_factor) + g * desat_factor
    b_pale = lum * (1 - desat_factor) + b * desat_factor
    
    # Apply subtle viral tint & slight pallor
    rgba[:, 0] = np.clip(r_pale * greenish_tint[0] * darken, 0.0, 1.0)
    rgba[:, 1] = np.clip(g_pale * greenish_tint[1] * darken, 0.0, 1.0)
    rgba[:, 2] = np.clip(b_pale * greenish_tint[2] * darken, 0.0, 1.0)
    
    img.pixels.foreach_set(rgba.flatten())
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f"[OK] Generated zombie texture: {out_path} ({w}x{h})")
    bpy.data.images.remove(img)

out_face = os.path.abspath('assets/external/vitruvian/zombie_face_bc.png')
out_body = os.path.abspath('assets/external/vitruvian/zombie_body_bc.png')
make_zombie_texture(src_face_png, out_face, desat_factor=0.45, greenish_tint=(0.90, 1.02, 0.94), darken=0.88)
make_zombie_texture(src_body_png, out_body, desat_factor=0.45, greenish_tint=(0.90, 1.02, 0.94), darken=0.88)

# Generate Worn Security Uniform textures (Shirt & Pants)
def make_uniform_texture(out_path, base_color=(0.14, 0.18, 0.25), dirt_noise=True):
    img = bpy.data.images.new("UniformTex", width=1024, height=1024)
    rgba = np.zeros((1024, 1024, 4), dtype=np.float32)
    rgba[:, :, 0] = base_color[0]
    rgba[:, :, 1] = base_color[1]
    rgba[:, :, 2] = base_color[2]
    rgba[:, :, 3] = 1.0
    
    # Add procedural fabric weave & dirt noise
    np.random.seed(42)
    noise = np.random.normal(0.0, 0.035, (1024, 1024, 1)).astype(np.float32)
    # Add dirt / grime patches
    grime_x = np.linspace(0, 4*np.pi, 1024)
    grime_y = np.linspace(0, 4*np.pi, 1024)
    gx, gy = np.meshgrid(grime_x, grime_y)
    grime = (np.sin(gx) * np.cos(gy) * 0.05).astype(np.float32)[:, :, np.newaxis]
    
    rgba[:, :, :3] = np.clip(rgba[:, :, :3] + noise + grime, 0.0, 1.0)
    
    img.pixels.foreach_set(rgba.flatten())
    img.filepath_raw = out_path
    img.file_format = 'PNG'
    img.save()
    print(f"[OK] Generated uniform texture: {out_path}")
    bpy.data.images.remove(img)

out_shirt = os.path.abspath('assets/external/vitruvian/zombie_shirt_bc.png')
out_pants = os.path.abspath('assets/external/vitruvian/zombie_pants_bc.png')
# Worn airport security shirt: desaturated tactical slate-blue
make_uniform_texture(out_shirt, base_color=(0.15, 0.19, 0.26))
# Dark charcoal security pants
make_uniform_texture(out_pants, base_color=(0.10, 0.11, 0.13))

# 2. Import Armature & Body with 9 Actions
body_glb = 'assets/external/animations/vitruvian_full_rigged.glb'
bpy.ops.import_scene.gltf(filepath=body_glb)

# Clean unwanted primitive objects
for o in list(bpy.data.objects):
    if any(o.name.startswith(p) for p in ['Cube', 'Icosphere', 'Camera', 'Light']):
        bpy.data.objects.remove(o, do_unlink=True)

arm = [o for o in bpy.data.objects if o.type == 'ARMATURE'][0]
print("[OK] Armature loaded:", arm.name, "Bones:", len(arm.data.bones))

# 3. Import Head Meshes
head_glb = 'assets/external/vitruvian/vitruvian_head.glb'
bpy.ops.import_scene.gltf(filepath=head_glb)

# Clean unwanted objects from head import
for o in list(bpy.data.objects):
    if any(o.name.startswith(p) for p in ['Cube', 'Icosphere', 'Camera', 'Light']):
        bpy.data.objects.remove(o, do_unlink=True)

head_meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.parent != arm]
print("[OK] Head meshes loaded:", [o.name for o in head_meshes])

# Apply transforms to head meshes so local vertices match world coords
bpy.ops.object.select_all(action='DESELECT')
for hm in head_meshes:
    hm.select_set(True)
bpy.context.view_layer.objects.active = head_meshes[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# 4. Proportional Head Scaling (-15%) & Neck Alignment
# Neck base pivot
pivot = mathutils.Vector((0.0, 0.035, 1.485))
scale_factor = 0.85 # 15% smaller

for hm in head_meshes:
    for v in hm.data.vertices:
        # Scale relative to neck pivot
        v.co = pivot + (v.co - pivot) * scale_factor
        # Slight Z settlement to seal neck collar
        v.co.z -= 0.015
    hm.data.update()

# 5. Bind Head Meshes to Armature via Armature Modifier & Vertex Groups
for hm in head_meshes:
    hm.parent = arm
    # Ensure vertex groups exist
    vg_head = hm.vertex_groups.get('mixamorig:Head') or hm.vertex_groups.new(name='mixamorig:Head')
    vg_neck = hm.vertex_groups.get('mixamorig:Neck') or hm.vertex_groups.new(name='mixamorig:Neck')
    
    # Assign weights
    all_indices = [v.index for v in hm.data.vertices]
    vg_head.add(all_indices, 1.0, 'REPLACE')
    
    # For neck boundary vertices on head mesh (Z < 1.50), blend with neck bone
    neck_seam_indices = [v.index for v in hm.data.vertices if v.co.z < 1.505]
    if neck_seam_indices:
        vg_neck.add(neck_seam_indices, 0.5, 'REPLACE')
        vg_head.add(neck_seam_indices, 0.5, 'REPLACE')
        print(f"  Blended {len(neck_seam_indices)} neck seam vertices for {hm.name}")
    
    # Add armature modifier
    mod = hm.modifiers.new(name='Armature', type='ARMATURE')
    mod.object = arm

# 6. Setup PBR Materials & Shaders
def create_pbr_material(name, diffuse_path, rough_path=None, normal_path=None, metallic=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    bsdf.inputs['Metallic'].default_value = metallic
    
    if os.path.exists(diffuse_path):
        tex_d = nodes.new('ShaderNodeTexImage')
        tex_d.image = bpy.data.images.load(diffuse_path)
        links.new(tex_d.outputs['Color'], bsdf.inputs['Base Color'])
    
    if rough_path and os.path.exists(rough_path):
        tex_r = nodes.new('ShaderNodeTexImage')
        tex_r.image = bpy.data.images.load(rough_path)
        links.new(tex_r.outputs['Color'], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = 0.8
        
    if normal_path and os.path.exists(normal_path):
        tex_n = nodes.new('ShaderNodeTexImage')
        tex_n.image = bpy.data.images.load(normal_path)
        tex_n.image.colorspace_settings.name = 'Non-Color'
        norm_map = nodes.new('ShaderNodeNormalMap')
        links.new(tex_n.outputs['Color'], norm_map.inputs['Color'])
        links.new(norm_map.outputs['Normal'], bsdf.inputs['Normal'])
        
    return mat

mat_skin_body = create_pbr_material(
    'Zombie_BodySkin_PBR',
    out_body,
    os.path.abspath('assets/external/vitruvian/vit_body_rough.png'),
    os.path.abspath('assets/external/vitruvian/vit_body_n.png')
)

mat_skin_face = create_pbr_material(
    'Zombie_FaceSkin_PBR',
    out_face,
    os.path.abspath('assets/external/vitruvian/vit_face_rough.png'),
    os.path.abspath('assets/external/vitruvian/vit_face_n.png')
)

mat_shirt = create_pbr_material(
    'Zombie_Shirt_PBR',
    out_shirt,
    normal_path=os.path.abspath('assets/external/vitruvian/vit_fabric_n.png')
)

mat_pants = create_pbr_material(
    'Zombie_Pants_PBR',
    out_pants,
    normal_path=os.path.abspath('assets/external/vitruvian/vit_fabric_n.png')
)

# Assign materials to meshes
body_mesh = bpy.data.objects.get('cm_vitruvian')
if body_mesh:
    body_mesh.data.materials.clear()
    body_mesh.data.materials.append(mat_skin_body)

shirt_mesh = bpy.data.objects.get('Shirt')
if shirt_mesh:
    shirt_mesh.data.materials.clear()
    shirt_mesh.data.materials.append(mat_shirt)

pants_mesh = bpy.data.objects.get('Pants')
if pants_mesh:
    pants_mesh.data.materials.clear()
    pants_mesh.data.materials.append(mat_pants)

for hm in head_meshes:
    if 'cm_vitruvian' in hm.name:
        hm.data.materials.clear()
        hm.data.materials.append(mat_skin_face)

# 7. Export the production-ready realistic infected zombie
final_glb = 'assets/external/vitruvian/zombie_realistic_human.glb'
bpy.ops.export_scene.gltf(
    filepath=final_glb,
    export_format='GLB',
    export_animations=True,
    export_skins=True,
    export_morph=False
)
print("=== EXPORT SUCCESS ===")
print("Exported:", final_glb, "Size:", os.path.getsize(final_glb), "bytes")
