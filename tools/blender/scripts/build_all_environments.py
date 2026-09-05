import sys
import os
import math
sys.path.append(os.getcwd())
import bpy
from tools.blender.scripts.asset_builder import (
    clear_scene, create_pbr_material, add_box, add_cylinder, add_cone, add_uv_sphere,
    join_objects, export_glb, export_obj
)

def build_airport_props_and_environment():
    print("Building Environment 1: Airport Terminal...")
    clear_scene()
    
    m_floor = create_pbr_material("Mat_AirportFloor", (0.72, 0.74, 0.76, 1.0), metallic=0.10, roughness=0.22)
    m_counter = create_pbr_material("Mat_CounterWood", (0.16, 0.14, 0.12, 1.0), metallic=0.0, roughness=0.52)
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_seat = create_pbr_material("Mat_LoungeSeat", (0.08, 0.14, 0.22, 1.0), metallic=0.0, roughness=0.68)
    m_beacon = create_pbr_material("Mat_EmergencyBeacon", (0.95, 0.08, 0.04, 1.0), metallic=0.1, roughness=0.2, emission=(0.95, 0.08, 0.04, 1.0), emission_strength=3.5)
    m_screen = create_pbr_material("Mat_FlightScreen", (0.04, 0.12, 0.25, 1.0), metallic=0.1, roughness=0.3, emission=(0.08, 0.25, 0.55, 1.0), emission_strength=1.8)
    m_case1 = create_pbr_material("Mat_SuitcaseBrown", (0.35, 0.22, 0.14, 1.0), metallic=0.05, roughness=0.60)
    m_case2 = create_pbr_material("Mat_SuitcaseRed", (0.50, 0.08, 0.08, 1.0), metallic=0.05, roughness=0.60)
    
    # 1. Build checkin_counter prop
    parts_counter = [
        add_box("Desk_Main", (0, 0.60, 0), (2.6, 1.2, 0.8), m_counter),
        add_box("Desk_Top", (0, 1.22, 0), (2.7, 0.05, 0.85), m_metal),
        add_box("Desk_BaggageScale", (1.6, 0.12, 0), (1.0, 0.24, 0.7), m_metal),
        add_cylinder("Monitor_Stand", (-0.6, 1.35, 0), 0.02, 0.20, material=m_metal),
        add_box("Monitor_Frame", (-0.6, 1.55, 0), (0.45, 0.32, 0.06), m_metal),
        add_box("Monitor_Display", (-0.6, 1.55, 0.035), (0.41, 0.28, 0.01), m_screen)
    ]
    obj_counter = join_objects(parts_counter, "Checkin_Counter")
    export_obj('models/environment/airport/checkin_counter.obj')
    
    # 2. Build airport_seats prop
    clear_scene()
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_seat = create_pbr_material("Mat_LoungeSeat", (0.08, 0.14, 0.22, 1.0), metallic=0.0, roughness=0.68)
    parts_seats = [
        add_box("Seat_Beam", (0, 0.40, 0), (1.9, 0.06, 0.08), m_metal),
        add_box("Seat_Leg_L", (-0.8, 0.20, 0), (0.06, 0.40, 0.40), m_metal),
        add_box("Seat_Leg_R", (0.8, 0.20, 0), (0.06, 0.40, 0.40), m_metal)
    ]
    for x_pos in [-0.6, 0.0, 0.6]:
        parts_seats.append(add_box(f"Seat_Cushion_{x_pos}", (x_pos, 0.46, 0), (0.50, 0.06, 0.46), m_seat))
        parts_seats.append(add_box(f"Seat_Back_{x_pos}", (x_pos, 0.74, -0.22), (0.50, 0.52, 0.06), m_seat))
    obj_seats = join_objects(parts_seats, "Airport_Seats")
    export_obj('models/environment/airport/airport_seats.obj')
    
    # 3. Build terminal_pillar prop
    clear_scene()
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_concrete = create_pbr_material("Mat_ConcretePillar", (0.75, 0.77, 0.80, 1.0), metallic=0.05, roughness=0.65)
    m_beacon = create_pbr_material("Mat_EmergencyBeacon", (0.95, 0.08, 0.04, 1.0), metallic=0.1, roughness=0.2, emission=(0.95, 0.08, 0.04, 1.0), emission_strength=3.5)
    parts_pillar = [
        add_box("Pillar_Base", (0, 0.25, 0), (1.1, 0.5, 1.1), m_metal),
        add_box("Pillar_Column", (0, 3.25, 0), (0.8, 5.5, 0.8), m_concrete),
        add_box("Pillar_Capital", (0, 6.15, 0), (1.1, 0.3, 1.1), m_metal),
        add_box("Beacon_Box", (0, 3.0, 0.45), (0.24, 0.32, 0.12), m_metal),
        add_cylinder("Beacon_Dome", (0, 3.0, 0.54), 0.07, 0.12, rotation=(math.radians(90), 0, 0), material=m_beacon)
    ]
    obj_pillar = join_objects(parts_pillar, "Terminal_Pillar")
    export_obj('models/environment/airport/terminal_pillar.obj')
    
    # 4. Build luggage_trolley prop
    clear_scene()
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_case1 = create_pbr_material("Mat_SuitcaseBrown", (0.35, 0.22, 0.14, 1.0), metallic=0.05, roughness=0.60)
    m_case2 = create_pbr_material("Mat_SuitcaseRed", (0.50, 0.08, 0.08, 1.0), metallic=0.05, roughness=0.60)
    parts_cart = [
        add_box("Cart_Base", (0, 0.14, 0), (0.70, 0.06, 1.10), m_metal),
        add_box("Cart_Handle", (0, 0.62, 0.55), (0.65, 0.90, 0.05), m_metal),
        add_box("Suitcase_1", (0, 0.30, -0.10), (0.55, 0.24, 0.75), m_case1),
        add_box("Suitcase_2", (0.02, 0.50, -0.05), (0.48, 0.18, 0.62), m_case2)
    ]
    obj_cart = join_objects(parts_cart, "Luggage_Trolley")
    export_obj('models/environment/airport/luggage_trolley.obj')
    
    # 5. Full Airport Terminal Environment GLB
    clear_scene()
    m_floor = create_pbr_material("Mat_AirportFloor", (0.72, 0.74, 0.76, 1.0), metallic=0.10, roughness=0.22)
    m_counter = create_pbr_material("Mat_CounterWood", (0.16, 0.14, 0.12, 1.0), metallic=0.0, roughness=0.52)
    m_metal = create_pbr_material("Mat_SteelBeam", (0.55, 0.58, 0.62, 1.0), metallic=0.88, roughness=0.28)
    m_seat = create_pbr_material("Mat_LoungeSeat", (0.08, 0.14, 0.22, 1.0), metallic=0.0, roughness=0.68)
    m_concrete = create_pbr_material("Mat_ConcretePillar", (0.75, 0.77, 0.80, 1.0), metallic=0.05, roughness=0.65)
    m_beacon = create_pbr_material("Mat_EmergencyBeacon", (0.95, 0.08, 0.04, 1.0), metallic=0.1, roughness=0.2, emission=(0.95, 0.08, 0.04, 1.0), emission_strength=3.5)
    
    env_parts = [
        add_box("Terminal_Floor", (0, -0.1, 0), (36.0, 0.2, 36.0), m_floor),
        add_box("Rear_Wall", (0, 4.0, -18.0), (36.0, 8.0, 0.5), m_concrete),
        add_box("Front_Wall", (0, 4.0, 18.0), (36.0, 8.0, 0.5), m_concrete),
        add_box("Ceiling_Truss_1", (0, 7.8, -8.0), (36.0, 0.4, 0.6), m_metal),
        add_box("Ceiling_Truss_2", (0, 7.8, 8.0), (36.0, 0.4, 0.6), m_metal),
    ]
    # Add pillars and counters in terminal layout
    for px in [-8.0, 8.0]:
        for pz in [-8.0, 8.0]:
            env_parts.append(add_box(f"Pillar_{px}_{pz}", (px, 3.5, pz), (1.0, 7.0, 1.0), m_concrete))
            env_parts.append(add_cylinder(f"Beacon_{px}_{pz}", (px, 4.0, pz + 0.55), 0.08, 0.12, rotation=(math.radians(90), 0, 0), material=m_beacon))
            
    for cx in [-5.0, 0.0, 5.0]:
        env_parts.append(add_box(f"Counter_{cx}", (cx, 0.6, -12.0), (3.0, 1.2, 0.8), m_counter))
        
    airport_env = join_objects(env_parts, "Airport_Terminal_Environment")
    export_glb('assets/3d/environments/airport_terminal.glb', 'tools/blender/generated/airport_terminal.blend')

