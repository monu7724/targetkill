# Handoff Report — Campaign Architecture & Wave System

## 1. Observation

### 1.1 Test Suite Baseline & Verification Status
- Executing `godot --headless scenes/test/TestRunner.tscn`:
  ```
  FINAL VERIFICATION SUMMARY
  Landscape mode             : PASS
  Touch controls             : PASS
  3D player                  : PASS
  FPS Arms presentation      : PASS
  Movement                   : PASS
  Look                       : PASS
  3D weapons                 : PASS
  Fire                       : PASS
  Reload                     : PASS
  Weapon switch              : PASS
  Viewmodel lighting         : PASS
  Touch aim pitch            : PASS
  Camera recoil kick         : PASS
  Muzzle flash light         : PASS
  Reticle and hitmarker      : PASS
  Modal UI isolation         : PASS
  3D zombies                 : PASS
  Zombie AI                  : PASS
  Zombie damage              : PASS
  Zombie death               : PASS
  Rewards                    : PASS
  Player damage              : PASS
  Player death               : PASS
  Airport environment        : PASS
  Railway environment        : PASS
  Train environment          : PASS
  Industrial environment     : PASS
  Final Lockdown             : PASS
  Lighting                   : PASS
  Materials/textures         : PASS
  VFX                        : PASS
  Audio                      : PASS
  Save/load                  : PASS
  Mission 2 unlock           : PASS
  Mission flow               : PASS
  State transitions          : PASS
  Hit zones & multipliers    : PASS
  Advanced Zombie AI         : PASS
  Zombie Director            : PASS
  VFX object pooling         : PASS
  Loading & crash recovery   : PASS
  Performance & Quality profiles : PASS
  Atomic Versioned Save      : PASS
  Memory lifecycle           : PASS
  ==================================================
  TOTAL: 44 / 44 PASSED
  ==================================================
  ```
- Executing `godot --headless assets_tests/Zombie360Test.tscn`:
  ```
  [OK] Player initialized at Vector3.ZERO (movement fixed at origin, 360° aim enabled)
  --- PHASE 1: VERIFYING 4-DIRECTION APPROACH ---
  [PASS] All 4 zombies actively navigating and approaching player from all 360° quadrants.
  --- PHASE 2: VERIFYING MELEE ATTACK BEHAVIOR ---
  [PASS] Zombie Front transitioned to melee ATTACK range (State: 4, Dist: 1.58m)
  --- PHASE 3: VERIFYING HEADSHOT DETECTION & DAMAGE MULTIPLIER ---
  [PASS] Headshot multiplier verified: Exactly 2.5x damage (50.0 DMG) dealt.
  --- PHASE 4: VERIFYING HIT REACTION ANIMATION ---
  [PASS] Hit reaction animations (headshot_reaction / stagger) verified and playable.
  --- PHASE 5: VERIFYING DEATH SEQUENCE & SOUND TRIGGER ---
  [PASS] Death state confirmed: is_dead=true, collision disabled=true
  ==================================================
    360° ZOMBIE INTEGRATION AUDIT: COMPLETE         
  ==================================================
  ```

### 1.2 Mission 1 Scenes & Preservation
- `scenes/environments/UrbanStreet.tscn`:
  - Contains root `[node name="AirportTerminal" type="Node3D"]` (line 55).
  - Contains `[node name="Player" parent="." instance=ExtResource("1_p001")]` (line 129).
  - Contains `[node name="ZombieSpawner" type="Node3D" parent="." node_paths=PackedStringArray("spawn_points")]` with script `res://scripts/GameManager.gd` (line 131-135).
  - Contains 6 spawn points: `SpawnFront` (0, 0, -13), `SpawnBack` (0, 0, 13), `SpawnLeft` (-13, 0, 0), `SpawnRight` (13, 0, 0), `SpawnFrontLeft` (-11, 0, -11), `SpawnFrontRight` (11, 0, -11).
  - Contains `[node name="ResultUI" parent="." instance=ExtResource("7_r001")]` (line 161).
