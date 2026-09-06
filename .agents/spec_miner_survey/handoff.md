# Test Harness & Regression Suite Specification Mining Report

## 1. Observation

### 1.1 Environment & Headless Execution
- **Godot Executable**: `/usr/local/bin/godot`
- **Godot Version**: `4.5.1.stable.official.f62fdbde1`
- **Project Configuration**: `/workspaces/targetkill/project.godot`
  - Window Size: `1280x720`, Stretch Mode: `canvas_items`, Aspect: `expand`, Handheld Orientation: `0` (Landscape).
  - Renderer: `gl_compatibility` (OpenGL ES 3.0 / WebGL 2.0 pipeline, mobile-optimized).
  - Autoload Singletons (registered globally in `project.godot:44-55`):
    1. `AdManager`: `res://scripts/Core/AdManager.gd`
    2. `BannerAdManager`: `res://scripts/Core/BannerAdManager.gd`
    3. `SaveManager`: `res://scripts/SaveManager.gd`
    4. `MissionManager`: `res://scripts/MissionManager.gd`
    5. `AudioManager`: `res://scripts/AudioManager.gd`
    6. `QualityManager`: `res://scripts/QualityManager.gd`
    7. `GameStateManager`: `res://scripts/Core/GameStateManager.gd`
    8. `EventBus`: `res://scripts/Core/EventBus.gd`
    9. `LoadingManager`: `res://scripts/Loading/LoadingManager.gd`
    10. `PerformanceManager`: `res://scripts/Performance/PerformanceManager.gd`
- **Headless Execution Command**:
  - `godot --headless scenes/test/TestRunner.tscn`
  - `godot --headless assets_tests/Zombie360Test.tscn`
  - `godot --headless -s scripts/Tools/<script_name>.gd` (for scripts extending `SceneTree`)
- **Process Termination**:
  - Scenes call `get_tree().quit()` upon completion, returning shell exit code `0`.
  - Scripts extending `SceneTree` call `quit(0)` upon completion.

---

### 1.2 Existing Regression Test Suite (`scenes/test/TestRunner.tscn`)
The primary test harness is implemented in `scenes/test/TestRunner.tscn` with logic in `scenes/test/TestRunner.gd` (373 lines). It executes sequentially across 6 test suites and records assertions in a `results` dictionary (`record_test(name, passed, detail)`). At the end of execution, `_print_summary()` prints `TOTAL: X / 44 PASSED` and invokes `get_tree().quit()`.

#### Complete Enumeration of All 44 Existing Tests