def build_railway_props_and_environment():
    print("Building Environment 2: Railway Station...")
    clear_scene()
    
    m_platform = create_pbr_material("Mat_PlatformConcrete", (0.45, 0.46, 0.48, 1.0), metallic=0.05, roughness=0.75)
    m_tactile = create_pbr_material("Mat_TactileStripYellow", (0.85, 0.70, 0.08, 1.0), metallic=0.0, roughness=0.60)
    m_rail = create_pbr_material("Mat_SteelRail", (0.65, 0.68, 0.72, 1.0), metallic=0.92, roughness=0.22)
    m_sleeper = create_pbr_material("Mat_WoodSleeper", (0.22, 0.16, 0.12, 1.0), metallic=0.0, roughness=0.85)
    m_ballast = create_pbr_material("Mat_GravelBallast", (0.28, 0.28, 0.30, 1.0), metallic=0.02, roughness=0.95)
    m_metal = create_pbr_material("Mat_TrussSteel", (0.15, 0.18, 0.22, 1.0), metallic=0.85, roughness=0.35)
    
    # 1. Station Platform Prop
    parts_plat = [
        add_box("Platform_Base", (0, 0.40, 0), (8.0, 0.80, 24.0), m_platform),
        add_box("Tactile_Edge_L", (-3.85, 0.81, 0), (0.30, 0.02, 24.0), m_tactile),
        add_box("Tactile_Edge_R", (3.85, 0.81, 0), (0.30, 0.02, 24.0), m_tactile)
    ]
    obj_plat = join_objects(parts_plat, "Station_Platform")
    export_obj('models/environment/station/station_platform.obj')
    
    # 2. Train Tracks Prop
    clear_scene()
    m_rail = create_pbr_material("Mat_SteelRail", (0.65, 0.68, 0.72, 1.0), metallic=0.92, roughness=0.22)
    m_sleeper = create_pbr_material("Mat_WoodSleeper", (0.22, 0.16, 0.12, 1.0), metallic=0.0, roughness=0.85)
    m_ballast = create_pbr_material("Mat_GravelBallast", (0.28, 0.28, 0.30, 1.0), metallic=0.02, roughness=0.95)
    parts_track = [
        add_box("Ballast_Bed", (0, 0.05, 0), (3.6, 0.10, 20.0), m_ballast),
        add_box("Rail_L", (-0.75, 0.22, 0), (0.08, 0.12, 20.0), m_rail),
        add_box("Rail_R", (0.75, 0.22, 0), (0.08, 0.12, 20.0), m_rail)
    ]
    for z_pos in range(-9, 10, 1):
        parts_track.append(add_box(f"Sleeper_{z_pos}", (0, 0.14, float(z_pos)), (2.4, 0.08, 0.24), m_sleeper))
    obj_track = join_objects(parts_track, "Train_Tracks")
    export_obj('models/environment/station/train_tracks.obj')
    
    # 3. Station Bench Prop
    clear_scene()
    m_metal = create_pbr_material("Mat_BenchMetal", (0.12, 0.14, 0.18, 1.0), metallic=0.85, roughness=0.40)
    m_slat = create_pbr_material("Mat_BenchWood", (0.35, 0.22, 0.14, 1.0), metallic=0.0, roughness=0.70)
    parts_bench = [
        add_box("Bench_Leg_L", (-0.9, 0.22, 0), (0.08, 0.44, 0.50), m_metal),
        add_box("Bench_Leg_R", (0.9, 0.22, 0), (0.08, 0.44, 0.50), m_metal)
    ]
    for y_slat, z_slat in [(0.44, -0.15), (0.44, 0.0), (0.44, 0.15)]:
        parts_bench.append(add_box(f"Seat_Slat_{z_slat}", (0, y_slat, z_slat), (2.0, 0.03, 0.12), m_slat))
    for y_back, z_back in [(0.62, -0.22), (0.76, -0.22)]:
        parts_bench.append(add_box(f"Back_Slat_{y_back}", (0, y_back, z_back), (2.0, 0.10, 0.03), m_slat))
    obj_bench = join_objects(parts_bench, "Station_Bench")
    export_obj('models/environment/station/station_bench.obj')
    
    # 4. Railway Station Full GLB
    clear_scene()
    m_platform = create_pbr_material("Mat_PlatformConcrete", (0.45, 0.46, 0.48, 1.0), metallic=0.05, roughness=0.75)
    m_tactile = create_pbr_material("Mat_TactileStripYellow", (0.85, 0.70, 0.08, 1.0), metallic=0.0, roughness=0.60)
    m_rail = create_pbr_material("Mat_SteelRail", (0.65, 0.68, 0.72, 1.0), metallic=0.92, roughness=0.22)
    m_sleeper = create_pbr_material("Mat_WoodSleeper", (0.22, 0.16, 0.12, 1.0), metallic=0.0, roughness=0.85)
    m_ballast = create_pbr_material("Mat_GravelBallast", (0.28, 0.28, 0.30, 1.0), metallic=0.02, roughness=0.95)
    m_metal = create_pbr_material("Mat_TrussSteel", (0.15, 0.18, 0.22, 1.0), metallic=0.85, roughness=0.35)
    m_wall = create_pbr_material("Mat_StationTiles", (0.35, 0.38, 0.40, 1.0), metallic=0.10, roughness=0.35)
    
    env_station = [
        add_box("Central_Platform", (0, 0.40, 0), (10.0, 0.80, 36.0), m_platform),
        add_box("Yellow_Warning_L", (-4.85, 0.81, 0), (0.30, 0.02, 36.0), m_tactile),
        add_box("Yellow_Warning_R", (4.85, 0.81, 0), (0.30, 0.02, 36.0), m_tactile),
        # Track beds on both sides
        add_box("Track_Bed_L", (-7.5, 0.05, 0), (4.5, 0.10, 36.0), m_ballast),
        add_box("Track_Bed_R", (7.5, 0.05, 0), (4.5, 0.10, 36.0), m_ballast),
        add_box("Rail_L1", (-8.25, 0.22, 0), (0.08, 0.12, 36.0), m_rail),
        add_box("Rail_L2", (-6.75, 0.22, 0), (0.08, 0.12, 36.0), m_rail),
        add_box("Rail_R1", (6.75, 0.22, 0), (0.08, 0.12, 36.0), m_rail),
        add_box("Rail_R2", (8.25, 0.22, 0), (0.08, 0.12, 36.0), m_rail),
        # Outer tunnel walls
        add_box("Tunnel_Wall_L", (-11.0, 4.0, 0), (0.6, 8.0, 36.0), m_wall),
        add_box("Tunnel_Wall_R", (11.0, 4.0, 0), (0.6, 8.0, 36.0), m_wall),
        # Overhead steel arched trusses
        add_box("Truss_Arch_1", (0, 7.5, -10.0), (22.0, 0.4, 0.6), m_metal),
        add_box("Truss_Arch_2", (0, 7.5, 0.0), (22.0, 0.4, 0.6), m_metal),
        add_box("Truss_Arch_3", (0, 7.5, 10.0), (22.0, 0.4, 0.6), m_metal)
    ]
    station_obj = join_objects(env_station, "Railway_Station_Environment")
    export_glb('assets/3d/environments/railway_station.glb', 'tools/blender/generated/railway_station.blend')

