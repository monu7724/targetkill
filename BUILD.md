# Sector Zero: Lockdown — Build & Pipeline Reference

## Target Specifications
* **Engine:** Godot 4.5.1 stable official
* **Pipeline:** Blender 4.0.2 headless + GLB/glTF
* **Platform:** Android 7.0+ (API 24 to API 34)
* **Orientation:** Permanent Landscape
* **Budget:** ₹0, 100% original assets

---

## Build Commands

The build pipeline script is available at `scripts/Tools/build_pipeline.sh`.

### 1. Run Automated Test Suites
Runs all 44 runtime gameplay and architectural tests:
```bash
./scripts/Tools/build_pipeline.sh run_tests
```
or directly with Godot:
```bash
godot --headless --path . scenes/test/TestRunner.tscn
```

### 2. Run Visual Acceptance Workflow
Verifies all 9 stages of visual presentation (Main Menu, Mission Select, Daylight Airport, Skeletal Zombies, Gun Viewmodel, Muzzle Flash, Hitmarker, and Result Screen):
```bash
godot --headless -s scripts/Tools/test_visual_acceptance.gd
```

### 3. Validate All 3D Assets
Inspects all 15 core GLB meshes across characters, weapons, zombies, and daylight environments:
```bash
./scripts/Tools/build_pipeline.sh validate_assets
```

### 4. Validate Android Configuration
Verifies Android export presets, SDK build tools, and headless Godot editor compilation:
```bash
./scripts/Tools/build_pipeline.sh validate_android
```

### 5. Build and Sign Android APK
Exports and signs the debug APK using Android SDK 34 build-tools:
```bash
./scripts/Tools/build_pipeline.sh build_apk
```
Output:
`/workspaces/targetkill/SectorZero-Lockdown-debug.apk`

---

## Quality Gates Checklist

- [x] **GATE 1: Boot & Main Menu:** Clean transition to `MAIN_MENU` state, landscape orientation locked.
- [x] **GATE 2: Mission Select & Loading:** Threaded background loading with progress bar and tip display.
- [x] **GATE 3: Mission 1 Playable:** Sunlit airport concourse, drop-off road with cars, bus, tarmac airliner.
- [x] **GATE 4: Mission Complete / Failed:** Count-up reward animation, modal isolation, defeat/victory stings.
- [x] **GATE 5: Mission Transition:** Clean return to Mission Select and progression saved.
- [x] **GATE 6: Memory Lifecycle:** 3x sequential scene load/unload with zero node or resource leaks.
- [x] **GATE 7: Signed Android APK:** Signed binary verified with `apksigner` ready for physical phone installation.