| # | Suite | Test Name | Target / Module | Verification Logic | Pass Condition |
|---|-------|-----------|-----------------|--------------------|----------------|
| 1 | Suite 1: Landscape & Controls | `Landscape mode` | ProjectSettings (`display/window`) | Checks viewport dimensions, handheld orientation, stretch aspect | Width > Height (1280 > 720), Orientation == 0 or 4, Aspect == "expand" |
| 2 | Suite 1: Landscape & Controls | `Touch controls` | `scenes/UI/HUD.tscn` | Instantiates HUD; verifies presence of all 6 mobile touch controls | `VirtualJoystick`, `FireButton`, `ReloadButton`, `SwitchButton`, `LookArea`, `PauseButton` != null |
| 3 | Suite 2: 3D Player & Weapons | `3D player` | `scenes/player/Player.tscn` | Checks player body mesh resource | `PlayerBody/MeshInstance3D.mesh != null` |
| 4 | Suite 2: 3D Player & Weapons | `FPS Arms presentation` | `scenes/player/Player.tscn` | Checks first-person arms mesh resource | `Camera3D/FPSArms/MeshInstance3D.mesh != null` |
| 5 | Suite 2: 3D Player & Weapons | `Movement` | `scenes/player/Player.gd` | Calls `set_virtual_movement(Vector2(0, -1))` and `_physics_process(0.1)` | `player.velocity.length() > 0.0 or player.global_position != Vector3.ZERO` |
| 6 | Suite 2: 3D Player & Weapons | `Look` | `scenes/player/Player.gd` | Calls `rotate_camera(10.0, 10.0)` | `camera.rotation.x != init_cam_rot` |
| 7 | Suite 2: 3D Player & Weapons | `3D weapons` | `scenes/player/Player.gd` | Instantiates weapons from `unlocked_ids` | `player.weapons.size() == 3` |
| 8 | Suite 2: 3D Player & Weapons | `Fire` | `scenes/weapons/Weapon.gd` | Calls `player._trigger_shoot()` on active pistol | `pistol.current_ammo < initial_ammo` (12 -> 11) |
| 9 | Suite 2: 3D Player & Weapons | `Reload` | `scenes/weapons/Weapon.gd` | Sets ammo to 2, calls `_trigger_reload()`, awaits timer | `pistol.current_ammo == pistol.max_ammo` (12/12) |
| 10 | Suite 2: 3D Player & Weapons | `Weapon switch` | `scenes/player/Player.gd` | Calls `switch_weapon()` twice | Switches sequentially: pistol -> rifle -> shotgun |
| 11 | Suite 2: 3D Player & Weapons | `Viewmodel lighting` | `scenes/player/Player.tscn` | Checks dedicated viewmodel lighting nodes | `Camera3D/ViewmodelLight` and `Camera3D/FrontFillLight` != null |
| 12 | Suite 2: 3D Player & Weapons | `Touch aim pitch` | `scenes/player/Player.gd` | Calls `rotate_camera(0.0, -25.0)` (drag up) | Pitch up produces negative rotation.x |
| 13 | Suite 2: 3D Player & Weapons | `Camera recoil kick` | `scenes/player/Player.gd` | Calls `apply_kick(-2.0)` and physics process | Camera angle decreases then recovers |
| 14 | Suite 2: 3D Player & Weapons | `Muzzle flash light` | `scenes/weapons/Weapon.tscn` | Checks weapon node hierarchy | `MuzzleLight` (OmniLight3D) != null |
| 15 | Suite 2: 3D Player & Weapons | `Reticle and hitmarker` | `scenes/UI/HUD.tscn` | Verifies dynamic crosshair & hitmarker | `Control/Crosshair` != null and `Hitmarker.get_child_count() == 4` |
| 16 | Suite 2: 3D Player & Weapons | `Modal UI isolation` | `scenes/UI/HUD.gd` | Calls `_on_game_over(null)` then `toggle_pause()` | `pause_menu.visible == false` and `pause_button.disabled == true` |
| 17 | Suite 3: Zombie AI & Combat | `3D zombies` | `scenes/zombies/Zombie.tscn` | Instantiates 4 archetypes ("normal", "fast", "heavy", "boss") | All 4 archetypes load a valid 3D mesh instance |
| 18 | Suite 3: Zombie AI & Combat | `Zombie AI` | `scenes/zombies/Zombie.gd` | Places zombie 4m from player; runs `_physics_process(0.2)` | Zombie velocity > 0 or distance to player decreases |
| 19 | Suite 3: Zombie AI & Combat | `Zombie damage` | `scripts/HealthComponent.gd` | Calls `zombie.take_damage(25.0)` | Zombie HP decreases from initial HP |
| 20 | Suite 3: Zombie AI & Combat | `Zombie death` | `scenes/zombies/Zombie.gd` | Calls `zombie.take_damage(100.0)` | `zombie.is_dead == true` |
| 21 | Suite 3: Zombie AI & Combat | `Rewards` | `scripts/SaveManager.gd` | Verifies cash reward after killing zombie | `SaveManager.data.cash > start_cash` |
| 22 | Suite 3: Zombie AI & Combat | `Player damage` | `scenes/player/Player.gd` | Calls `player.take_damage(20.0)` | Player HP decreases |
| 23 | Suite 3: Zombie AI & Combat | `Player death` | `scenes/player/Player.gd` | Calls `player.take_damage(200.0)` | `player.is_dead == true` |
| 24 | Suite 4: Realistic Environments | `Airport environment` | `scenes/environments/AirportTerminal.tscn` | Loads scene; verifies Ground, Light, Spawner, GLB node | Has `Ground`, `DirectionalLight3D`, `ZombieSpawner`, `AirportTerminalGLB` |
| 25 | Suite 4: Realistic Environments | `Railway environment` | `scenes/environments/RailwayStation.tscn` | Loads scene; verifies Ground, Light, Spawner, GLB node | Has `Ground`, `DirectionalLight3D`, `ZombieSpawner`, `RailwayStationGLB` |
| 26 | Suite 4: Realistic Environments | `Train environment` | `scenes/environments/AbandonedTrain.tscn` | Loads scene; verifies Ground, Light, Spawner, GLB node | Has `Ground`, `DirectionalLight3D`, `ZombieSpawner`, `TrainCarriageGLB` |
| 27 | Suite 4: Realistic Environments | `Industrial environment` | `scenes/environments/DarkIndustrial.tscn` | Loads scene; verifies Ground, Light, Spawner, GLB node | Has `Ground`, `DirectionalLight3D`, `ZombieSpawner`, `DarkIndustrialGLB` |
| 28 | Suite 4: Realistic Environments | `Final Lockdown` | `scenes/environments/FinalLockdown.tscn` | Loads scene; verifies Ground, Light, Spawner, GLB node | Has `Ground`, `DirectionalLight3D`, `ZombieSpawner`, `BossArenaGLB` |
| 29 | Suite 4: Realistic Environments | `Lighting` | Static Assertion | DirectionalLight3D, Omni beacons, fog, quality profiles | Always true |
| 30 | Suite 4: Realistic Environments | `Materials/textures` | Static Assertion | PBR materials (Albedo, Roughness, Metallic, Normal, Emission) | Always true |
| 31 | Suite 4: Realistic Environments | `VFX` | Static Assertion | Blood splatter, impact debris, muzzle flash, shake | Always true |
| 32 | Suite 4: Realistic Environments | `Audio` | Static Assertion | Weapons, zombies, reload, impacts, footsteps, UI | Always true |
| 33 | Suite 5: Progression & Save/Load | `Save/load` | `scripts/SaveManager.gd` | Sets cash to 777, marks mission_01 complete, saves, clears cash to 0, reloads | Cash restored to 777 and `is_mission_completed("mission_01") == true` |
| 34 | Suite 5: Progression & Save/Load | `Mission 2 unlock` | `resources/missions/mission_02.tres` | Reads `unlock_requirement_id` ("mission_01") | `SaveManager.is_mission_completed(mission_02.unlock_requirement_id) == true` |
| 35 | Suite 5: Progression & Save/Load | `Mission flow` | Static Assertion | Start -> Gameplay -> Objective -> Results -> Rewards -> Next | Always true |
| 36 | Suite 6: Production Architecture | `State transitions` | `scripts/Core/GameStateManager.gd` | Exercises BOOT -> MAIN_MENU -> MISSION_SELECT -> GAMEPLAY -> PAUSED -> GAMEPLAY -> MISSION_COMPLETE | All transitions valid, `is_paused()` toggles, ends at MISSION_COMPLETE |
| 37 | Suite 6: Production Architecture | `Hit zones & multipliers` | `scripts/Combat/HitZone.gd` | Tests HEAD, CHEST, ARM hitzones with 20 base dmg | HEAD deals 50.0 (2.5x, headshot=true), CHEST deals 20.0 (1.0x), ARM deals 14.0 (0.7x) |
| 38 | Suite 6: Production Architecture | `Advanced Zombie AI` | `scenes/zombies/Zombie.gd` | Tests `ai_state` property and 35.0 dmg stagger threshold | `z.ai_state == z.AIState.STAGGER` |
| 39 | Suite 6: Production Architecture | `Zombie Director` | `scripts/Zombies/ZombieDirector.gd` | Simulates wave 2 and wave 3 composition | Wave 2 queue includes "fast", Wave 3 queue includes "heavy" |
| 40 | Suite 6: Production Architecture | `VFX object pooling` | `scripts/VFXManager.gd` (or `ImpactPool.gd`) | Checks pre-allocated pools | Pools for "blood" and "concrete" have >= 10 instances |
| 41 | Suite 6: Production Architecture | `Loading & crash recovery` | `scripts/Loading/LoadingManager.gd` | Verifies async scene loader singleton | `LoadingManager` exists and has `load_scene_async()` |
| 42 | Suite 6: Production Architecture | `Performance & Quality profiles` | `scripts/Performance/PerformanceManager.gd` & `QualityManager.gd` | Changes profile to LOW and MEDIUM | QualityManager reflects LOW then MEDIUM |
| 43 | Suite 6: Production Architecture | `Atomic Versioned Save` | `scripts/SaveManager.gd` | Checks version number and save file existence | `SAVE_VERSION == 2` and `FileAccess.file_exists(SAVE_PATH)` |
| 44 | Suite 6: Production Architecture | `Memory lifecycle` | `scenes/environments/AirportTerminal.tscn` | Sequentially instantiates and frees scene 3 times | Zero crashes or unhandled exceptions |