def build_train_carriage():
    print("Building Environment 3: Abandoned Train Carriage...")
    clear_scene()
    
    m_body = create_pbr_material("Mat_TrainPaint", (0.14, 0.28, 0.35, 1.0), metallic=0.75, roughness=0.45)
    m_rust = create_pbr_material("Mat_RustSteel", (0.35, 0.18, 0.10, 1.0), metallic=0.45, roughness=0.85)
    m_glass = create_pbr_material("Mat_BrokenGlass", (0.15, 0.25, 0.28, 0.7), metallic=0.90, roughness=0.10)
    m_interior = create_pbr_material("Mat_TrainFloor", (0.20, 0.20, 0.22, 1.0), metallic=0.10, roughness=0.70)
    m_seat = create_pbr_material("Mat_TrainSeat", (0.42, 0.10, 0.08, 1.0), metallic=0.05, roughness=0.80)
    m_bogie = create_pbr_material("Mat_WheelBogie", (0.08, 0.08, 0.09, 1.0), metallic=0.90, roughness=0.35)
    
    parts = []
    # 1. Carriage Floor & Chassis
    parts.append(add_box("Chassis", (0, 0.60, 0), (3.2, 0.25, 18.0), m_rust))
    parts.append(add_box("Floor_Walkway", (0, 0.75, 0), (2.8, 0.05, 17.6), m_interior))
    
    # 2. Outer Corrugated Walls with Window Openings
    parts.append(add_box("Side_Wall_L_Lower", (-1.45, 1.30, 0), (0.15, 1.05, 18.0), m_body))
    parts.append(add_box("Side_Wall_R_Lower", (1.45, 1.30, 0), (0.15, 1.05, 18.0), m_body))
    parts.append(add_box("Side_Wall_L_Upper", (-1.45, 2.70, 0), (0.15, 0.60, 18.0), m_body))
    parts.append(add_box("Side_Wall_R_Upper", (1.45, 2.70, 0), (0.15, 0.60, 18.0), m_body))
    
    # Window posts & glass panels
    for z_win in range(-7, 8, 2):
        parts.append(add_box(f"Win_Glass_L_{z_win}", (-1.45, 2.10, float(z_win)), (0.06, 0.70, 1.4), m_glass))
        parts.append(add_box(f"Win_Glass_R_{z_win}", (1.45, 2.10, float(z_win)), (0.06, 0.70, 1.4), m_glass))
        parts.append(add_box(f"Win_Pillar_L_{z_win}", (-1.45, 2.10, float(z_win) + 0.85), (0.18, 0.75, 0.30), m_body))
        parts.append(add_box(f"Win_Pillar_R_{z_win}", (1.45, 2.10, float(z_win) + 0.85), (0.18, 0.75, 0.30), m_body))
        
    # Curved Arched Roof
    parts.append(add_box("Roof_Center", (0, 3.10, 0), (2.8, 0.15, 18.0), m_rust))
    parts.append(add_box("End_Wall_Front", (0, 1.90, 9.0), (3.0, 2.30, 0.20), m_body))
    parts.append(add_box("End_Wall_Back", (0, 1.90, -9.0), (3.0, 2.30, 0.20), m_body))
    
    # 3. Passenger Interior Seats & Overhead Luggage Racks
    for z_row in [-5.5, -3.0, -0.5, 2.0, 4.5]:
        parts.append(add_box(f"Seat_L_{z_row}", (-0.95, 1.10, z_row), (0.75, 0.55, 0.70), m_seat))
        parts.append(add_box(f"Seat_R_{z_row}", (0.95, 1.10, z_row), (0.75, 0.55, 0.70), m_seat))
    # Overhead Luggage Racks
    parts.append(add_box("Rack_L", (-1.10, 2.50, 0), (0.50, 0.04, 16.0), m_rust))
    parts.append(add_box("Rack_R", (1.10, 2.50, 0), (0.50, 0.04, 16.0), m_rust))
    
    # 4. Undercarriage Bogies & Steel Wheels
    for z_bogie in [-6.0, 6.0]:
        parts.append(add_box(f"Bogie_Frame_{z_bogie}", (0, 0.35, z_bogie), (2.4, 0.20, 2.8), m_bogie))
        for x_w in [-1.1, 1.1]:
            for z_w in [-0.8, 0.8]:
                parts.append(add_cylinder(f"Wheel_{z_bogie}_{x_w}_{z_w}", (x_w, 0.28, z_bogie + z_w), 0.28, 0.12, rotation=(0, 0, math.radians(90)), material=m_bogie))
                
    train_obj = join_objects(parts, "Abandoned_Train_Carriage")
    export_obj('models/environment/train/train_carriage.obj')
    export_glb('assets/3d/environments/train_carriage.glb', 'tools/blender/generated/train_carriage.blend')

