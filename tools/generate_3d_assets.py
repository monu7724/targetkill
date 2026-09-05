import math
import os

class ObjBuilder:
    def __init__(self):
        self.vertices = []
        self.uvs = []
        self.normals = []
        self.faces = []

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices)

    def add_uv(self, u, v):
        self.uvs.append((u, v))
        return len(self.uvs)

    def add_normal(self, nx, ny, nz):
        l = math.sqrt(nx*nx + ny*ny + nz*nz)
        if l > 0.0001:
            nx, ny, nz = nx/l, ny/l, nz/l
        self.normals.append((nx, ny, nz))
        return len(self.normals)

    def add_face(self, v_idx_list, uv_idx_list, norm_idx):
        # 1-indexed for OBJ
        face_verts = []
        for i in range(len(v_idx_list)):
            v = v_idx_list[i]
            u = uv_idx_list[i] if i < len(uv_idx_list) else 1
            n = norm_idx
            face_verts.append(f"{v}/{u}/{n}")
        self.faces.append(face_verts)

    def add_quad(self, p1, p2, p3, p4, uv_box=(0, 0, 1, 1)):
        # Computes normal automatically
        v1 = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
        v2 = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
        nx = v1[1]*v2[2] - v1[2]*v2[1]
        ny = v1[2]*v2[0] - v1[0]*v2[2]
        nz = v1[0]*v2[1] - v1[1]*v2[0]
        n_idx = self.add_normal(nx, ny, nz)

        u0, v0, u1, v1_ = uv_box
        uv1 = self.add_uv(u0, v0)
        uv2 = self.add_uv(u1, v0)
        uv3 = self.add_uv(u1, v1_)
        uv4 = self.add_uv(u0, v1_)

        idx1 = self.add_vertex(*p1)
        idx2 = self.add_vertex(*p2)
        idx3 = self.add_vertex(*p3)
        idx4 = self.add_vertex(*p4)

        self.add_face([idx1, idx2, idx3], [uv1, uv2, uv3], n_idx)
        self.add_face([idx1, idx3, idx4], [uv1, uv3, uv4], n_idx)

    def add_box(self, center, size, uv_scale=(1.0, 1.0)):
        cx, cy, cz = center
        sx, sy, sz = size[0]/2.0, size[1]/2.0, size[2]/2.0

        # 8 corners
        c = [
            (cx - sx, cy - sy, cz - sz), # 0
            (cx + sx, cy - sy, cz - sz), # 1
            (cx + sx, cy + sy, cz - sz), # 2
            (cx - sx, cy + sy, cz - sz), # 3
            (cx - sx, cy - sy, cz + sz), # 4
            (cx + sx, cy - sy, cz + sz), # 5
            (cx + sx, cy + sy, cz + sz), # 6
            (cx - sx, cy + sy, cz + sz), # 7
        ]
        # Front (+Z)
        self.add_quad(c[4], c[5], c[6], c[7], (0, 0, uv_scale[0], uv_scale[1]))
        # Back (-Z)
        self.add_quad(c[1], c[0], c[3], c[2], (0, 0, uv_scale[0], uv_scale[1]))
        # Top (+Y)
        self.add_quad(c[3], c[2], c[6], c[7], (0, 0, uv_scale[0], uv_scale[1]))
        # Bottom (-Y)
        self.add_quad(c[0], c[1], c[5], c[4], (0, 0, uv_scale[0], uv_scale[1]))
        # Right (+X)
        self.add_quad(c[5], c[1], c[2], c[6], (0, 0, uv_scale[0], uv_scale[1]))
        # Left (-X)
        self.add_quad(c[0], c[4], c[7], c[3], (0, 0, uv_scale[0], uv_scale[1]))

    def add_cylinder(self, center, radius, height, segments=12, axis='y'):
        cx, cy, cz = center
        h2 = height / 2.0
        ring1 = []
        ring2 = []
        norm_side = []
        
        for i in range(segments):
            angle = (i / segments) * 2.0 * math.pi
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            
            if axis == 'y':
                p1 = (cx + radius * cos_a, cy - h2, cz + radius * sin_a)
                p2 = (cx + radius * cos_a, cy + h2, cz + radius * sin_a)
                n = (cos_a, 0, sin_a)
            elif axis == 'z':
                p1 = (cx + radius * cos_a, cy + radius * sin_a, cz - h2)
                p2 = (cx + radius * cos_a, cy + radius * sin_a, cz + h2)
                n = (cos_a, sin_a, 0)
            else: # x
                p1 = (cx - h2, cy + radius * cos_a, cz + radius * sin_a)
                p2 = (cx + h2, cy + radius * cos_a, cz + radius * sin_a)
                n = (0, cos_a, sin_a)
                
            ring1.append(self.add_vertex(*p1))
            ring2.append(self.add_vertex(*p2))
            norm_side.append(self.add_normal(*n))

        # Side quads
        for i in range(segments):
            next_i = (i + 1) % segments
            u0 = i / segments
            u1 = (i + 1) / segments
            uv1 = self.add_uv(u0, 0)
            uv2 = self.add_uv(u1, 0)
            uv3 = self.add_uv(u1, 1)
            uv4 = self.add_uv(u0, 1)

            self.add_face([ring1[i], ring1[next_i], ring2[next_i]], [uv1, uv2, uv3], norm_side[i])
            self.add_face([ring1[i], ring2[next_i], ring2[i]], [uv1, uv3, uv4], norm_side[i])

    def save(self, filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(f"# Sector Zero: Lockdown 3D Asset\n")
            for v in self.vertices:
                f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for vt in self.uvs:
                f.write(f"vt {vt[0]:.4f} {vt[1]:.4f}\n")
            for vn in self.normals:
                f.write(f"vn {vn[0]:.4f} {vn[1]:.4f} {vn[2]:.4f}\n")
            for face in self.faces:
                f.write(f"f {' '.join(face)}\n")
        print(f"Saved: {filepath} ({len(self.vertices)} verts, {len(self.faces)} faces)")

# ==========================================
# 1. WEAPON MODELS
# ==========================================

def build_pistol():
    # USP-45 Tactical
    b = ObjBuilder()
    # Slide (Steel)
    b.add_box((0, 0.02, -0.05), (0.032, 0.038, 0.20))
    # Slide serrations (rear)
    b.add_box((0.017, 0.02, 0.01), (0.003, 0.03, 0.05))
    b.add_box((-0.017, 0.02, 0.01), (0.003, 0.03, 0.05))
    # Barrel
    b.add_cylinder((0, 0.02, -0.16), 0.008, 0.04, axis='z')
    # Polymer Frame & Grip
    b.add_box((0, -0.05, 0.01), (0.030, 0.11, 0.048))
    # Trigger guard & Trigger
    b.add_box((0, -0.025, -0.04), (0.012, 0.032, 0.045))
    b.add_box((0, -0.022, -0.035), (0.006, 0.02, 0.01))
    # Tactical iron sights
    b.add_box((0, 0.042, -0.13), (0.006, 0.01, 0.015)) # Front sight
    b.add_box((0, 0.042, 0.03), (0.012, 0.01, 0.012))  # Rear sight notch
    # Mag base plate
    b.add_box((0, -0.108, 0.015), (0.034, 0.012, 0.054))
    b.save('models/weapons/pistol.obj')

def build_rifle():
    # M4A1 Sentinel Assault Rifle
    b = ObjBuilder()
    # Upper Receiver
    b.add_box((0, 0.03, -0.05), (0.04, 0.055, 0.22))
    # Lower Receiver & Magwell
    b.add_box((0, -0.03, -0.06), (0.038, 0.06, 0.16))
    # Quad-rail Handguard
    b.add_box((0, 0.025, -0.28), (0.042, 0.045, 0.24))
    # Barrel
    b.add_cylinder((0, 0.025, -0.46), 0.010, 0.14, axis='z')
    # Flash Hider
    b.add_cylinder((0, 0.025, -0.54), 0.013, 0.035, axis='z')
    # Curved 30-round STANAG Magazine
    b.add_box((0, -0.12, -0.10), (0.026, 0.14, 0.065))
    # Pistol Grip
    b.add_box((0, -0.08, 0.02), (0.032, 0.10, 0.048))
    # Buffer Tube & Tactical Stock
    b.add_cylinder((0, 0.02, 0.14), 0.016, 0.16, axis='z')
    b.add_box((0, 0.02, 0.23), (0.038, 0.11, 0.10))
    # Picatinny Top Rail & Reflex Holo Sight
    b.add_box((0, 0.062, -0.12), (0.024, 0.012, 0.32)) # Top rail
    b.add_box((0, 0.085, -0.08), (0.032, 0.035, 0.065)) # Sight body
    b.add_box((0, 0.09, -0.08), (0.024, 0.025, 0.05))  # Sight glass frame
    b.save('models/weapons/rifle.obj')

def build_shotgun():
    # Remington 870 Tactical Shotgun
    b = ObjBuilder()
    # Receiver
    b.add_box((0, 0.01, -0.08), (0.042, 0.065, 0.26))
    # Heavy 12ga Barrel
    b.add_cylinder((0, 0.03, -0.44), 0.013, 0.48, axis='z')
    # Magazine Tube
    b.add_cylinder((0, 0.005, -0.38), 0.012, 0.38, axis='z')
    # Tactical Grooved Pump Forend
    b.add_cylinder((0, 0.005, -0.32), 0.022, 0.18, axis='z')
    # Trigger Guard
    b.add_box((0, -0.035, -0.02), (0.014, 0.035, 0.06))
    # Full Ergonomic Stock
    b.add_box((0, -0.04, 0.15), (0.038, 0.08, 0.20))
    b.add_box((0, -0.05, 0.26), (0.042, 0.12, 0.04)) # Recoil pad
    b.save('models/weapons/shotgun.obj')

def build_fps_arms():
    # First-Person Tactical Arms & Gloved Hands
    b = ObjBuilder()
    # Right Forearm (SWAT tactical sleeve)
    b.add_cylinder((0.18, -0.22, 0.20), 0.045, 0.30, axis='z')
    # Right Gloved Hand holding grip
    b.add_box((0.14, -0.12, 0.06), (0.05, 0.07, 0.08))
    # Fingers wrapped around grip
    b.add_cylinder((0.12, -0.11, 0.06), 0.014, 0.06, axis='x')
    b.add_cylinder((0.12, -0.14, 0.06), 0.013, 0.06, axis='x')
    
    # Left Forearm supporting forward
    b.add_cylinder((-0.14, -0.24, 0.12), 0.042, 0.28, axis='z')
    # Left Gloved Hand cradling forend
    b.add_box((-0.06, -0.14, -0.10), (0.06, 0.05, 0.08))
    b.add_cylinder((-0.03, -0.13, -0.10), 0.014, 0.05, axis='z')
    b.save('models/player/fps_arms.obj')

# ==========================================
# 2. PLAYER FULL BODY MODEL
# ==========================================

def build_player_soldier():
    b = ObjBuilder()
    # Tactical Helmet & Head
    b.add_box((0, 1.72, 0), (0.22, 0.23, 0.23)) # Helmet
    b.add_box((0, 1.74, 0.11), (0.16, 0.06, 0.05)) # Goggles
    b.add_box((0, 1.62, 0.03), (0.18, 0.10, 0.18)) # Balaclava face
    # Torso & Plate Carrier (Tactical Vest)
    b.add_box((0, 1.34, 0), (0.38, 0.44, 0.24)) # Torso
    b.add_box((0, 1.36, 0.05), (0.34, 0.38, 0.18)) # Armor plate
    b.add_box((0, 1.25, 0.14), (0.28, 0.12, 0.06)) # Mag pouches
    b.add_box((-0.18, 1.40, 0.06), (0.06, 0.12, 0.06)) # Radio
    # Tactical Belt & Holster
    b.add_box((0, 1.08, 0), (0.36, 0.08, 0.22))
    b.add_box((0.20, 0.98, 0), (0.08, 0.15, 0.08)) # Holster
    # Left Arm
    b.add_cylinder((-0.26, 1.40, 0), 0.07, 0.26, axis='y') # Shoulder/Upper arm
    b.add_cylinder((-0.26, 1.15, 0.04), 0.055, 0.24, axis='y') # Forearm
    b.add_box((-0.26, 0.98, 0.06), (0.07, 0.09, 0.07)) # Gloved hand
    # Right Arm
    b.add_cylinder((0.26, 1.40, 0), 0.07, 0.26, axis='y') # Shoulder/Upper arm
    b.add_cylinder((0.26, 1.15, 0.04), 0.055, 0.24, axis='y') # Forearm
    b.add_box((0.26, 0.98, 0.06), (0.07, 0.09, 0.07)) # Gloved hand
    # Legs (Combat pants)
    b.add_cylinder((-0.12, 0.80, 0), 0.09, 0.45, axis='y') # Left Thigh
    b.add_cylinder((0.12, 0.80, 0), 0.09, 0.45, axis='y')  # Right Thigh
    b.add_box((-0.12, 0.58, 0.09), (0.10, 0.10, 0.04))    # Left Knee pad
    b.add_box((0.12, 0.58, 0.09), (0.10, 0.10, 0.04))     # Right Knee pad
    b.add_cylinder((-0.12, 0.35, 0), 0.075, 0.40, axis='y') # Left Shin
    b.add_cylinder((0.12, 0.35, 0), 0.075, 0.40, axis='y')  # Right Shin
    # Combat Boots
    b.add_box((-0.12, 0.09, 0.03), (0.12, 0.16, 0.26))
    b.add_box((0.12, 0.09, 0.03), (0.12, 0.16, 0.26))
    b.save('models/player/player_soldier.obj')

# ==========================================
# 3. REALISTIC ZOMBIE MODELS
# ==========================================

def build_zombie_normal():
    # Regular Decayed Zombie
    b = ObjBuilder()
    # Deformed head with gaping mouth and eye sockets
    b.add_box((0, 1.62, 0.04), (0.20, 0.22, 0.20)) # Cranium
    b.add_box((0, 1.54, 0.13), (0.14, 0.07, 0.08)) # Gaping jaw
    # Torso (Torn dirty clothing exposing ribs)
    b.add_box((0, 1.25, 0), (0.34, 0.45, 0.20))
    b.add_box((0.08, 1.28, 0.10), (0.14, 0.18, 0.03)) # Exposed chest wound
    # Shambling Arms
    b.add_cylinder((-0.22, 1.30, 0.12), 0.055, 0.30, axis='z') # Left arm reaching
    b.add_cylinder((-0.22, 1.28, 0.34), 0.045, 0.26, axis='z') # Left forearm
    b.add_box((-0.22, 1.28, 0.48), (0.06, 0.07, 0.09))       # Clawed hand
    
    b.add_cylinder((0.22, 1.25, 0.08), 0.055, 0.28, axis='z')  # Right arm reaching
    b.add_cylinder((0.22, 1.22, 0.28), 0.045, 0.24, axis='z')
    b.add_box((0.22, 1.22, 0.41), (0.06, 0.07, 0.09))
    # Pelvis & Torn Trousers
    b.add_box((0, 0.95, 0), (0.30, 0.16, 0.18))
    # Legs
    b.add_cylinder((-0.10, 0.68, 0), 0.075, 0.42, axis='y')
    b.add_cylinder((0.10, 0.68, 0), 0.075, 0.42, axis='y')
    b.add_cylinder((-0.10, 0.28, 0), 0.065, 0.42, axis='y')
    b.add_cylinder((0.10, 0.28, 0), 0.065, 0.42, axis='y')
    # Tattered shoes
    b.add_box((-0.10, 0.06, 0.02), (0.10, 0.10, 0.22))
    b.add_box((0.10, 0.06, 0.02), (0.10, 0.10, 0.22))
    b.save('models/zombies/zombie_normal.obj')

def build_zombie_fast():
    # Lean, hunched predatory sprinter zombie
    b = ObjBuilder()
    # Snarling feral head, thrust forward
    b.add_box((0, 1.48, 0.18), (0.18, 0.20, 0.18))
    b.add_box((0, 1.40, 0.26), (0.12, 0.08, 0.10)) # Snarl jaw
    # Hunched spine & Torso
    b.add_box((0, 1.18, 0.06), (0.28, 0.42, 0.18))
    b.add_box((0, 1.30, -0.04), (0.16, 0.18, 0.08)) # Hunched spine hump
    # Elongated feral arms with sharp bone fingers
    b.add_cylinder((-0.19, 1.10, 0.22), 0.045, 0.35, axis='z')
    b.add_cylinder((-0.19, 0.95, 0.45), 0.038, 0.30, axis='z')
    b.add_box((-0.19, 0.95, 0.62), (0.05, 0.05, 0.12)) # Sharp claws
    
    b.add_cylinder((0.19, 1.10, 0.22), 0.045, 0.35, axis='z')
    b.add_cylinder((0.19, 0.95, 0.45), 0.038, 0.30, axis='z')
    b.add_box((0.19, 0.95, 0.62), (0.05, 0.05, 0.12))
    # Agile crouched legs
    b.add_cylinder((-0.11, 0.65, -0.04), 0.065, 0.44, axis='y')
    b.add_cylinder((0.11, 0.65, -0.04), 0.065, 0.44, axis='y')
    b.add_cylinder((-0.11, 0.24, 0.05), 0.055, 0.40, axis='y')
    b.add_cylinder((0.11, 0.24, 0.05), 0.055, 0.40, axis='y')
    b.add_box((-0.11, 0.05, 0.08), (0.09, 0.08, 0.22))
    b.add_box((0.11, 0.05, 0.08), (0.09, 0.08, 0.22))
    b.save('models/zombies/zombie_fast.obj')

def build_zombie_heavy():
    # Hulking armored brute with riot gear and bloated muscle
    b = ObjBuilder()
    # Brutal head with neck collar
    b.add_box((0, 1.76, 0.04), (0.25, 0.26, 0.24))
    b.add_box((0, 1.70, 0), (0.34, 0.12, 0.28)) # Reinforced collar
    # Colossal armored chest with cracked riot vest
    b.add_box((0, 1.38, 0), (0.54, 0.52, 0.34))
    b.add_box((0, 1.40, 0.18), (0.46, 0.40, 0.08)) # Dented ceramic chest plate
    # Massive arms
    b.add_cylinder((-0.34, 1.42, 0), 0.11, 0.32, axis='y')
    b.add_cylinder((-0.34, 1.10, 0.10), 0.095, 0.34, axis='z')
    b.add_box((-0.34, 1.10, 0.30), (0.14, 0.14, 0.14)) # Huge fist
    
    b.add_cylinder((0.34, 1.42, 0), 0.11, 0.32, axis='y')
    b.add_cylinder((0.34, 1.10, 0.10), 0.095, 0.34, axis='z')
    b.add_box((0.34, 1.10, 0.30), (0.14, 0.14, 0.14))
    # Thick heavy legs
    b.add_cylinder((-0.16, 0.75, 0), 0.13, 0.46, axis='y')
    b.add_cylinder((0.16, 0.75, 0), 0.13, 0.46, axis='y')
    b.add_cylinder((-0.16, 0.30, 0), 0.11, 0.44, axis='y')
    b.add_cylinder((0.16, 0.30, 0), 0.11, 0.44, axis='y')
    # Heavy riot boots
    b.add_box((-0.16, 0.09, 0.04), (0.16, 0.18, 0.30))
    b.add_box((0.16, 0.09, 0.04), (0.16, 0.18, 0.30))
    b.save('models/zombies/zombie_heavy.obj')

def build_zombie_boss():
    # The Alpha Mutant Behemoth (2.4m tall)
    b = ObjBuilder()
    # Mutated Monstrous Head with horn protrusions
    b.add_box((0, 2.30, 0.08), (0.34, 0.35, 0.32))
    b.add_cone = lambda c, r, h: b.add_cylinder(c, r, h, 8, 'y') # simplify horn
    b.add_cone((-0.14, 2.50, 0.12), 0.06, 0.16) # Left bone horn
    b.add_cone((0.14, 2.50, 0.12), 0.06, 0.16)  # Right bone horn
    # Giant mutated muscular torso & bone carapace
    b.add_box((0, 1.80, 0), (0.75, 0.68, 0.48))
    b.add_box((0, 1.85, 0.24), (0.60, 0.50, 0.12)) # Chest bone carapace
    b.add_box((0, 1.95, -0.22), (0.45, 0.40, 0.14)) # Back spines
    # Colossal mutated right arm with jagged spikes
    b.add_cylinder((0.48, 1.85, 0.08), 0.16, 0.45, axis='y') # Mutation shoulder
    b.add_cylinder((0.52, 1.45, 0.20), 0.14, 0.50, axis='z') # Massive forearm
    b.add_box((0.52, 1.45, 0.52), (0.24, 0.24, 0.24))       # Giant crusher fist
    b.add_box((0.52, 1.62, 0.25), (0.06, 0.18, 0.06))       # Elbow bone spike
    
    # Left Arm (Strong but normal proportioned mutant arm)
    b.add_cylinder((-0.45, 1.85, 0), 0.12, 0.40, axis='y')
    b.add_cylinder((-0.45, 1.45, 0.15), 0.10, 0.42, axis='z')
    b.add_box((-0.45, 1.45, 0.40), (0.16, 0.16, 0.18))
    # Massive Stomping Legs
    b.add_cylinder((-0.24, 1.00, 0), 0.18, 0.60, axis='y')
    b.add_cylinder((0.24, 1.00, 0), 0.18, 0.60, axis='y')
    b.add_cylinder((-0.24, 0.40, 0), 0.15, 0.58, axis='y')
    b.add_cylinder((0.24, 0.40, 0), 0.15, 0.58, axis='y')
    b.add_box((-0.24, 0.10, 0.06), (0.22, 0.20, 0.38))
    b.add_box((0.24, 0.10, 0.06), (0.22, 0.20, 0.38))
    b.save('models/zombies/zombie_boss.obj')

# ==========================================
# 4. REALISTIC ENVIRONMENT MODELS
# ==========================================

def build_airport_props():
    # Check-in Counter
    b = ObjBuilder()
    b.add_box((0, 0.6, 0), (2.4, 1.2, 0.8)) # Main desk
    b.add_box((0, 1.22, -0.2), (2.4, 0.06, 0.45)) # Counter top
    b.add_box((-0.6, 1.45, -0.15), (0.45, 0.35, 0.08)) # Monitor 1
    b.add_box((0.6, 1.45, -0.15), (0.45, 0.35, 0.08))  # Monitor 2
    b.add_box((0, 0.15, 0.45), (1.8, 0.25, 0.8))       # Baggage belt
    b.save('models/environment/airport/checkin_counter.obj')

    # Airport Seats (Row of 3)
    b = ObjBuilder()
    b.add_box((0, 0.4, 0), (1.8, 0.06, 0.08)) # Support beam
    b.add_box((-0.7, 0.2, 0), (0.06, 0.4, 0.4)) # Left leg
    b.add_box((0.7, 0.2, 0), (0.06, 0.4, 0.4))  # Right leg
    for x in [-0.55, 0.0, 0.55]:
        b.add_box((x, 0.45, 0), (0.48, 0.06, 0.45)) # Seat base
        b.add_box((x, 0.72, -0.20), (0.48, 0.50, 0.06)) # Seat back
    b.save('models/environment/airport/airport_seats.obj')

    # Luggage Trolley with Suitcases
    b = ObjBuilder()
    b.add_box((0, 0.15, 0), (0.7, 0.06, 1.1)) # Base platform
    b.add_cylinder((-0.3, 0.10, -0.45), 0.08, 0.04, axis='x') # Wheels
    b.add_cylinder((0.3, 0.10, -0.45), 0.08, 0.04, axis='x')
    b.add_cylinder((-0.3, 0.10, 0.45), 0.08, 0.04, axis='x')
    b.add_cylinder((0.3, 0.10, 0.45), 0.08, 0.04, axis='x')
    b.add_box((0, 0.60, 0.52), (0.65, 0.90, 0.05)) # Handle bar
    # Suitcases stacked
    b.add_box((0, 0.32, -0.1), (0.55, 0.25, 0.75)) # Big case
    b.add_box((0.02, 0.54, -0.05), (0.48, 0.20, 0.60)) # Medium case
    b.save('models/environment/airport/luggage_trolley.obj')

    # Terminal Pillar with Emergency Light
    b = ObjBuilder()
    b.add_box((0, 3.5, 0), (0.8, 7.0, 0.8)) # Large structural pillar
    b.add_box((0, 6.8, 0), (1.2, 0.4, 1.2)) # Capital top
    b.add_box((0, 0.2, 0), (1.2, 0.4, 1.2)) # Plinth base
    b.add_box((0, 3.2, 0.45), (0.25, 0.35, 0.12)) # Emergency light box
    b.save('models/environment/airport/terminal_pillar.obj')

def build_station_props():
    # Metro Railway Tracks (Pair of steel rails on sleepers)
    b = ObjBuilder()
    for z in range(-5, 6):
        b.add_box((0, 0.04, z * 0.8), (1.8, 0.08, 0.22)) # Sleepers (ties)
    # Left & Right Steel Rails
    b.add_box((-0.65, 0.12, 0), (0.08, 0.10, 8.8))
    b.add_box((0.65, 0.12, 0), (0.08, 0.10, 8.8))
    b.save('models/environment/station/train_tracks.obj')

    # Station Platform Section
    b = ObjBuilder()
    b.add_box((0, 0.5, 0), (3.5, 1.0, 6.0)) # Platform body
    b.add_box((1.65, 1.01, 0), (0.3, 0.02, 6.0)) # Tactile warning yellow edge
    b.save('models/environment/station/station_platform.obj')

    # Subway Station Bench
    b = ObjBuilder()
    b.add_box((0, 0.45, 0), (1.8, 0.06, 0.45))
    b.add_box((0, 0.72, -0.20), (1.8, 0.50, 0.06))
    b.add_box((-0.7, 0.22, 0), (0.08, 0.44, 0.40))
    b.add_box((0.7, 0.22, 0), (0.08, 0.44, 0.40))
    b.save('models/environment/station/station_bench.obj')

def build_train_props():
    # Metro Passenger Train Carriage (Segment)
    b = ObjBuilder()
    # Floor
    b.add_box((0, 0.6, 0), (2.8, 0.2, 8.0))
    # Outer Left & Right Walls with window cutouts
    b.add_box((-1.4, 2.0, -2.5), (0.1, 2.6, 2.5))
    b.add_box((-1.4, 2.0, 2.5), (0.1, 2.6, 2.5))
    b.add_box((-1.4, 2.8, 0), (0.1, 1.0, 2.5)) # Above door
    b.add_box((-1.4, 1.0, 0), (0.1, 0.6, 2.5)) # Below door
    
    b.add_box((1.4, 2.0, -2.5), (0.1, 2.6, 2.5))
    b.add_box((1.4, 2.0, 2.5), (0.1, 2.6, 2.5))
    b.add_box((1.4, 2.8, 0), (0.1, 1.0, 2.5))
    b.add_box((1.4, 1.0, 0), (0.1, 0.6, 2.5))
    # Roof Curved Arch
    b.add_box((0, 3.3, 0), (2.8, 0.15, 8.0))
    # Interior Seats
    b.add_box((-1.0, 1.0, -2.2), (0.5, 0.45, 1.8))
    b.add_box((1.0, 1.0, -2.2), (0.5, 0.45, 1.8))
    b.add_box((-1.0, 1.0, 2.2), (0.5, 0.45, 1.8))
    b.add_box((1.0, 1.0, 2.2), (0.5, 0.45, 1.8))
    # Overhead Handrails
    b.add_cylinder((-0.6, 2.7, 0), 0.02, 7.5, axis='z')
    b.add_cylinder((0.6, 2.7, 0), 0.02, 7.5, axis='z')
    b.save('models/environment/train/train_carriage.obj')

def build_industrial_props():
    # Dumpster
    b = ObjBuilder()
    b.add_box((0, 0.7, 0), (1.8, 1.2, 1.2)) # Main bin
    b.add_box((0, 1.35, -0.3), (1.85, 0.1, 0.65)) # Slanted lid back
    b.add_box((0, 1.32, 0.3), (1.85, 0.08, 0.65))  # Slanted lid front
    b.add_box((-0.95, 0.8, 0), (0.1, 0.15, 0.3))   # Side forklift pocket
    b.add_box((0.95, 0.8, 0), (0.1, 0.15, 0.3))
    b.save('models/environment/industrial/dumpster.obj')

    # Street Lamp Post
    b = ObjBuilder()
    b.add_cylinder((0, 2.5, 0), 0.07, 5.0, axis='y') # Vertical pole
    b.add_cylinder((0.4, 5.0, 0), 0.05, 0.9, axis='x') # Arm
    b.add_box((0.85, 4.95, 0), (0.35, 0.12, 0.22))     # Lamp housing
    b.save('models/environment/industrial/street_lamp.obj')

if __name__ == '__main__':
    build_pistol()
    build_rifle()
    build_shotgun()
    build_fps_arms()
    build_player_soldier()
    build_zombie_normal()
    build_zombie_fast()
    build_zombie_heavy()
    build_zombie_boss()
    build_airport_props()
    build_station_props()
    build_train_props()
    build_industrial_props()
    print("All 3D models generated successfully!")