---

### 1.3 `assets_tests/Zombie360Test.tscn`
- **Script**: `assets_tests/Zombie360Test.gd` (118 lines)
- **Scene**: `assets_tests/Zombie360Test.tscn`
- **Structure**:
  - `Player`: Position fixed at `Vector3.ZERO`, 360° aiming enabled.
  - 4 `RealisticZombie` instances placed at 8m in all 4 cardinal directions:
    - Front: `(0, 0, -8)`
    - Back: `(0, 0, 8)`
    - Left: `(-8, 0, 0)`
    - Right: `(8, 0, 0)`
- **Automated Headless Audit Flow**:
  - Automatically detected via `DisplayServer.get_name() == "headless"`.
  - Phase 1: 4-Direction Approach (150 physics frames / 2.5s; verifies all 4 advance > 0.5m).
  - Phase 2: Melee Attack Behavior (moves front zombie to 1.6m; verifies `ai_state == ATTACK` or distance <= 1.7m).
  - Phase 3: Headshot Detection & 2.5x Multiplier (`take_hit(20.0)` on `HeadHitZone`; verifies 50.0 damage and `is_headshot == true`).
  - Phase 4: Hit Reaction Animation (verifies `headshot_reaction` or `stagger` animation).
  - Phase 5: Death Sequence & Sound Trigger (100 damage lethal blow; verifies `is_dead == true`, collision disabled, death animation engaged).
  - Exits with `get_tree().quit()`.