def build_industrial_props_and_environment():
    print("Building Environment 4: Dark Industrial Street...")
    clear_scene()
    
    m_asphalt = create_pbr_material("Mat_WetAsphalt", (0.12, 0.13, 0.14, 1.0), metallic=0.15, roughness=0.30)
    m_brick = create_pbr_material("Mat_IndustrialBrick", (0.32, 0.18, 0.15, 1.0), metallic=0.05, roughness=0.85)
    m_shutter = create_pbr_material("Mat_RollerShutter", (0.25, 0.28, 0.32, 1.0), metallic=0.80, roughness=0.45)
    m_metal = create_pbr_material("Mat_GalvanizedSteel", (0.42, 0.44, 0.46, 1.0), metallic=0.85, roughness=0.38)
    m_lamp_glow = create_pbr_material("Mat_SodiumStreetGlow", (1.0, 0.75, 0.20, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.78, 0.22, 1.0), emission_strength=4.0)
    m_dumpster = create_pbr_material("Mat_GreenDumpster", (0.10, 0.24, 0.15, 1.0), metallic=0.35, roughness=0.65)
    
    # 1. Dumpster Prop
    parts_dump = [
        add_box("Dumpster_Tub", (0, 0.65, 0), (2.2, 1.1, 1.4), m_dumpster),
        add_box("Lid_L", (-0.55, 1.25, 0), (1.05, 0.08, 1.35), m_metal),
        add_box("Lid_R", (0.55, 1.25, 0), (1.05, 0.08, 1.35), m_metal),
        # Forklift pockets
        add_box("Pocket_L", (-1.12, 0.55, 0), (0.06, 0.15, 1.2), m_metal),
        add_box("Pocket_R", (1.12, 0.55, 0), (0.06, 0.15, 1.2), m_metal)
    ]
    obj_dump = join_objects(parts_dump, "Dumpster")
    export_obj('models/environment/industrial/dumpster.obj')
    
    # 2. Street Lamp Prop
    clear_scene()
    m_metal = create_pbr_material("Mat_GalvanizedSteel", (0.42, 0.44, 0.46, 1.0), metallic=0.85, roughness=0.38)
    m_lamp_glow = create_pbr_material("Mat_SodiumStreetGlow", (1.0, 0.75, 0.20, 1.0), metallic=0.0, roughness=0.1, emission=(1.0, 0.78, 0.22, 1.0), emission_strength=4.0)
    parts_lamp = [
        add_cylinder("Pole_Base", (0, 0.30, 0), 0.22, 0.60, material=m_metal),
        add_cylinder("Pole_Main", (0, 3.20, 0), 0.10, 5.50, material=m_metal),
        add_box("Arm_Curved", (0.60, 5.80, 0), (1.20, 0.12, 0.12), m_metal),
        add_box("Luminaire_Housing", (1.15, 5.70, 0), (0.50, 0.15, 0.30), m_metal),
        add_box("Lamp_Glass_Glow", (1.15, 5.61, 0), (0.44, 0.02, 0.24), m_lamp_glow)
    ]
    obj_lamp = join_objects(parts_lamp, "Street_Lamp")
    export_obj('models/environment/industrial/street_lamp.obj')
    
    # 3. Full Industrial Street GLB
    clear_scene()
    m_asphalt = create_pbr_material("Mat_WetAsphalt", (0.12, 0.13, 0.14, 1.0), metallic=0.15, roughness=0.30)
    m_curb = create_pbr_material("Mat_ConcreteCurb", (0.40, 0.42, 0.44, 1.0), metallic=0.05, roughness=0.75)
    m_brick = create_pbr_material("Mat_IndustrialBrick", (0.32, 0.18, 0.15, 1.0), metallic=0.05, roughness=0.85)
    m_shutter = create_pbr_material("Mat_RollerShutter", (0.25, 0.28, 0.32, 1.0), metallic=0.80, roughness=0.45)
    m_metal = create_pbr_material("Mat_GalvanizedSteel", (0.42, 0.44, 0.46, 1.0), metallic=0.85, roughness=0.38)
    
    env_ind = [
        add_box("Street_Roadway", (0, -0.1, 0), (12.0, 0.2, 40.0), m_asphalt),
        add_box("Sidewalk_L", (-8.0, 0.08, 0), (4.0, 0.24, 40.0), m_curb),
        add_box("Sidewalk_R", (8.0, 0.08, 0), (4.0, 0.24, 40.0), m_curb),
        # Brick Warehouse Wall L
        add_box("Warehouse_L", (-12.0, 4.5, 0), (4.0, 9.0, 40.0), m_brick),
        add_box("Warehouse_R", (12.0, 4.5, 0), (4.0, 9.0, 40.0), m_brick),
        # Shutter loading doors
        add_box("Shutter_L1", (-9.9, 2.0, -10.0), (0.2, 4.0, 5.0), m_shutter),
        add_box("Shutter_L2", (-9.9, 2.0, 10.0), (0.2, 4.0, 5.0), m_shutter),
        add_box("Shutter_R1", (9.9, 2.0, 0.0), (0.2, 4.0, 5.0), m_shutter)
    ]
    ind_obj = join_objects(env_ind, "Dark_Industrial_Environment")
    export_glb('assets/3d/environments/industrial_street.glb', 'tools/blender/generated/industrial_street.blend')

