# Project: Sector Zero: Lockdown — 12-Mission Campaign & Mission 2

## Architecture
Sector Zero: Lockdown is a mobile-first stationary 3D zombie FPS built with Godot 4.5.1 under the `gl_compatibility` renderer.
The project architecture is composed of:
- **Core Singletons (Autoloads)**: `SaveManager`, `MissionManager`, `GameStateManager`, `EventBus`, `QualityManager`, `PerformanceManager`, `LoadingManager`, `AudioManager`.
- **Campaign Data**: `MissionData` resources (`resources/missions/mission_01.tres` through `mission_12.tres`) defining unlock dependencies, 3-wave compositions, threat ratings, and single-claim cash bounties ($500 -> $6,000).
- **Combat & Spawning**: `GameManager.gd` / `ZombieDirector.gd` managing stationary 360-degree combat with 3 large waves per mission, directional spawn points (`DirectionZone`), and `HitZone` detection (`HEAD` 2.5x, `CHEST` 1.0x, `LEG` 0.7x).
- **Environment Complexes**: 5 reusable complexes (Airport, Railway, Urban, Industrial, Quarantine) using batched GLB meshes, realistic PBR materials, and mobile-friendly directional lighting profiles.
- **UI Architecture**: `HUD.tscn` (mobile touch controls, wave indicator `WAVE: %d / %d`, boss bar, reticle), `MissionSelectUI.tscn` (12-mission grid + briefing modal), `ResultUI.tscn` (victory stats, single-claim cash display).

## Feature Inventory
Every feature identified during the Step 0 Survey is cataloged below with its assigned milestone:

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | F1: 12-Mission Registry | Complete definitions for `mission_01.tres` to `mission_12.tres` with sequential unlock requirements | M1 | Survey (Campaign Explorer / Spec Miner) |
| 2 | F2: Gradual Cash Scaling | Linear bounty scaling ($500 -> $6,000 in $500 steps) | M1 | Survey (Spec Miner / Campaign Explorer) |
| 3 | F3: Single-Claim Bounty Enforcement | Prevent duplicate cash rewards on replay or restart in `MissionManager.gd` / `SaveManager.gd` | M1 | Survey (Spec Miner / Campaign Explorer) |
| 4 | F4: Save/Load Persistence | Version 2 atomic JSON persistence for unlocked missions and single-claim cash | M1 | Survey (Spec Miner) |
| 5 | F5: 3-Wave Spawning Engine | Structured 3-wave system in `GameManager.gd` / `MissionData.gd` with directional groups | M1 | Survey (Campaign Explorer) |
| 6 | F6: Wave & Result UI Sync | HUD wave display (`WAVE: X / 3`) via `EventBus.wave_started` and replay status on `ResultUI` | M1 | Survey (Campaign Explorer) |
| 7 | F7: 12-Mission Select UI | Expanded `MissionSelectUI.gd` displaying all 12 missions with tactical briefings | M1 | Survey (Campaign Explorer) |
| 8 | F8: 5 Environment Complexes | Airport, Railway, Urban, Industrial, Quarantine complexes with distinct atmospheres | M2 | Survey (Assets Explorer) |
| 9 | F9: Airport Service Road Scene | Dedicated `AirportServiceRoad.tscn` for Mission 2 with tarmac, hangars, and barriers | M2 | Survey (Assets Explorer) |
| 10 | F10: Infected Dog Skeletal Rig | 18-bone quadruped armature with 5 animations (run, attack, hit_head, hit_body, death) | M3 | Survey (Assets Explorer) |
| 11 | F11: Dog Combat & HitZones | Dedicated `HeadHitZone` (2.5x) and `BodyHitZone` (1.0x), quadruped AI, SFX audio | M3 | Survey (Assets Explorer) |
| 12 | F12: Mission 2 Wave Progression | 3 escalating waves: W1 (6 dogs), W2 (12 dogs 3 directions), W3 (14 dogs + Alpha dog) | M3 | Survey (Assets Explorer / Campaign Explorer) |
| 13 | F13: Android 720p 60fps & CC0 | `gl_compatibility` compliance, <100 draw calls, <=3 lights, ASTC/ETC2, full CC0 licenses | M4 | Survey (Assets Explorer) |
| 14 | F14: Mission 1 Preservation | `UrbanStreet.tscn` and `AirportTerminal.tscn` remain intact; all 44 regression tests pass | M1 / M5 | Survey (All Explorers) |
| 15 | F15: Comprehensive Test Expansion | New test suites covering campaign registry, cash scaling, single claim, waves, and dog hitzones | M5 | Survey (Spec Miner) |

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Campaign Architecture, Wave Engine & Reward Integrity (R1) | 12-mission resources (`mission_01` to `mission_12`), single-claim cash fix in `MissionManager.gd`/`SaveManager.gd`, 3-wave system in `GameManager.gd`, HUD wave label sync, `MissionSelectUI` expansion. Mission 1 untouched. | none | PLANNED |
| M2 | Reusable Environment Complexes & Airport Service Road (R2) | `AirportServiceRoad.tscn` creation for Mission 2, environment setup, CC0 props integration, lighting profiles, `ASSET_LICENSES.md` documentation. | M1 | PLANNED |
| M3 | Infected Dog Skeletal Rig, Combat AI & Mission 2 Wave Deployment (R3) | Procedural/CC0 quadruped GLB (`infected_dog.glb`) with 18 bones & 5 animations, `InfectedDog.tscn` with Head/Body `HitZone`s, dog SFX, and Mission 2 wave configuration. | M1, M2 | PLANNED |
| M4 | Performance & Android Targeting (R4) | Audit draw calls, dynamic lights (<=3), textures (<=1024), particle counts, memory lifecycle test, and `ASSET_LICENSES.md` compliance. | M2, M3 | PLANNED |
| M5 | Final E2E Test Suite Pass & Adversarial Hardening (AC & Workstream F) | Run full headless regression suite (`TestRunner.tscn` >= 50/50), `Zombie360Test.tscn`, `test_mission1_gameplay.gd`, new campaign tests, adversarial edge case stress testing. | M1, M2, M3, M4 | PLANNED |