- **Observed Execution**: Exits with code `0`. All 5 phases PASS.

---

### 1.4 Additional Test Suites & Tool Scripts

| Path | Type | What it Tests | Headless Execution Command | Current Status |
|------|------|---------------|----------------------------|----------------|
| `tools/test_skeletal_zombies_runtime.gd` | `SceneTree` script | Normal (11 anims, 23 bones), Fast (7 anims), Heavy (6 anims), Boss (8 anims, 24 bones) + directional hit reacts | `godot --headless -s tools/test_skeletal_zombies_runtime.gd` | **PASS** (100% clean) |
| `scripts/Tools/test_memory_lifecycle.gd` | `SceneTree` script | 5x repeated M1 -> Results -> MissionSelect -> M1 loop + M1->M2->M1 switch flow; verifies memory leak delta < 5MB | `godot --headless -s scripts/Tools/test_memory_lifecycle.gd` | **PASS** (Delta +0.07 MB) |
| `scripts/Tools/test_mission1_gameplay.gd` | `SceneTree` script | Full Mission 1 audit: 4 spawn points, 4 zombies approach, 360° rotation, headshot/chest/death combat verification | `godot --headless -s scripts/Tools/test_mission1_gameplay.gd` | **PASS** (All audit asserts pass) |
| `assets_tests/CityPropsTest.tscn` | Node3D scene | CC0 urban props presence and transforms | `godot --headless assets_tests/CityPropsTest.tscn` | **PASS** |
| `assets_tests/InfectedZombieTest.tscn` | Node3D scene | Skeleton3D bone count, animation cycling, material bindings | `godot --headless assets_tests/InfectedZombieTest.tscn` | **PASS** |
| `assets_tests/PBRMaterialTest.tscn` | Node3D scene | Poly Haven CC0 PBR textures (Albedo, Normal, Roughness) | `godot --headless assets_tests/PBRMaterialTest.tscn` | **PASS** |
| `assets_tests/RealHumanTest.tscn` | Node3D scene | Vitruvian CC0 humanoid armature & Walk animation | `godot --headless assets_tests/RealHumanTest.tscn` | **PASS** |
| `scenes/test/CaptureRunner.tscn` | Node scene | Multi-screen capture (MainMenu, MissionSelect, Armory, Result, HUD) | `godot --headless scenes/test/CaptureRunner.tscn` | **PASS** |
| `scripts/Tools/test_visual_acceptance.gd` | `SceneTree` script | 9-step visual acceptance gate | `godot --headless -s scripts/Tools/test_visual_acceptance.gd` | **FAIL / HANG**: Line 40 asserts `sun.light_energy >= 2.0`, but `AirportTerminal.tscn` was changed to `0.4`. |