def build_boss_arena():
    print("Building Environment 5: Final Lockdown Boss Arena...")
    clear_scene()
    
    m_floor = create_pbr_material("Mat_ContainmentFloor", (0.18, 0.20, 0.22, 1.0), metallic=0.55, roughness=0.40)
    m_hazard = create_pbr_material("Mat_HazardYellowBlack", (0.85, 0.72, 0.06, 1.0), metallic=0.10, roughness=0.50)
    m_wall = create_pbr_material("Mat_VaultBlastWall", (0.12, 0.14, 0.16, 1.0), metallic=0.85, roughness=0.35)
    m_siren = create_pbr_material("Mat_EmergencySirenRed", (0.98, 0.04, 0.02, 1.0), metallic=0.1, roughness=0.2, emission=(0.98, 0.04, 0.02, 1.0), emission_strength=4.5)
    m_catwalk = create_pbr_material("Mat_SteelGrateCatwalk", (0.25, 0.27, 0.30, 1.0), metallic=0.90, roughness=0.30)
    
    parts = []
    # 1. Arena Octagonal / Square Reinforced Vault Floor (28m x 28m)
    parts.append(add_box("Arena_Floor", (0, -0.1, 0), (28.0, 0.2, 28.0), m_floor))
    # Hazard Border perimeter strip
    parts.append(add_box("Hazard_Border_N", (0, 0.02, -13.0), (26.0, 0.02, 0.8), m_hazard))
    parts.append(add_box("Hazard_Border_S", (0, 0.02, 13.0), (26.0, 0.02, 0.8), m_hazard))
    parts.append(add_box("Hazard_Border_W", (-13.0, 0.02, 0), (0.8, 0.02, 26.0), m_hazard))
    parts.append(add_box("Hazard_Border_E", (13.0, 0.02, 0), (0.8, 0.02, 26.0), m_hazard))
    
    # 2. Heavy Blast Containment Walls
    parts.append(add_box("Blast_Wall_North", (0, 5.0, -14.0), (28.0, 10.0, 1.5), m_wall))
    parts.append(add_box("Blast_Wall_South", (0, 5.0, 14.0), (28.0, 10.0, 1.5), m_wall))
    parts.append(add_box("Blast_Wall_West", (-14.0, 5.0, 0), (1.5, 10.0, 28.0), m_wall))
    parts.append(add_box("Blast_Wall_East", (14.0, 5.0, 0), (1.5, 10.0, 28.0), m_wall))
    
    # 3. Central Cryo / Bio-Containment Pedestal
    parts.append(add_box("Pedestal_Base", (0, 0.25, -4.0), (6.0, 0.5, 6.0), m_floor))
    parts.append(add_cylinder("Cryo_Tube_1", (-1.8, 1.6, -4.0), 0.50, 2.4, material=m_wall))
    parts.append(add_cylinder("Cryo_Tube_2", (1.8, 1.6, -4.0), 0.50, 2.4, material=m_wall))
    
    # 4. Elevated Perimeter Catwalk with Warning Lights
    parts.append(add_box("Catwalk_North", (0, 4.5, -12.0), (24.0, 0.3, 2.5), m_catwalk))
    parts.append(add_box("Catwalk_Railing", (0, 5.2, -10.8), (24.0, 1.1, 0.08), m_hazard))
    
    # 5. Four Corner Emergency Siren Towers
    for cx, cz in [(-12.0, -12.0), (12.0, -12.0), (-12.0, 12.0), (12.0, 12.0)]:
        parts.append(add_cylinder(f"Siren_Column_{cx}_{cz}", (cx, 3.0, cz), 0.30, 6.0, material=m_wall))
        parts.append(add_cylinder(f"Siren_Light_{cx}_{cz}", (cx, 6.2, cz), 0.22, 0.35, material=m_siren))
        
    boss_arena_obj = join_objects(parts, "Boss_Arena_Containment_Vault")
    export_obj('models/environment/boss_arena/containment_vault.obj')
    export_glb('assets/3d/environments/boss_arena.glb', 'tools/blender/generated/boss_arena.blend')

if __name__ == '__main__':
    build_airport_props_and_environment()
    build_railway_props_and_environment()
    build_train_carriage()
    build_industrial_props_and_environment()
    build_boss_arena()
    print("ALL 5 REALISTIC ENVIRONMENTS & PROPS SUCCESSFULLY BUILT!")