- `scenes/environments/AirportTerminal.tscn`:
  - Diff against `UrbanStreet.tscn` reveals `AirportTerminal.tscn` incorporates `AirportTerminalGLB` (ExtResource 14_glb_air), `AtmosphereEnhancer` (ExtResource 15_atmo), material overrides (`mat_concrete.tres`, `mat_steel.tres`, `mat_wood.tres`), and tuned spawn positions (-8.5m, 8.5m).
- `resources/missions/mission_01.tres`:
  - `scene_path = "res://scenes/environments/AirportTerminal.tscn"` (line 14).
  - `reward_cash = 50` (line 13).
  - `target_count = 10` (line 11).
  - `wave_count = 1` (line 12).
- `scripts/Tools/test_mission1_gameplay.gd`:
  - Line 5: `"MISSION 1 (AIRPORT TERMINAL) PRODUCTION AUDIT"`.
  - Verifies Player, Spawner using `RealisticZombie.tscn`, 4 cardinal spawn points (Front, Back, Left, Right), 360° aim rotation, headshot 2.5x multiplier, and death sequence.

### 1.3 Spawning & Wave Systems
- `scripts/GameManager.gd`:
  - Line 27: `start_next_wave()` called in `_ready()`.
  - Line 38: `zombies_to_spawn = 4 + (current_wave * 2)`.
  - Line 54: `spawn_wave()` spawns single zombies sequentially with a flat `await get_tree().create_timer(1.4).timeout` delay.
  - Line 84: Picks random spawn point > 10m from player.
  - Line 116-130: `_check_wave_end()` notifies `mission_mgr.on_wave_completed()` and starts next wave if `current_wave < mission.wave_count` or `kill_count < mission.target_count`.
  - **Absence**: Never signals the HUD (`update_wave`), never emits `EventBus.wave_started`, has no concept of grouped spawns, directional pacing, or distinct wave compositions.
- `scripts/Zombies/ZombieDirector.gd`:
  - Already possesses production wave logic: signals `wave_started(wave_idx, total_enemies)`, `wave_cleared(wave_idx)`, and `all_waves_completed()`.
  - Line 39: `event_bus.wave_started.emit(current_wave, total_waves)`.
  - Line 135: `event_bus.wave_completed.emit(current_wave)`.
- `scripts/Zombies/SpawnPoint.gd`:
  - Already defines `enum DirectionZone { FRONT, LEFT, RIGHT, REAR, DISTANT }`.

### 1.4 Cash Reward Architecture & Duplicate Cash Bug
- `scripts/MissionManager.gd`:
  - Lines 145-149:
    ```gdscript
    var save_mgr = get_node_or_null("/root/SaveManager")
    if save_mgr:
        save_mgr.add_cash(current_mission.reward_cash)
        save_mgr.complete_mission(current_mission.mission_id)
    ```
  - `save_mgr.add_cash(current_mission.reward_cash)` is called unconditionally on victory, without checking if `save_mgr.is_mission_completed(current_mission.mission_id)`.
  - Replaying a mission grants `current_mission.reward_cash` repeatedly on every completion.
- `scripts/SaveManager.gd`:
  - Line 114: `complete_mission(mission_id: String)` appends to `data.completed_missions` only if not present:
    ```gdscript
    func complete_mission(mission_id: String):
        if not mission_id in data.completed_missions:
            data.completed_missions.append(mission_id)
            save_game()
    ```
  - Line 118: `func is_mission_completed(mission_id: String) -> bool: return mission_id in data.completed_missions`.

### 1.5 UI Systems (MissionSelect, HUD, ResultUI)
- `scripts/MissionSelectUI.gd`:
  - Lines 18-24:
    ```gdscript
    var missions = [
        "res://resources/missions/mission_01.tres",
        "res://resources/missions/mission_02.tres",
        "res://resources/missions/mission_03.tres",
        "res://resources/missions/mission_04.tres",
        "res://resources/missions/mission_05.tres"
    ]
    ```
    Only 5 missions are listed; missions 6–12 are missing.
  - Lines 62-89: Tactical Briefing Modal displays Location, Threat Level (★), Objective, Lore, Recommended Loadout, and Mission Bounty.
