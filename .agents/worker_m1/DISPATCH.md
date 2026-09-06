# DISPATCH — Worker M1: Campaign Architecture, Wave Engine & Reward Integrity

## Objective
Implement Milestone 1 (Campaign Architecture, Wave Engine & Reward Integrity) for Sector Zero: Lockdown.

## MANDATORY INTEGRITY WARNING
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Context & Inputs
- Read `/workspaces/targetkill/ORIGINAL_REQUEST.md` (mandatory).
- Read `/workspaces/targetkill/PROJECT.md`.
- Read `/workspaces/targetkill/.agents/spec_miner_survey/handoff.md`.
- Read `/workspaces/targetkill/.agents/explorer_campaign/handoff.md`.

## Write Ownership
You exclusively own and may modify:
- `resources/missions/` (`mission_01.tres` through `mission_12.tres`)
- `scripts/MissionData.gd`
- `scripts/MissionManager.gd`
- `scripts/SaveManager.gd`
- `scripts/GameManager.gd`
- `scripts/MissionSelectUI.gd`
- `scenes/UI/HUD.gd` (or `scripts/UI/HUD.gd`)
- `scripts/ResultUI.gd`
DO NOT touch `scenes/environments/UrbanStreet.tscn` or `scenes/environments/AirportTerminal.tscn` (Mission 1 must remain intact).

## Specific Implementation Requirements
1. **12-Mission Resources**:
   - Update `mission_01.tres` through `mission_05.tres` and create `mission_06.tres` through `mission_12.tres`.
   - Each mission resource must have:
     - Linear cash rewards: M1 ($500), M2 ($1,000), M3 ($1,500), ..., M12 ($6,000).
     - Unlock chaining: `mission_01` has `unlock_requirement_id = ""`; `mission_%02d` requires `mission_%02d` (N-1).
     - `wave_count = 3`.
     - Plausible lore, location, threat stars, and scene path pointing to appropriate environment complex.
2. **Reward Single-Claim Enforcement**:
   - In `scripts/MissionManager.gd:finish_mission(success: bool)`:
     - Check `if not save_mgr.is_mission_completed(current_mission.mission_id):` before awarding cash!
     - If first completion: award `current_mission.reward_cash`.
     - If replaying an already-completed mission: grant $0 bounty (`last_stats["bounty_awarded"] = 0`).
     - In `scripts/ResultUI.gd`, indicate if bounty was claimed or if replay yielded $0.
3. **Structured 3-Wave Spawning Engine**:
   - In `scripts/MissionData.gd`, add `@export var waves: Array[Dictionary] = []`.
   - In `scripts/GameManager.gd`:
     - Run 3 distinct waves.
     - Emit `EventBus.wave_started(current_wave, 3)` at the start of each wave.
     - Connect `HUD.update_wave(current_wave)` or listen via `EventBus` so the HUD displays `WAVE: %d / 3`.
     - Support directional groups if specified in `mission.waves`, otherwise use procedural wave scaling.
4. **Mission Select UI Expansion**:
   - Update `scripts/MissionSelectUI.gd` to load and display all 12 missions.
5. **Build and Test Verification**:
   - Run `godot --headless scenes/test/TestRunner.tscn` — ensure all regression tests pass (>= 44/44).
   - Run `godot --headless assets_tests/Zombie360Test.tscn` — ensure all 5 phases pass.
   - Run `godot --headless -s scripts/Tools/test_mission1_gameplay.gd` — ensure Mission 1 passes intact.

## Output Requirements
Write your completion report to `/workspaces/targetkill/.agents/worker_m1/handoff.md`.
Include the exact test execution commands and terminal outputs.
When done, message orchestrator.

## 2026-09-06T13:14:39Z
You are the Worker for Milestone 1 (Campaign Architecture, Wave Engine & Reward Integrity).
Your working directory is /workspaces/targetkill/.agents/worker_m1/.
Read /workspaces/targetkill/ORIGINAL_REQUEST.md (mandatory), /workspaces/targetkill/PROJECT.md, /workspaces/targetkill/.agents/explorer_campaign/handoff.md, and /workspaces/targetkill/.agents/worker_m1/DISPATCH.md.
MANDATORY INTEGRITY WARNING: DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
Implement the 12-mission resources with linear $500->$6000 scaling, single-claim cash reward enforcement, 3-wave spawning with directional groups in GameManager.gd, wave indicator sync in HUD, and expanded MissionSelectUI. Keep Mission 1 (UrbanStreet.tscn / AirportTerminal.tscn) 100% intact.
Run godot --headless scenes/test/TestRunner.tscn, Zombie360Test.tscn, and test_mission1_gameplay.gd to verify.
Write your handoff to /workspaces/targetkill/.agents/worker_m1/handoff.md and notify orchestrator when done.