## Interface Contracts

### MissionData ↔ GameManager
- `MissionData.wave_count: int` (always 3)
- `MissionData.waves: Array[Dictionary]`
  - Each wave dict: `{"wave_num": int, "groups": Array[Dictionary]}`
  - Each group dict: `{"enemy_type": String, "count": int, "spawn_direction": String, "delay": float}`
- If `MissionData.waves` is empty, `GameManager` falls back to procedural 3 waves (preserving Mission 1).

### GameManager ↔ HUD
- `EventBus.wave_started.emit(current_wave: int, total_waves: int)`
- `HUD.gd` connects to `EventBus.wave_started` to update `WaveLabel.text = "WAVE: %d / %d" % [current_wave, total_waves]`.

### MissionManager ↔ SaveManager (Reward Single-Claim Contract)
- `MissionManager.finish_mission(success: bool)`:
  - If `success == true`:
    - Check: `var is_first_win = not save_mgr.is_mission_completed(current_mission.mission_id)`
    - If `is_first_win`:
      - `save_mgr.add_cash(current_mission.reward_cash)`
      - `last_stats["bounty_awarded"] = current_mission.reward_cash`
    - Else:
      - Do NOT call `add_cash()`
      - `last_stats["bounty_awarded"] = 0`
    - `save_mgr.complete_mission(current_mission.mission_id)`

### InfectedDog ↔ Weapon (Combat HitZone Contract)
- `InfectedDog` root `CharacterBody3D` in group `"zombies"`
- `HeadHitZone` (Area3D, `zone_type = 0` / HEAD) at `pos = Vector3(0, 0.52, -0.45)` with `damage_multiplier = 2.5`
- `BodyHitZone` (Area3D, `zone_type = 1` / CHEST) at `pos = Vector3(0, 0.38, 0.05)` with `damage_multiplier = 1.0`
- Responds to `take_hit(damage: float, impact_vector: Vector3)` and returns `HitResult`
- Responds to `take_damage(amount: float)`

## Code Layout
- `resources/missions/`: `mission_01.tres` through `mission_12.tres` (MissionData resources)
- `scripts/`:
  - `MissionData.gd`: Resource definition
  - `MissionManager.gd`: Mission lifecycle, reward granting logic
  - `SaveManager.gd`: Atomic persistence, completed missions and cash tracking
  - `GameManager.gd`: Wave spawning controller, stationary combat loop
  - `MissionSelectUI.gd`: Mission selection UI
  - `ResultUI.gd`: Post-mission summary screen
- `scenes/UI/`: `HUD.tscn`, `HUD.gd`, `MissionSelectUI.tscn`, `ResultUI.tscn`
- `scenes/environments/`:
  - `UrbanStreet.tscn`: Mission 1 environment (MUST REMAIN INTACT)
  - `AirportTerminal.tscn`: Mission 1 environment (MUST REMAIN INTACT)
  - `AirportServiceRoad.tscn`: Mission 2 environment
  - `RailwayStation.tscn`, `AbandonedTrain.tscn`, `DarkIndustrial.tscn`, `FinalLockdown.tscn`: Environment complexes
- `scenes/zombies/`:
  - `Zombie.tscn`, `Zombie.gd`: Generic zombie base
  - `InfectedDog.tscn`, `InfectedDog.gd`: Mission 2 quadruped infected canine
- `assets/3d/zombies/`: `infected_dog.glb`
- `scenes/test/`: `TestRunner.tscn`, `TestRunner.gd`
- `assets_tests/`: `Zombie360Test.tscn`, `Zombie360Test.gd`
- `ASSET_LICENSES.md`: CC0 and MIT licensing documentation