- `scripts/MissionCardUI.gd`:
  - Lines 36-53: Sets card visual state (`LOCKED` with "WATCH AD", `COMPLETED` with "REPLAY", `ACTIVE` with "DEPLOY").
- `scripts/HUD.gd`:
  - Line 5: `@onready var wave_label = $Control/TopBar/Margin/HBox/LeftBox/WaveLabel`.
  - Line 347: `func update_wave(value: int): if wave_label: wave_label.text = "WAVE: " + str(value)`.
  - Never invoked by `GameManager.gd`.
- `scripts/ResultUI.gd`:
  - Lines 23-44: Animates cash reward counting upward unconditionally from 0 to `stats.cash`. Does not indicate whether the reward was first-time or a replay with $0 reward.

---

## 2. Logic Chain

1. **Mission 1 Preservation**:
   - `ORIGINAL_REQUEST.md` (lines 38-39) specifies: "Mission 1 remains intact and unmodified."
   - `UrbanStreet.tscn` and `AirportTerminal.tscn` both represent Mission 1 environments. `AirportTerminal.tscn` is referenced by `mission_01.tres` and regression suite `TestRunner.gd`.
   - Modifying neither scene ensures 100% zero-regression compliance for Mission 1.

2. **12-Mission Campaign Progression**:
   - `ORIGINAL_REQUEST.md` (R1, line 13) requires a 12-mission structure, each consisting of exactly 3 large waves, with gradual cash rewards from $500 to $6,000 granted exactly once.
   - 12 missions with $500 steps perfectly span the range:
     $500 + (n - 1) * $500:
     - M1: $500
     - M2: $1,000
     - M3: $1,500
     - M4: $2,000
     - M5: $2,500
     - M6: $3,000
     - M7: $3,500
     - M8: $4,000
     - M9: $4,500
     - M10: $5,000
     - M11: $5,500
     - M12: $6,000
   - Sequential unlock chain: Mission $N$ has `unlock_requirement_id = "mission_%02d" % (N - 1)`, Mission 1 has `""`. This satisfies both linear progression and Test 5 (`mission_02.unlock_requirement_id == "mission_01"`).

3. **Prevention of Duplicate Cash Exploits**:
   - Observation 1.4 confirms `MissionManager.finish_mission` does not check `save_mgr.is_mission_completed` before calling `save_mgr.add_cash`.
   - By querying `save_mgr.is_mission_completed(current_mission.mission_id)` prior to calling `save_mgr.complete_mission()`, the system can determine if this is the first victory.
   - If first victory: award `current_mission.reward_cash`, record `last_stats["cash"] = reward_cash`, set `last_stats["first_time_reward"] = true`.
   - If replay: do not award mission bounty (`last_stats["cash"] = 0`, `last_stats["first_time_reward"] = false`).
   - In `ResultUI.gd`, if `first_time_reward` is false, display `"REPLAY COMPLETE — REWARD PREVIOUSLY CLAIMED"` or `+$0 CASH`.

4. **Wave Architecture (3 Large Waves per Mission)**:
   - Observation 1.3 shows `GameManager.gd` spawns enemies sequentially from random points with no wave configuration or direction logic.
   - Observation 1.3 shows `ZombieDirector.gd` already supports `EventBus.wave_started(wave_idx, total_waves)` and tension curves.
   - Adding a structured `waves: Array[Dictionary]` property to `MissionData.gd` allows each mission to specify:
     ```gdscript
     waves = [
       { "wave_num": 1, "groups": [...] },
       { "wave_num": 2, "groups": [...] },
       { "wave_num": 3, "groups": [...] }
     ]
     ```
   - For Mission 2 (Airport Service Road - Infected Dogs):
     - Wave 1: Small dog groups (e.g., 2 groups of 3 dogs from FRONT and FRONT_LEFT).
     - Wave 2: Larger groups + varied spawn directions (e.g., 3 groups of 4 dogs from LEFT, RIGHT, and REAR).
     - Wave 3: Largest assault + special final group (e.g., 4 groups of 4 dogs + final elite alpha dog pack from multiple directions).
   - If `waves` array is empty, default to standard 3-wave procedural generation (preserving Mission 1).