---

### 1.5 SaveManager, Persistence, Reward & Progression Specifications

#### Save Architecture (`scripts/SaveManager.gd`)
- Save file: `user://savegame.json`
- Backup file: `user://savegame.json.bak`
- Temp file: `user://savegame.json.tmp`
- Current format version: `const SAVE_VERSION = 2`
- Write mechanism: Atomic replace (`.tmp` write -> flush -> close -> copy old to `.bak` -> rename `.tmp` to main path).
- Data Schema:
```gdscript
{
    "version": 2,
    "cash": int,
    "completed_missions": Array[String],
    "unlocked_weapons": Array[String], # ["pistol", "rifle", "shotgun"]
    "is_first_launch": bool,           # Controls tutorial display
    "selected_quality": int,           # 0: Low, 1: Medium, 2: High
    "settings": { ... },
    "weapon_upgrades": { ... }
}
```

#### Reward & Progression Mechanics
- `SaveManager.add_cash(amount: int)`: Updates `data.cash`, saves game, emits `EventBus.cash_changed`.
- `SaveManager.complete_mission(mission_id: String)`: Appends `mission_id` to `data.completed_missions`, saves game.
- `SaveManager.is_mission_completed(mission_id: String) -> bool`: Checks membership in `data.completed_missions`.
- `MissionManager.finish_mission(success: bool)`:
  - If `success == true`:
    - Calls `save_mgr.add_cash(current_mission.reward_cash)`
    - Calls `save_mgr.complete_mission(current_mission.mission_id)`
    - Emits `mission_completed(current_mission)`
- **Existing Mission Resources** (`resources/missions/`):
  - `mission_01.tres`: ID `mission_01`, Reward `$50`, Unlock req `""`
  - `mission_02.tres`: ID `mission_02`, Reward `$100`, Unlock req `"mission_01"`
  - `mission_03.tres`: ID `mission_03`, Reward `$200`, Unlock req `"mission_02"`
  - `mission_04.tres`: ID `mission_04`, Reward `$350`, Unlock req `"mission_03"`
  - `mission_05.tres`: ID `mission_05`, Reward `$1000`, Unlock req `"mission_04"`
  - Missions 6 through 12 do not exist yet.
- **Tutorial State Tracking**:
  - `SaveManager.data.is_first_launch`: Defaults to `true`.
  - When `TutorialUI` finishes all 5 steps: sets `SaveManager.data.is_first_launch = false; SaveManager.save_game()`.
  - In `TutorialUI._ready()`: If `not SaveManager.data.is_first_launch`, calls `queue_free()`.

---

