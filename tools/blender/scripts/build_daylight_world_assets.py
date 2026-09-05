"""
Sector Zero: Lockdown - Master Daylight Realistic 3D World Pipeline
Generates bright daytime environments with AAA/GTA-style presentation:
- Mission 1: Daylight Airport Terminal (Exterior drop-off road, bus, cars, facade + interior concourse, skylights, tarmac)
- Mission 2: Daylight Railway Station (Platform, tracks, overhead catenary, canopy, signage)
- Mission 3: Daylight Train Yard (Full carriage, outdoor rails, ballast, crates, utility poles)
- Mission 4: Daylight Industrial District (Asphalt road, sidewalks, warehouses, trucks, pallets, containers)
- Mission 5: Daylight Bio-Containment Facility (Skylit modern quarantine lab, catwalks, observation glass)
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

def add_box(name, loc, size, mat=None, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0]/2.0, size[1]/2.0, size[2]/2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    return obj

def add_cyl(name, loc, r, d, rot=(0,0,0), mat=None, verts=14, smooth=True):
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
    print(f"Exported Daylight GLB: {glb_path} ({os.path.getsize(glb_path)} bytes)")
    if obj_path:
        os.makedirs(os.path.dirname(obj_path), exist_ok=True)
        bpy.ops.wm.obj_export(filepath=obj_path, export_materials=True, export_selected_objects=False)
        print(f"Exported OBJ: {obj_path} ({os.path.getsize(obj_path)} bytes)")


# ==============================================================================
# HELPER: VEHICLE GENERATORS (BUS, CAR, VAN, LUGGAGE CART)
# ==============================================================================

def add_bus(parts, loc, rot_y, mat_body, mat_glass, mat_wheel, mat_light):
    bx, by, bz = loc
    # Bus Main Body
    parts.append(add_box(f"Bus_Body_{bx}_{bz}", (bx, by + 1.5, bz), (2.5, 2.4, 7.8), mat_body, rot=(0, rot_y, 0)))
    # Tinted Glass Windows Band
    parts.append(add_box(f"Bus_Glass_{bx}_{bz}", (bx, by + 1.85, bz), (2.54, 0.95, 7.4), mat_glass, rot=(0, rot_y, 0)))
    # Front Windshield
    parts.append(add_box(f"Bus_Windshield_{bx}_{bz}", (bx, by + 1.85, bz - 3.85), (2.4, 1.0, 0.15), mat_glass, rot=(0, rot_y, 0)))
    # Roof Air Conditioner Pod
    parts.append(add_box(f"Bus_AC_{bx}_{bz}", (bx, by + 2.85, bz), (1.6, 0.35, 3.2), mat_body, rot=(0, rot_y, 0)))
    # Headlights
    parts.append(add_box(f"Bus_Headlight_L_{bx}", (bx - 0.9, by + 0.75, bz - 3.92), (0.35, 0.20, 0.08), mat_light, rot=(0, rot_y, 0)))
    parts.append(add_box(f"Bus_Headlight_R_{bx}", (bx + 0.9, by + 0.75, bz - 3.92), (0.35, 0.20, 0.08), mat_light, rot=(0, rot_y, 0)))
    # 4 Wheels
    for wz in [-2.4, 2.4]:
        parts.append(add_cyl(f"Bus_Wheel_L_{bx}_{wz}", (bx - 1.28, by + 0.46, bz + wz), 0.46, 0.28, rot=(0, 0, math.radians(90)), mat=mat_wheel))
        parts.append(add_cyl(f"Bus_Wheel_R_{bx}_{wz}", (bx + 1.28, by + 0.46, bz + wz), 0.46, 0.28, rot=(0, 0, math.radians(90)), mat=mat_wheel))

def add_car(parts, loc, rot_y, mat_paint, mat_glass, mat_wheel, mat_light, mat_trim):
    cx, cy, cz = loc
    # Lower Chassis
    parts.append(add_box(f"Car_Chassis_{cx}_{cz}", (cx, cy + 0.42, cz), (1.85, 0.55, 4.4), mat_paint, rot=(0, rot_y, 0)))
    # Cabin Glass & Roof
    parts.append(add_box(f"Car_Cabin_{cx}_{cz}", (cx, cy + 0.95, cz - 0.2), (1.60, 0.58, 2.2), mat_glass, rot=(0, rot_y, 0)))
    parts.append(add_box(f"Car_Roof_{cx}_{cz}", (cx, cy + 1.25, cz - 0.2), (1.55, 0.06, 1.8), mat_paint, rot=(0, rot_y, 0)))
    # Bumpers
    parts.append(add_box(f"Car_Bumper_F_{cx}", (cx, cy + 0.30, cz - 2.22), (1.80, 0.30, 0.12), mat_trim, rot=(0, rot_y, 0)))
    parts.append(add_box(f"Car_Bumper_R_{cx}", (cx, cy + 0.30, cz + 2.22), (1.80, 0.30, 0.12), mat_trim, rot=(0, rot_y, 0)))
    # Headlights
    parts.append(add_box(f"Car_Light_L_{cx}", (cx - 0.65, cy + 0.45, cz - 2.21), (0.28, 0.14, 0.05), mat_light, rot=(0, rot_y, 0)))
    parts.append(add_box(f"Car_Light_R_{cx}", (cx + 0.65, cy + 0.45, cz - 2.21), (0.28, 0.14, 0.05), mat_light, rot=(0, rot_y, 0)))
    # 4 Wheels
    for wz in [-1.35, 1.35]:
        parts.append(add_cyl(f"Car_Wheel_L_{cx}_{wz}", (cx - 0.94, cy + 0.32, cz + wz), 0.34, 0.22, rot=(0, 0, math.radians(90)), mat=mat_wheel))
        parts.append(add_cyl(f"Car_Wheel_R_{cx}_{wz}", (cx + 0.94, cy + 0.32, cz + wz), 0.34, 0.22, rot=(0, 0, math.radians(90)), mat=mat_wheel))

def add_luggage_trolley(parts, loc, rot_y, mat_metal, mat_luggage1, mat_luggage2):
    tx, ty, tz = loc
    # Frame base on wheels
    parts.append(add_box(f"Trolley_Base_{tx}_{tz}", (tx, ty + 0.18, tz), (0.85, 0.06, 1.4), mat_metal, rot=(0, rot_y, 0)))
    # Push handle
    parts.append(add_box(f"Trolley_Handle_{tx}_{tz}", (tx, ty + 0.65, tz + 0.65), (0.80, 0.95, 0.05), mat_metal, rot=(math.radians(15), rot_y, 0)))
    # Stacked Suitcases
    parts.append(add_box(f"Suitcase_1_{tx}", (tx, ty + 0.34, tz - 0.15), (0.65, 0.26, 0.85), mat_luggage1, rot=(0, rot_y + 0.1, 0)))
    parts.append(add_box(f"Suitcase_2_{tx}", (tx, ty + 0.58, tz - 0.10), (0.60, 0.22, 0.80), mat_luggage2, rot=(0, rot_y - 0.15, 0)))


# ==============================================================================
# 1. MISSION 1 — DAYTIME AIRPORT (GOLD MASTER)
# ==============================================================================

def build_daylight_airport():
    print("\n--- 1. GENERATING MASTER DAYLIGHT AIRPORT TERMINAL ---")
    clear_scene()
    
    # Realistic Daytime Materials (Sunlit PBR)
    m_tiles = create_mat("Mat_AirportFloorTiles", (0.76, 0.78, 0.82, 1.0), metallic=0.08, roughness=0.18) # Polished sunlit tiles
    m_asphalt = create_mat("Mat_RoadAsphalt", (0.34, 0.35, 0.37, 1.0), roughness=0.82) # Sunlit asphalt
    m_curb = create_mat("Mat_ConcreteCurb", (0.72, 0.74, 0.76, 1.0), roughness=0.70) # Concrete curb
    m_curb_yellow = create_mat("Mat_YellowCurb", (0.92, 0.78, 0.12, 1.0), roughness=0.60) # Yellow painted curb
    m_road_line = create_mat("Mat_RoadStripeWhite", (0.94, 0.94, 0.94, 1.0), roughness=0.60) # White road paint
    m_glass = create_mat("Mat_CurtainWallGlass", (0.70, 0.84, 0.96, 0.60), metallic=0.20, roughness=0.04) # Sunlit glass
    m_mullion = create_mat("Mat_SteelMullions", (0.24, 0.26, 0.30, 1.0), metallic=0.85, roughness=0.30)
    m_truss = create_mat("Mat_RoofTrussSteel", (0.48, 0.50, 0.54, 1.0), metallic=0.75, roughness=0.35)
    m_counter = create_mat("Mat_CheckinCounter", (0.90, 0.92, 0.94, 1.0), roughness=0.22)
    m_screen = create_mat("Mat_FlightMonitor", (0.15, 0.45, 0.90, 1.0), emission=(0.15, 0.45, 0.90, 1.0), emission_strength=2.8)
    m_seat = create_mat("Mat_AirportSeat", (0.18, 0.32, 0.52, 1.0), roughness=0.50)
    m_pillar = create_mat("Mat_PillarConcrete", (0.70, 0.72, 0.74, 1.0), roughness=0.72)
    m_bus_paint = create_mat("Mat_BusPaint", (0.92, 0.92, 0.94, 1.0), roughness=0.25)
    m_car_paint1 = create_mat("Mat_CarPaintBlue", (0.14, 0.32, 0.65, 1.0), metallic=0.35, roughness=0.20)
    m_car_paint2 = create_mat("Mat_CarPaintSilver", (0.75, 0.76, 0.78, 1.0), metallic=0.80, roughness=0.25)
    m_wheel = create_mat("Mat_TireRubber", (0.12, 0.12, 0.13, 1.0), roughness=0.85)
    m_light_white = create_mat("Mat_HeadlightGlow", (0.98, 0.98, 1.0, 1.0), emission=(0.98, 0.98, 1.0, 1.0), emission_strength=3.0)
    m_trim = create_mat("Mat_CarTrimBlack", (0.10, 0.10, 0.11, 1.0), roughness=0.60)
    m_luggage1 = create_mat("Mat_LuggageNavy", (0.12, 0.20, 0.35, 1.0), roughness=0.55)
    m_luggage2 = create_mat("Mat_LuggageRed", (0.65, 0.15, 0.12, 1.0), roughness=0.55)
    m_tarmac = create_mat("Mat_DistantTarmac", (0.42, 0.44, 0.46, 1.0), roughness=0.85)
    
    parts = []
    
    # 1. MAIN TERMINAL CONCOURSE FLOOR (Y=0.0, 36m x 24m)
    parts.append(add_box("Concourse_Floor", (0, -0.1, 0), (36.0, 0.2, 24.0), m_tiles))
    
    # 2. EXTERIOR DROP-OFF ROADWAY (FOREGROUND / EXTERIOR, Z = 12 to 24)
    # Asphalt Drop-off Road (2 lanes)
    parts.append(add_box("DropOff_Road", (0, -0.15, 18.0), (36.0, 0.2, 12.0), m_asphalt))
    # Raised Pedestrian Sidewalk & Curbs (Z = 11.5)
    parts.append(add_box("Terminal_Sidewalk", (0, 0.05, 12.0), (36.0, 0.3, 2.0), m_curb))
    parts.append(add_box("Yellow_Curb_Stripe", (0, 0.12, 11.0), (36.0, 0.04, 0.25), m_curb_yellow))
    # Painted White Road Markings (Lane Dividers & Crosswalk)
    for rx in range(-14, 15, 4):
        parts.append(add_box(f"Road_Stripe_{rx}", (rx, -0.04, 18.0), (2.0, 0.01, 0.22), m_road_line))
    for cx in range(-3, 4):
        parts.append(add_box(f"Crosswalk_Bar_{cx}", (cx*1.1, -0.04, 15.0), (0.65, 0.01, 4.0), m_road_line))
        
    # 3. VEHICLES IN DROP-OFF LANE (REAL WORLD VEHICLES AT REAL SCALE)
    # Airport Shuttle Bus parked in drop-off bay
    add_bus(parts, (-9.0, -0.05, 19.5), 0, m_bus_paint, m_glass, m_wheel, m_light_white)
    # Parked Blue Sedan Car
    add_car(parts, (6.0, -0.05, 16.5), math.radians(8), m_car_paint1, m_glass, m_wheel, m_light_white, m_trim)
    # Parked Silver SUV
    add_car(parts, (12.5, -0.05, 19.5), math.radians(-5), m_car_paint2, m_glass, m_wheel, m_light_white, m_trim)
    
    # 4. AIRPORT TERMINAL FRONT ENTRANCE FACADE (GLASS CURTAIN & CANOPY)
    # Large Glass Frontage spanning across Z = 11.0
    parts.append(add_box("Entrance_Glass_Wall", (0, 3.2, 11.0), (34.0, 6.2, 0.08), m_glass))
    for fx in range(-16, 17, 4):
        parts.append(add_box(f"Entrance_Mullion_V_{fx}", (fx, 3.2, 11.0), (0.16, 6.4, 0.18), m_mullion))
    # Overhead Architectural Glass Canopy over drop-off curb
    parts.append(add_box("DropOff_Canopy", (0, 5.2, 13.5), (34.0, 0.25, 4.5), m_glass))
    for cx in [-12, -4, 4, 12]:
        parts.append(add_cyl(f"Canopy_Support_{cx}", (cx, 2.6, 15.5), 0.12, 5.2, mat=m_mullion, verts=10))
        
    # 5. REAR WINDOW FACADE OVERLOOKING TARMAC (BACKGROUND DEPTH, Z = -12.0)
    parts.append(add_box("Tarmac_Glass_Wall", (0, 3.2, -12.0), (34.0, 6.2, 0.08), m_glass))
    for fx in range(-16, 17, 4):
        parts.append(add_box(f"Tarmac_Mullion_V_{fx}", (fx, 3.2, -12.0), (0.16, 6.4, 0.18), m_mullion))
    # Outside Sunlit Runway Tarmac Apron (Z = -12 to -35)
    parts.append(add_box("Sunlit_Tarmac", (0, -0.15, -24.0), (48.0, 0.1, 24.0), m_tarmac))
    # Painted yellow taxiway centerline outside
    parts.append(add_box("Taxiway_Yellow_Line", (0, -0.09, -24.0), (0.35, 0.01, 24.0), m_curb_yellow))
    # Distant Airliner Aircraft Silhouette parked at gate
    parts.append(add_cyl("Airliner_Fuselage", (-10.0, 3.8, -26.0), 2.2, 22.0, rot=(0, math.radians(70), 0), mat=m_bus_paint, verts=16))
    parts.append(add_box("Airliner_Wing", (-9.0, 2.8, -26.0), (14.0, 0.22, 4.2), mat=m_bus_paint, rot=(0, math.radians(22), 0)))
    parts.append(add_cyl("Airliner_Engine", (-6.0, 1.8, -25.5), 0.75, 2.4, rot=(0, math.radians(70), 0), mat=m_mullion, verts=12))
    # Airport Control Tower in background distance
    parts.append(add_cyl("Control_Tower_Shaft", (16.0, 8.0, -30.0), 1.6, 16.0, mat=m_pillar, verts=12))
    parts.append(add_cyl("Control_Tower_Cab", (16.0, 16.5, -30.0), 3.2, 3.0, mat=m_glass, verts=16))
    
    # 6. STRUCTURAL ROOF TRUSSES & NATURAL SKYLIGHTS (DAYLIGHT ENTERS FROM ABOVE)
    for zt in [-8, 0, 8]:
        parts.append(add_box(f"Roof_Truss_Main_{zt}", (0, 6.2, zt), (35.0, 0.32, 0.32), m_truss))
        for xt in range(-14, 15, 4):
            parts.append(add_box(f"Truss_Diagonal_{zt}_{xt}", (xt, 5.8, zt), (1.9, 0.09, 0.09), m_truss, rot=(0, 0, math.radians(35))))
    # Glass Skylights running along the terminal roof
    parts.append(add_box("Roof_Skylight_1", (-6.0, 6.35, 0.0), (4.5, 0.08, 22.0), m_glass))
    parts.append(add_box("Roof_Skylight_2", (6.0, 6.35, 0.0), (4.5, 0.08, 22.0), m_glass))
    
    # 7. ARCHITECTURAL CONCRETE PILLARS (MIDGROUND)
    for px, pz in [(-7, -5), (7, -5), (-7, 5), (7, 5)]:
        parts.append(add_cyl(f"Concourse_Pillar_{px}_{pz}", (px, 3.1, pz), 0.65, 6.2, mat=m_pillar, verts=10))
        parts.append(add_cyl(f"Pillar_Collar_{px}_{pz}", (px, 5.8, pz), 0.85, 0.40, mat=m_mullion, verts=10))
        
    # 8. CHECK-IN DESKS & BAGGAGE SCALES (MIDGROUND)
    for cx, cz in [(-4.5, -6.5), (4.5, -6.5)]:
        parts.append(add_box(f"Desk_{cx}", (cx, 0.55, cz), (3.6, 1.10, 0.90), m_counter))
        parts.append(add_box(f"Desk_Scale_{cx}", (cx + 1.2, 0.18, cz + 0.1), (0.85, 0.35, 1.2), m_mullion))
        parts.append(add_box(f"Desk_Monitor_{cx}", (cx - 0.6, 1.35, cz - 0.2), (0.50, 0.32, 0.04), m_screen))
        
    # 9. FLIGHT INFORMATION DISPLAY MONITORS (FIDS OVERHEAD)
    parts.append(add_box("FIDS_Display_1", (0, 3.8, 0.0), (3.6, 0.95, 0.15), m_screen))
    parts.append(add_cyl("FIDS_Hanger_L", (-1.4, 4.8, 0.0), 0.03, 1.8, mat=m_mullion, verts=8))
    parts.append(add_cyl("FIDS_Hanger_R", (1.4, 4.8, 0.0), 0.03, 1.8, mat=m_mullion, verts=8))
    
    # 10. WAITING BENCH ROWS (FOREGROUND / MIDGROUND COVER)
    for bz in [-1.5, 3.5]:
        parts.append(add_box(f"Bench_Row_L_{bz}", (-4.0, 0.38, bz), (3.2, 0.45, 0.65), m_seat))
        parts.append(add_box(f"Bench_Row_R_{bz}", (4.0, 0.38, bz), (3.2, 0.45, 0.65), m_seat))
        
    # 11. SCATTERED LUGGAGE TROLLEYS & HARD-SHELL BAGS
    add_luggage_trolley(parts, (-1.5, 0.0, 2.0), math.radians(25), m_mullion, m_luggage1, m_luggage2)
    add_luggage_trolley(parts, (2.5, 0.0, -3.0), math.radians(-40), m_mullion, m_luggage2, m_luggage1)
    # Overturned loose suitcase
    parts.append(add_box("Spilled_Luggage_1", (0.5, 0.15, -1.0), (0.65, 0.22, 0.45), m_luggage1, rot=(0, math.radians(55), 0)))
    
    # 12. SECURITY MAGNETOMETER ARCH
    parts.append(add_box("Metal_Detector_L", (-0.65, 1.2, -8.5), (0.14, 2.4, 0.65), m_counter))
    parts.append(add_box("Metal_Detector_R", (0.65, 1.2, -8.5), (0.14, 2.4, 0.65), m_counter))
    parts.append(add_box("Metal_Detector_Top", (0, 2.35, -8.5), (1.44, 0.18, 0.65), m_counter))
    
    airport_obj = join_all(parts, "AirportTerminalGLB")
    export_assets(
        'assets/3d/environments/airport_terminal.glb',
        'models/environment/airport/airport_terminal.obj',
        'tools/blender/generated/airport_terminal.blend'
    )
    print("Master Daylight Airport Terminal generated successfully!")


# ==============================================================================
# 2. MISSION 2 — DAYTIME RAILWAY / METRO STATION
# ==============================================================================

def build_daylight_railway_station():
    print("\n--- 2. GENERATING DAYLIGHT RAILWAY STATION ---")
    clear_scene()
    
    m_platform = create_mat("Mat_PlatformConcrete", (0.74, 0.76, 0.78, 1.0), roughness=0.65)
    m_tactile = create_mat("Mat_TactilePaving", (0.92, 0.80, 0.14, 1.0), roughness=0.55)
    m_steel = create_mat("Mat_StructuralSteel", (0.42, 0.45, 0.48, 1.0), metallic=0.85, roughness=0.30)
    m_rail = create_mat("Mat_SteelRails", (0.55, 0.58, 0.62, 1.0), metallic=0.90, roughness=0.22)
    m_sleepers = create_mat("Mat_WoodSleepers", (0.30, 0.24, 0.18, 1.0), roughness=0.85)
    m_glass = create_mat("Mat_CanopyGlass", (0.72, 0.84, 0.95, 0.60), metallic=0.15, roughness=0.05)
    m_bench = create_mat("Mat_StationBench", (0.22, 0.35, 0.50, 1.0), roughness=0.50)
    m_sign = create_mat("Mat_StationSign", (0.15, 0.45, 0.85, 1.0), emission=(0.15, 0.45, 0.85, 1.0), emission_strength=2.5)
    
    parts = []
    # Platform
    parts.append(add_box("Platform_Floor", (4.0, 0.0, 0), (14.0, 0.20, 36.0), m_platform))
    parts.append(add_box("Tactile_Stripe", (-2.8, 0.105, 0), (0.45, 0.015, 36.0), m_tactile))
    # Tracks & Ballast (Sunlit lower bed)
    parts.append(add_box("Track_Ballast", (-8.0, -1.20, 0), (12.0, 0.20, 36.0), m_platform))
    for rx in [-6.5, -9.5]:
        parts.append(add_box(f"Rail_L_{rx}", (rx - 0.7, -1.03, 0), (0.08, 0.14, 36.0), m_rail))
        parts.append(add_box(f"Rail_R_{rx}", (rx + 0.7, -1.03, 0), (0.08, 0.14, 36.0), m_rail))
        for sz in range(-16, 17, 2):
            parts.append(add_box(f"Sleeper_{rx}_{sz}", (rx, -1.13, sz), (2.0, 0.10, 0.25), m_sleepers))
    # Overhead Catenary Poles & Canopy
    for pz in [-10, 0, 10]:
        parts.append(add_cyl(f"Station_Pillar_{pz}", (4.0, 2.8, pz), 0.40, 5.6, mat=m_steel, verts=10))
        parts.append(add_box(f"Station_Truss_{pz}", (0.0, 5.4, pz), (22.0, 0.30, 0.30), m_steel))
        # Overhead Catenary Power Wire
        parts.append(add_cyl(f"Catenary_Mast_{pz}", (-8.0, 3.5, pz), 0.14, 7.0, mat=m_steel, verts=8))
        parts.append(add_box(f"Catenary_Arm_{pz}", (-7.0, 6.2, pz), (3.5, 0.10, 0.10), m_steel))
    parts.append(add_box("Glass_Canopy_Roof", (4.0, 5.6, 0), (14.0, 0.12, 36.0), m_glass))
    # Benches & Signs
    parts.append(add_box("Station_Transit_Sign", (4.0, 3.6, 0), (3.8, 0.80, 0.12), m_sign))
    parts.append(add_box("Station_Bench_1", (4.0, 0.38, -5.0), (2.8, 0.45, 0.65), m_bench))
    parts.append(add_box("Station_Bench_2", (4.0, 0.38, 5.0), (2.8, 0.45, 0.65), m_bench))
    
    stn_obj = join_all(parts, "RailwayStationGLB")
    export_assets('assets/3d/environments/railway_station.glb', 'models/environment/railway/railway_station.obj', 'tools/blender/generated/railway_station.blend')
    print("Daylight Railway Station generated successfully!")


# ==============================================================================
# 3. MISSION 3 — DAYTIME ABANDONED TRAIN YARD
# ==============================================================================

def build_daylight_train_yard():
    print("\n--- 3. GENERATING DAYLIGHT ABANDONED TRAIN YARD ---")
    clear_scene()
    
    m_body = create_mat("Mat_TrainSteel", (0.75, 0.77, 0.80, 1.0), metallic=0.85, roughness=0.25)
    m_stripe = create_mat("Mat_TrainBlueStripe", (0.15, 0.35, 0.70, 1.0), roughness=0.45)
    m_glass = create_mat("Mat_TrainWindowGlass", (0.70, 0.84, 0.96, 0.55), metallic=0.2, roughness=0.05)
    m_interior = create_mat("Mat_TrainInterior", (0.82, 0.84, 0.86, 1.0), roughness=0.60)
    m_seat = create_mat("Mat_TrainSeats", (0.18, 0.32, 0.55, 1.0), roughness=0.55)
    m_rail = create_mat("Mat_Rails", (0.55, 0.58, 0.62, 1.0), metallic=0.90, roughness=0.22)
    m_ground = create_mat("Mat_TrainYardGround", (0.40, 0.38, 0.34, 1.0), roughness=0.88)
    
    parts = []
    # Ground & Tracks
    parts.append(add_box("Yard_Ground", (0, -0.1, 0), (28.0, 0.2, 36.0), m_ground))
    for rx in [-1.0, 1.0]:
        parts.append(add_box(f"Yard_Rail_{rx}", (rx, 0.05, 0), (0.08, 0.12, 36.0), m_rail))
    # 18m Stainless Steel Train Carriage with Sunlight coming through windows
    parts.append(add_box("Carriage_Floor", (0, 0.55, 0), (2.8, 0.20, 18.0), m_interior))
    parts.append(add_box("Carriage_Roof", (0, 3.25, 0), (2.8, 0.20, 18.0), m_body))
    parts.append(add_box("Carriage_Stripe_L", (-1.42, 1.85, 0), (0.04, 0.35, 18.0), m_stripe))
    parts.append(add_box("Carriage_Stripe_R", (1.42, 1.85, 0), (0.04, 0.35, 18.0), m_stripe))
    # Glass Windows along both sides letting daylight pour in
    parts.append(add_box("Carriage_Glass_L", (-1.41, 2.25, 0), (0.04, 0.75, 17.0), m_glass))
    parts.append(add_box("Carriage_Glass_R", (1.41, 2.25, 0), (0.04, 0.75, 17.0), m_glass))
    # Interior Passenger Seats
    for sz in range(-7, 8, 2):
        parts.append(add_box(f"Train_Seat_L_{sz}", (-0.95, 0.95, sz), (0.75, 0.65, 0.65), m_seat))
        parts.append(add_box(f"Train_Seat_R_{sz}", (0.95, 0.95, sz), (0.75, 0.65, 0.65), m_seat))
    # Shipping Cargo Container near tracks (cover)
    m_crate = create_mat("Mat_CargoContainer", (0.65, 0.20, 0.15, 1.0), roughness=0.60)
    parts.append(add_box("Cargo_Container_1", (5.5, 1.3, -4.0), (2.6, 2.6, 6.2), m_crate))
    
    trn_obj = join_all(parts, "TrainCarriageGLB")
    export_assets('assets/3d/environments/train_carriage.glb', 'models/environment/train/train_carriage.obj', 'tools/blender/generated/train_carriage.blend')
    print("Daylight Train Yard generated successfully!")


# ==============================================================================
# 4. MISSION 4 — DAYTIME INDUSTRIAL STREET
# ==============================================================================

def build_daylight_industrial_street():
    print("\n--- 4. GENERATING DAYLIGHT INDUSTRIAL STREET ---")
    clear_scene()
    
    m_asphalt = create_mat("Mat_AsphaltRoad", (0.35, 0.36, 0.38, 1.0), roughness=0.80) # Sunlit road
    m_sidewalk = create_mat("Mat_ConcreteSidewalk", (0.70, 0.72, 0.74, 1.0), roughness=0.68) # Concrete pavement
    m_road_line = create_mat("Mat_WhiteLine", (0.94, 0.94, 0.94, 1.0), roughness=0.55)
    m_warehouse = create_mat("Mat_WarehouseWall", (0.58, 0.60, 0.64, 1.0), metallic=0.65, roughness=0.45)
    m_dumpster = create_mat("Mat_DumpsterGreen", (0.16, 0.36, 0.22, 1.0), roughness=0.65)
    m_truck = create_mat("Mat_TruckPaint", (0.88, 0.88, 0.90, 1.0), roughness=0.25)
    m_metal = create_mat("Mat_IndustrialMetal", (0.45, 0.48, 0.52, 1.0), metallic=0.85, roughness=0.30)
    m_glass = create_mat("Mat_IndustrialGlass", (0.70, 0.84, 0.96, 0.60), metallic=0.20, roughness=0.05)
    m_wheel = create_mat("Mat_TruckWheel", (0.12, 0.12, 0.13, 1.0), roughness=0.85)
    
    parts = []
    # Asphalt Roadway with Painted Centerlines
    parts.append(add_box("Street_Asphalt", (0, 0, 0), (12.0, 0.20, 36.0), m_asphalt))
    for rz in range(-14, 15, 4):
        parts.append(add_box(f"Street_Centerline_{rz}", (0, 0.105, rz), (0.20, 0.01, 2.0), m_road_line))
    # Concrete Sidewalks & Curbs
    parts.append(add_box("Sidewalk_L", (-8.5, 0.15, 0), (5.0, 0.30, 36.0), m_sidewalk))
    parts.append(add_box("Sidewalk_R", (8.5, 0.15, 0), (5.0, 0.30, 36.0), m_sidewalk))
    # Warehouse Facade with Loading Dock Rollup Doors
    parts.append(add_box("Warehouse_Facade", (-11.5, 4.5, 0), (1.0, 9.0, 36.0), m_warehouse))
    for dz in [-8.0, 8.0]:
        parts.append(add_box(f"Rollup_Door_{dz}", (-10.95, 2.2, dz), (0.12, 4.2, 5.0), m_metal))
    # Parked Delivery Truck at Loading Dock
    parts.append(add_box("Truck_Cab", (-8.5, 1.5, -6.0), (2.4, 2.6, 2.8), m_truck))
    parts.append(add_box("Truck_Windshield", (-8.5, 1.8, -7.35), (2.2, 0.9, 0.10), m_glass))
    parts.append(add_box("Truck_CargoBox", (-8.5, 2.0, -1.5), (2.5, 3.2, 5.8), m_truck))
    for wz in [-7.0, -5.0, -3.0, 0.5]:
        parts.append(add_cyl(f"Truck_Wheel_L_{wz}", (-9.78, 0.48, wz), 0.48, 0.26, rot=(0, 0, math.radians(90)), mat=m_wheel))
        parts.append(add_cyl(f"Truck_Wheel_R_{wz}", (-7.22, 0.48, wz), 0.48, 0.26, rot=(0, 0, math.radians(90)), mat=m_wheel))
    # Commercial Dumpsters & Wooden Pallets
    for dz in [-10.0, 10.0]:
        parts.append(add_box(f"Dumpster_{dz}", (7.5, 0.85, dz), (1.8, 1.4, 2.4), m_dumpster))
        parts.append(add_box(f"Wooden_Pallet_{dz}", (7.5, 0.12, dz + 2.5), (1.2, 0.18, 1.2), m_metal))
        
    street_obj = join_all(parts, "DarkIndustrialGLB")
    export_assets('assets/3d/environments/industrial_street.glb', 'models/environment/industrial/industrial_street.obj', 'tools/blender/generated/industrial_street.blend')
    print("Daylight Industrial Street generated successfully!")


# ==============================================================================
# 5. MISSION 5 — DAYLIGHT BIO-CONTAINMENT FACILITY
# ==============================================================================

def build_daylight_boss_arena():
    print("\n--- 5. GENERATING DAYLIGHT BIO-CONTAINMENT ARENA ---")
    clear_scene()
    
    m_floor = create_mat("Mat_ArenaFloor", (0.75, 0.77, 0.80, 1.0), metallic=0.08, roughness=0.25)
    m_hazard = create_mat("Mat_HazardStripe", (0.95, 0.80, 0.10, 1.0), roughness=0.55)
    m_wall = create_mat("Mat_ContainmentWall", (0.65, 0.68, 0.72, 1.0), metallic=0.50, roughness=0.35)
    m_catwalk = create_mat("Mat_SteelCatwalk", (0.35, 0.38, 0.42, 1.0), metallic=0.85, roughness=0.25)
    m_glass = create_mat("Mat_ObservationGlass", (0.70, 0.85, 0.98, 0.50), metallic=0.20, roughness=0.04)
    m_pipe = create_mat("Mat_ConduitPipes", (0.85, 0.85, 0.88, 1.0), metallic=0.80, roughness=0.28)
    
    parts = []
    # Clean clinical containment floor with yellow perimeter hazard stripes
    parts.append(add_box("Arena_Floor", (0, 0, 0), (34.0, 0.20, 34.0), m_floor))
    # Perimeter Hazard Border (diagonal caution markings)
    for hx in [-16.0, 16.0]:
        parts.append(add_box(f"Hazard_Border_X_{hx}", (hx, 0.105, 0), (1.0, 0.015, 34.0), m_hazard))
    for hz in [-16.0, 16.0]:
        parts.append(add_box(f"Hazard_Border_Z_{hz}", (0, 0.105, hz), (34.0, 0.015, 1.0), m_hazard))
    # 8m Reinforced Containment Blast Walls
    parts.append(add_box("Blast_Wall_Rear", (0, 4.0, -17.0), (34.0, 8.0, 0.8), m_wall))
    parts.append(add_box("Blast_Wall_Left", (-17.0, 4.0, 0), (0.8, 8.0, 34.0), m_wall))
    parts.append(add_box("Blast_Wall_Right", (17.0, 4.0, 0), (0.8, 8.0, 34.0), m_wall))
    # Elevated Observation Control Rooms with Glass Windows overlooking the arena
    parts.append(add_box("Observation_Room", (0, 6.0, -16.5), (24.0, 3.2, 2.4), m_wall))
    parts.append(add_box("Observation_Glass", (0, 6.0, -15.2), (22.0, 2.2, 0.10), m_glass))
    # Perimeter Steel Catwalk & Guardrails
    parts.append(add_box("Catwalk_Platform", (0, 4.2, -15.5), (32.0, 0.18, 2.2), m_catwalk))
    parts.append(add_box("Catwalk_Railing", (0, 4.9, -14.5), (32.0, 0.95, 0.08), m_catwalk))
    # Large Natural Daylight Skylight Truss Roof
    parts.append(add_box("Arena_Skylight_1", (-6.0, 8.2, 0), (6.0, 0.12, 30.0), m_glass))
    parts.append(add_box("Arena_Skylight_2", (6.0, 8.2, 0), (6.0, 0.12, 30.0), m_glass))
    
    arena_obj = join_all(parts, "BossArenaGLB")
    export_assets('assets/3d/environments/boss_arena.glb', 'models/environment/boss_arena/boss_arena.obj', 'tools/blender/generated/boss_arena.blend')
    print("Daylight Bio-Containment Arena generated successfully!")

if __name__ == '__main__':
    print("=== BUILDING ALL DAYLIGHT 3D REALISTIC ENVIRONMENTS ===")
    build_daylight_airport()
    build_daylight_railway_station()
    build_daylight_train_yard()
    build_daylight_industrial_street()
    build_daylight_boss_arena()
    print("=== ALL DAYLIGHT 3D ENVIRONMENTS SUCCESSFULLY BUILT ===")