5. **UI & HUD Synchronization**:
   - `HUD.gd` already contains `wave_label` and `update_wave(value)`.
   - Connecting `EventBus.wave_started` in `HUD._ready()`:
     ```gdscript
     event_bus.wave_started.connect(func(wave_num, total_waves):
         if wave_label:
             wave_label.text = "WAVE: %d / %d" % [wave_num, total_waves]
     )
     ```
     This automatically updates the wave display during gameplay.
   - `MissionSelectUI.gd` missions array needs to list `mission_01.tres` through `mission_12.tres`.

---

## 3. Caveats

- **Dog Asset Status**: `assets/ai_generated/infected_dog/` and `assets/external/animals/` are currently empty directories awaiting models and skeletal animations from the asset stream (`explorer_assets`). Mission 2 wave data can be fully defined and tested using existing archetypes or stubbed dog configs until the GLB models are plugged in.
- **Environment Complex Distribution**: The 12 missions will be distributed across the 5 complexes (Airport, Railway, Urban, Industrial, Quarantine). For missions where specialized sub-areas (e.g. Airport Service Road) are under construction, variants can share existing base scenes with modified lighting/atmosphere profiles.
- **User Savegame State in Test Runs**: TestRunner Test 5 modifies `SaveManager.data.cash` and marks `mission_01` completed. Clearing `user://savegame.json*` or properly resetting defaults before tests guarantees 44/44 clean runs.

---

## 4. Conclusion

1. **Mission 1 Status**: Mission 1 (`UrbanStreet.tscn` / `AirportTerminal.tscn`) is in working order and passes all audit checks (`test_mission1_gameplay.gd` and `TestRunner.gd`). It must not be modified.
2. **12-Mission Resources**: Create `mission_06.tres` through `mission_12.tres` in `resources/missions/` and update `mission_01.tres` through `mission_05.tres` with the $500 -> $6,000 cash progression ($500 per mission).
3. **Cash Reward Fix**: Update `MissionManager.finish_mission` to check `not save_mgr.is_mission_completed(current_mission.mission_id)` before calling `add_cash()`. Update `ResultUI.gd` to display appropriate text when replaying.
4. **Wave Architecture**: Unify wave spawning into a 3-wave system supporting grouped directional spawns, integrated with `EventBus.wave_started(current, total)` and `HUD.wave_label` ("WAVE: 1 / 3").
5. **Mission Select UI**: Update `MissionSelectUI.gd` to load all 12 missions.

---

## 5. Verification Method

### Test Commands
1. **Run Full Regression Suite (Must pass 44/44)**:
   ```bash
   rm -f ~/.local/share/godot/app_userdata/'Sector Zero- Lockdown'/savegame.json*
   godot --headless scenes/test/TestRunner.tscn
   ```
   *Expected output*: `TOTAL: 44 / 44 PASSED`

2. **Run 360° Zombie Test**:
   ```bash
   godot --headless assets_tests/Zombie360Test.tscn
   ```
   *Expected output*: All 5 phases PASS.

3. **Run Mission 1 Gameplay Audit**:
   ```bash
   godot --headless -s scripts/Tools/test_mission1_gameplay.gd
   ```
   *Expected output*: `MISSION 1 AUDIT: ALL TESTS PASSED SUCCESSFULLY`

### Invalidation Conditions
- Any edit made to `scenes/environments/UrbanStreet.tscn` or `scenes/environments/AirportTerminal.tscn` that breaks existing tests.
- Replaying a mission increases player cash by `reward_cash` a second time.
- `TestRunner.tscn` score falls below 44/44.
- Mission select fails to display all 12 missions.