## 2. Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Test Harness | 6-Suite Sequential Execution | `TestRunner.gd` runs 6 test suites asynchronously via `await` and records pass/fail status | None (invoked via `_ready()`) | Formatted test tags (`[PASS]`/`[FAIL]`) and total tally | Prints `TOTAL: X / Y PASSED`, quits process | `scenes/test/TestRunner.gd:16-25` |
| 2 | Test Harness | Test Result Aggregation | `record_test(name, passed, detail)` stores assertion outcomes in `results` dictionary | `name: String`, `passed: bool`, `detail: String` | Formatted console output | Marks entry failed if `passed == false` | `scenes/test/TestRunner.gd:5-9` |
| 3 | Test Harness | Headless Exit Signaling | Signals test completion to external CI/scripts | Headless environment | `get_tree().quit()` with exit code 0 | Hangs if await never resolves | `scenes/test/TestRunner.gd:24` |
| 4 | Visual & Asset | Automated Headless 360° Audit | `Zombie360Test.gd` runs 5-phase automated audit without UI intervention when in headless mode | `DisplayServer.get_name() == "headless"` | 5 phase passes in console | Prints `[FAIL]` on threshold deviations and quits | `assets_tests/Zombie360Test.gd:31-35` |
| 5 | Visual & Asset | Skeletal Rig Validation | `tools/test_skeletal_zombies_runtime.gd` validates bone counts (23/24) and required animation lists | Zombie scene archetypes | Assertions pass | Assertion error if animation or bone missing | `tools/test_skeletal_zombies_runtime.gd:19-27` |
| 6 | Visual & Asset | Memory Lifecycle Stress Test | `scripts/Tools/test_memory_lifecycle.gd` verifies 5x scene load/unload with leak threshold < 5MB | Scene resource paths | Measured static memory growth (MB) | Asserts growth < 5MB | `scripts/Tools/test_memory_lifecycle.gd:114-117` |
| 7 | Combat | Multi-Zone Hit Multipliers | `HitZone` computes damage based on hit location | `base_damage: float`, `impact_vector: Vector3` | `HitResult` with `final_damage` and `is_headshot` | Fallback to base damage if unconfigured | `scripts/Combat/HitZone.gd:25-45` |
| 8 | Combat | AI Stagger Reaction | Inflicting >= 35.0 damage triggers `AIState.STAGGER` on zombies | Bullet damage >= 35.0 | Zombie enters stagger state, halts movement | Standard damage without stagger if < 35.0 | `scenes/zombies/Zombie.gd:120-140` |
| 9 | Combat | Encounter Pacing (ZombieDirector) | `ZombieDirector` generates escalating wave composition curve | `current_wave: int` | Populated `spawn_queue` ("normal", "fast", "heavy") | Capped by `max_active_zombies` | `scripts/Zombies/ZombieDirector.gd:43-68` |
| 10 | Persistence | Atomic Versioned Save | Dual-stage `.tmp` file write with atomic rename and `.bak` backup | `SaveManager.data` Dictionary | JSON file written at `user://savegame.json` | Reverts to `.bak` if parse fails; fallback copy on cross-FS | `scripts/SaveManager.gd:36-59` |
| 11 | Persistence | Backwards-Compatible Schema Merge | Merges disk JSON with default dictionary structure | Parsed JSON Dictionary | Updated in-memory `SaveManager.data` | Ignores invalid types, fills missing defaults | `scripts/SaveManager.gd:90-105` |
| 12 | Progression | Mission Unlock Chaining | Unlocks mission cards based on prerequisite completion | Prerequisite `unlock_requirement_id` | UI State: `STATUS: ACTIVE` / `STATUS: LOCKED` | Locks mission and prompts `WATCH AD` button | `scripts/MissionCardUI.gd:29-53` |
| 13 | Progression | First Launch Tutorial Lifecycle | Shows 5-step tutorial on new saves, suppressed after completion | `SaveManager.data.is_first_launch` | Displays tutorial overlay or self-deletes via `queue_free()` | None | `scripts/TutorialUI.gd:15-28` |
| 14 | Progression | Single-Claim CASH Bounty (Spec Req) | R1 requirement: $500 -> $6,000 cash rewards granted strictly once per mission | `mission.reward_cash`, `mission.mission_id` | Increased cash on first win; 0 cash on replay | Duplicate rewards granted in current implementation | `ORIGINAL_REQUEST.md:13`, `MissionManager.gd:147` |

---

## 3. Edge Cases

| # | Feature | Input | Observed Behavior |
|---|---------|-------|-------------------|
| 1 | `TestRunner` Weapon Verification | User's persisted `user://savegame.json` contains `"unlocked_weapons": ["pistol"]` | `Player._init_weapons()` loads only 1 weapon instead of 3. Tests `3D weapons` and `Weapon switch` FAIL, resulting in `42 / 44 PASSED`. When `SaveManager.data.unlocked_weapons` contains `["pistol", "rifle", "shotgun"]`, it achieves `44 / 44 PASSED`. |
| 2 | `SaveManager` Replay Reward Logic | Player completes an already-completed mission (e.g. replaying Mission 1) | `MissionManager.finish_mission()` calls `save_mgr.add_cash(current_mission.reward_cash)` unconditionally. Duplicate cash is granted on every win, violating R1 acceptance criteria ("No duplicate CASH rewards can be claimed on restart"). |
| 3 | `Visual Acceptance Test` Lighting Assertion | `scripts/Tools/test_visual_acceptance.gd` line 40 executed against updated `AirportTerminal.tscn` | `AirportTerminal.tscn` has `DirectionalLight3D.light_energy = 0.4` (dark nighttime/foggy mood), but the script asserts `sun.light_energy >= 2.0`, causing a hard assertion crash and hanging the background process. |
| 4 | Dummy Headless Viewport Capture | Script calls `vp.get_texture().get_image()` under `godot --headless` without Vulkan/X11 | `texture_2d_get` outputs `ERROR: Parameter "t" is null` because headless mode uses the dummy rendering server. Previews cannot be read directly from dummy SubViewport without software render or window display server. |
| 5 | SSAO under GL Compatibility Renderer | Any 3D scene loading an `Environment` with `ssao_enabled = true` | Emits `WARNING: Screen-space ambient occlusion (SSAO) can only be enabled when using the Forward+ renderer`. Non-fatal warning, but pollutes test logs. |
| 6 | ObjectDB Memory Leak Warnings at Exit | Headless test completion and `get_tree().quit()` | Prints `WARNING: ObjectDB instances leaked at exit` and `ERROR: 1 resources still in use at exit`. Normal in Godot when nodes queued for deletion at tree exit are freed during engine teardown. |

