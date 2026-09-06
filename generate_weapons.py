import os

weapons = {
    "m4a1": {"length": 0.8, "height": 0.2, "width": 0.05, "color": "0.2 0.2 0.2"},
    "ak47": {"length": 0.85, "height": 0.22, "width": 0.06, "color": "0.4 0.2 0.1"},
    "scar_l": {"length": 0.82, "height": 0.25, "width": 0.07, "color": "0.7 0.6 0.4"},
    "g36": {"length": 0.78, "height": 0.24, "width": 0.06, "color": "0.15 0.15 0.15"},
    "famas": {"length": 0.75, "height": 0.26, "width": 0.05, "color": "0.25 0.25 0.25"},
    "aug": {"length": 0.79, "height": 0.23, "width": 0.05, "color": "0.3 0.3 0.2"},
    "mp5": {"length": 0.6, "height": 0.2, "width": 0.05, "color": "0.1 0.1 0.1"},
    "spas12": {"length": 0.9, "height": 0.18, "width": 0.06, "color": "0.2 0.2 0.2"},
    "svd": {"length": 1.1, "height": 0.18, "width": 0.04, "color": "0.4 0.15 0.1"},
    "m249": {"length": 1.0, "height": 0.3, "width": 0.1, "color": "0.3 0.3 0.2"}
}

out_dir = "/workspaces/targetkill/models/weapons"
os.makedirs(out_dir, exist_ok=True)

def write_cube(f, l, h, w):
    # A simple cube centered at z=0, y=0, stretching from z=0 to z=-l
    # Actually, let's just make it a basic block that Godot can read
    verts = [
        [-w/2, -h/2, 0], [w/2, -h/2, 0], [w/2, h/2, 0], [-w/2, h/2, 0],
        [-w/2, -h/2, -l], [w/2, -h/2, -l], [w/2, h/2, -l], [-w/2, h/2, -l]
    ]
    for v in verts:
        f.write(f"v {v[0]} {v[1]} {v[2]}\n")
    
    faces = [
        [1, 2, 3, 4], # back
        [5, 8, 7, 6], # front
        [1, 5, 6, 2], # bottom
        [2, 6, 7, 3], # right
        [3, 7, 8, 4], # top
        [4, 8, 5, 1]  # left
    ]
    for face in faces:
        f.write(f"f {face[0]} {face[1]} {face[2]} {face[3]}\n")

for name, specs in weapons.items():
    obj_path = os.path.join(out_dir, f"{name}.obj")
    mtl_path = os.path.join(out_dir, f"{name}.mtl")
    
    with open(mtl_path, "w") as f:
        f.write(f"newmtl mat_{name}\n")
        f.write(f"Kd {specs['color']}\n")
        
    with open(obj_path, "w") as f:
        f.write(f"mtllib {name}.mtl\n")
        f.write(f"usemtl mat_{name}\n")
        write_cube(f, specs['length'], specs['height'], specs['width'])

print("Generated 10 weapon models")
