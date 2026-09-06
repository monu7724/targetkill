# External Asset Manifest & Legal Provenance

This document provides complete provenance, licensing documentation, technical validation, and suitability evaluations for all external assets imported into `assets/external/`.

---

## 1. Vitruvian Human Character & Animations

### `vitruvian_human_complete.glb`
- **Asset Name:** Vitruvian Human Character (Full Armature + Head + Body)
- **Source:** VitruvianGodot by Agile Lens (derived from CharMorph "Vitruvian" base by Sean Buckley & Olaf Delgado-Friedrichs)
- **Source URL:** https://github.com/ibrews/VitruvianGodot
- **License:** **CC0 1.0 Universal (Public Domain)** for 3D meshes & textures; **MIT License** for toolchain/shader code.
- **Commercial Use:** **Permitted** (Public domain / MIT, closed-source and commercial games allowed, no Epic EULA restrictions).
- **Format:** GLB (binary glTF 2.0)
- **File Size:** 37.0 MB
- **Textures:** Embedded PBR (Base Color, Normal, Roughness) derived from `vit_body_*.png` and `vit_face_*.png`.
- **Skeleton / Armature:** **Yes — 52-bone humanoid armature (`mixamo_vitruvian`)** with standard Mixamo bone naming (`Hips`, `Spine`, `Neck`, `Head`, `LeftArm`, `RightArm`, `LeftLeg`, etc.).
- **Animations:** **Yes — 9 skeletal animations included:**
  1. `Idle` (Looping resting breath)
  2. `Walk` (Full humanoid walking stride)
  3. `Attack_mixamo_vitruvian` (Torso coil and upper-body claw swing)
  4. `HitReaction_mixamo_vitruvian` (Violent 35° neck snap and shoulder flinch)
  5. `Death_mixamo_vitruvian` (Knee buckle, spine drop, and ground collapse)
  6. `HappyIdle`
  7. `Sway`
  8. `Turn`
  9. `Wave`
- **Godot Import Status:** **PASS** (Imports cleanly into Godot 4.5.1 via `assets_tests/RealHumanTest.tscn`).
- **Intended Game Use:** Candidate replacement for humanoid zombie enemies and civilian NPC victims.
- **Evaluation & Recommendation:** 
  - *Recommendation:* **USE WITH ADJUSTMENTS / WORK-IN-PROGRESS.**
  - *Pros:* High-poly realistic human anatomy, 52-bone armature, fully functional skeletal walk and death animations.
  - *Caveats:* Head was designed for cinematic portrait close-ups, so head scale requires minor proportional reduction to fit the neck seam perfectly before production replacement.

---

## 2. City Props Kit 1 (Urban Modular Props)

- **Asset Collection:** City Props Kit 1 (Free Edition)
- **Author:** Coding Creature
- **Source URL:** https://codingcreature.com/assets/city-props-kit-1/ (Distribution via https://codingcreature.itch.io/city-props-kit-1/)
- **License:** **CC0 1.0 Universal (Public Domain)**
  - Confirmed on official website and included `README.txt` ("All assets are released under the CC0 license, meaning you're free to use them for personal or commercial projects (no credit needed)").
- **Commercial Use:** **Permitted** (Free for commercial and personal games).
- **Format:** GLB (binary glTF 2.0)
- **File Size:** 98 individual `.glb` files totaling ~15 MB uncompressed.
- **Key Files Imported:**
  - `concrete_jersey_barrier_01_large.glb` (72 KB)
  - `barrel_02_big_red.glb` (85 KB)
  - `barrel_02_big_blue.glb` (85 KB)
  - `barrel_02_big_green.glb` (85 KB)
  - `barrel_02_big_yellow.glb` (85 KB)
  - `fire_hydrant_01.glb` (239 KB)
  - `bus_stop.glb` (993 KB)
  - `traffic_light_01_base_large_black.glb` (82 KB)
  - `digital_information_kiosk_01_medium.glb` (892 KB)
  - `pedestrian_traffic_light_02_base_medium_black.glb` (82 KB)
  - `cctv_camera_01_base.glb` (82 KB)
  - `metal_garbage_can_01_big.glb` (120 KB)
  - `traffic_bollard_01_metal_large.glb` (60 KB)
  - `pallet_medium_large_01.glb` (45 KB)
- **Textures:** Embedded textures and atlas palette (`city_elements_atlas_a.png`, `color_placeholder.png`).
- **Skeleton / Armature:** None (Static rigid props).
- **Animations:** None.
- **Godot Import Status:** **PASS** (All 98 GLBs imported cleanly; verified in `assets_tests/CityPropsTest.tscn`).
- **Intended Game Use:** Street barricades, airport drop-off lanes, industrial zone dressing, and cover props for combat arenas.
- **Evaluation & Recommendation:** **USE (HIGHLY RECOMMENDED).** Clean topology, accurate real-world dimensions, light draw calls, zero rendering glitches.

---

## 3. Poly Haven PBR Materials & Props

- **Source:** Poly Haven
- **Source URL:** https://polyhaven.com/
- **License:** **CC0 1.0 Universal (Public Domain)**
  - Confirmed at https://polyhaven.com/license ("All assets on Poly Haven are licensed as CC0, which means you can use them for any purpose, including commercial work").
- **Commercial Use:** **Permitted** (No royalties, no attribution legally required).
- **Format:** JPG 1k PBR texture sets + Godot `StandardMaterial3D` (`.tres`) + GLB model.

### Material 1: Brushed Concrete (`mat_poly_concrete.tres`)
- **Textures:** 
  - `brushed_concrete_diff_1k.jpg` (847 KB)
  - `brushed_concrete_nor_gl_1k.jpg` (849 KB, OpenGL tangent-space normal)
  - `brushed_concrete_rough_1k.jpg` (701 KB)
- **Godot Import Status:** **PASS**
- **Intended Game Use:** Airport terminal concourses, railway platforms, exterior pavements.

### Material 2: Beige Plaster Wall (`mat_poly_wall.tres`)
- **Textures:**
  - `beige_wall_diff_1k.jpg` (33 KB)
  - `beige_wall_nor_gl_1k.jpg` (153 KB)
  - `beige_wall_rough_1k.jpg` (151 KB)
- **Godot Import Status:** **PASS**
- **Intended Game Use:** Interior airport walls, partition dividers, train station rooms.

### Material 3: Industrial Tread Metal Plate (`mat_poly_metal.tres`)
- **Textures:**
  - `metal_plate_diff_1k.jpg` (692 KB)
  - `metal_plate_nor_gl_1k.jpg` (770 KB)
  - `metal_plate_rough_1k.jpg` (775 KB)
- **Metallic:** 0.95
- **Godot Import Status:** **PASS**
- **Intended Game Use:** Metal walkways, industrial storage containers, security doors.

### Model 1: Poly Haven Industrial Barrel (`barrel_03.glb`)
- **File Size:** 560 KB
- **Textures:** Embedded 1k Diffuse, Normal, ARM (AO/Roughness/Metallic).
- **Godot Import Status:** **PASS**
- **Intended Game Use:** Hazardous explosive barrel placement and environmental obstacles.

- **Evaluation & Recommendation:** **USE (HIGHLY RECOMMENDED).** Exceptional PBR visual quality with zero overexposure, realistic sunlight specular highlights, and optimal 1K resolution tailored for mobile GPU memory.