---

## 4. Logic Chain

1. **TestRunner Reliability & Autoload Coupling**:
   - *Observation*: Running `godot --headless scenes/test/TestRunner.tscn` initially resulted in `TOTAL: 42 / 44 PASSED` because `Player.gd` queries `SaveManager.data.unlocked_weapons`. The persistent file `/home/codespace/.local/share/godot/app_userdata/Sector Zero- Lockdown/savegame.json` had `"unlocked_weapons": ["pistol"]`.
   - *Logic*: Because `TestRunner.gd` does not initialize or mock `SaveManager.data.unlocked_weapons` before instantiating `Player.tscn`, the regression test suite is coupled to host filesystem state. Resetting `unlocked_weapons` to `["pistol", "rifle", "shotgun"]` immediately produces `44 / 44 PASSED`.
   - *Inference*: Any future test suite expansion must include hermetic test setup (setting `SaveManager.data.unlocked_weapons` explicitly at test start) so tests are 100% reproducible regardless of previous save files.

2. **CASH Reward Single-Claim Specification Gap**:
   - *Observation*: `ORIGINAL_REQUEST.md` lines 13 and 33-34 specify: "Implement gradual CASH rewards ($500 -> $6,000) granted exactly once upon completion" and "No duplicate CASH rewards can be claimed on restart."
   - *Observation*: In `scripts/MissionManager.gd:145-149`:
     ```gdscript
     var save_mgr = get_node_or_null("/root/SaveManager")
     if save_mgr:
         save_mgr.add_cash(current_mission.reward_cash)
         save_mgr.complete_mission(current_mission.mission_id)
     ```
   - *Logic*: `SaveManager.complete_mission` checks `if not mission_id in data.completed_missions`, but `save_mgr.add_cash` is called before checking or recording if the mission was already completed. Replaying a mission currently grants cash multiple times.
   - *Inference*: The implementation must record completed claims (either checking `not is_mission_completed(mission_id)` before calling `add_cash`, or maintaining `data.claimed_rewards: Array[String]`), and test cases must assert that re-completing a mission does not increase cash.

3. **Campaign Scaling ($500 -> $6,000) for 12 Missions**:
   - *Observation*: `resources/missions/` only contains `mission_01.tres` through `mission_05.tres` with rewards: $50, $100, $200, $350, $1,000.
   - *Logic*: R1 requires 12 missions with gradual rewards from $500 to $6,000. A standard linear scaling formula is:
     $$\text{Reward}(m) = 500 + (m - 1) \times 500 = 500 \times m$$
     For $m \in [1, 12]$:
     - Mission 1: $500
     - Mission 2: $1,000
     - Mission 3: $1,500
     - Mission 4: $2,000
     - Mission 5: $2,500
     - Mission 6: $3,000
     - Mission 7: $3,500
     - Mission 8: $4,000
     - Mission 9: $4,500
     - Mission 10: $5,000
     - Mission 11: $5,500
     - Mission 12: $6,000
   - *Inference*: Mission resources `mission_01.tres` through `mission_12.tres` must be created/updated with these reward values, 3-wave objectives (`wave_count = 3`), and chained unlock requirements.

---

## 5. Caveats
1. **Read-Only Investigation**: As a specification miner, no code changes or scene edits have been made to the production repository.
2. **Missing Campaign Assets**: Missions 6 through 12 and the Mission 2 Infected Dog models/animations do not exist in the codebase yet.
3. **Outdated Visual Acceptance Script**: `scripts/Tools/test_visual_acceptance.gd` expects daylight lighting (`light_energy >= 2.0`), which fails because `AirportTerminal.tscn` was aesthetically updated to nighttime/fog (`light_energy = 0.4`). However, this script is not part of the primary regression gate (`scenes/test/TestRunner.tscn`).

---

## 6. Conclusion & Recommendations for Next Agent

### Summary of Discovered Specifications
1. **Current Regression Status**: `godot --headless scenes/test/TestRunner.tscn` passes **44 / 44** when test weapons are unlocked. `godot --headless assets_tests/Zombie360Test.tscn` passes **5 / 5** phases completely.
2. **Headless Execution**: `godot --headless <scene_path>` works reliably on Godot 4.5.1 on Linux, loads all 10 autoloads, and quits cleanly via `get_tree().quit()`.
3. **Primary Implementation Gaps**:
   - Single-claim cash reward enforcement is currently missing in `MissionManager.gd` / `SaveManager.gd`.
   - Campaign only has 5 missions; missions 6-12 must be authored.
   - Rewards are currently $50-$1,000 rather than $500-$6,000.
   - Each mission must be structured around exactly 3 waves.

### Recommended Test Architecture for 12-Mission Campaign
To satisfy all acceptance criteria, the implementation team should structure the test harness as follows:

1. **Harden `scenes/test/TestRunner.gd` Setup**:
   - At the beginning of `_test_player_and_fps_weapons()` in `TestRunner.gd`, add:
     ```gdscript
     var save_mgr = get_node_or_null("/root/SaveManager")
     if save_mgr:
         save_mgr.data.unlocked_weapons = ["pistol", "rifle", "shotgun"]
     ```
   - This ensures the existing 44 regression tests are guaranteed 44/44 without dependence on user save files.

2. **Add Test Suite 7 to `TestRunner.gd`**:
   Add `await _test_campaign_architecture()` to `_run_tests()`:
   - **Test 45: `12-Mission Registry & Chaining`**: Validates that all 12 mission `.tres` files load, have valid IDs, and consecutive unlock chaining (`mission_02` requires `mission_01`, ..., `mission_12` requires `mission_11`).
   - **Test 46: `Gradual Cash Rewards ($500 -> $6,000)`**: Validates that `mission_01` has $500, `mission_12` has $6,000, and all intermediate rewards increase monotonically.
   - **Test 47: `3-Wave Structure`**: Asserts that every mission data resource has `wave_count == 3`.
   - **Test 48: `Single-Claim CASH Reward Logic`**:
     - Reset cash to 0. Complete a mission -> cash increases by reward amount.
     - Call `finish_mission(true)` for the same mission again -> cash does NOT increase.
   - **Test 49: `No Duplicate CASH on Save/Load Restart`**:
     - Save game after claim. Call `load_game()`.
     - Verify cash remains equal to single claim, and reward cannot be re-granted after reload.
   - **Test 50: `Mission 2 Dog Spawner & Hit Zones`**:
     - Verify Mission 2 spawns Infected Dog archetype with Head (2.5x) and Body hitzones.

---

## 7. Verification Method

To independently verify all findings in this report:

```bash
# 1. Verify primary test runner (must report 44 / 44 PASSED)
python3 -c '
import json
path = "/home/codespace/.local/share/godot/app_userdata/Sector Zero- Lockdown/savegame.json"
with open(path, "r") as f: d = json.load(f)
d["unlocked_weapons"] = ["pistol", "rifle", "shotgun"]
with open(path, "w") as f: json.dump(d, f, indent=4)
'
godot --headless scenes/test/TestRunner.tscn

# 2. Verify 360° zombie test (must report COMPLETE and exit 0)
godot --headless assets_tests/Zombie360Test.tscn

# 3. Verify skeletal animations unit test (must report ALL PASSED and exit 0)
godot --headless -s tools/test_skeletal_zombies_runtime.gd

# 4. Verify memory lifecycle stress test (must report PASSED with < 5MB growth)
godot --headless -s scripts/Tools/test_memory_lifecycle.gd
```
