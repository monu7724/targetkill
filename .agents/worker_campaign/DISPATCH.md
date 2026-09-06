# DISPATCH — worker_campaign

**Role**: Campaign Architect & Wave Systems Specialist
**Working Directory**: `/workspaces/targetkill/.agents/worker_campaign`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`

## Mission Objective
Build out the 12-mission campaign framework with structured 3-wave progression, gradual cash reward scaling ($500 -> $6,000), single-claim bounty enforcement, and the Airport Service Road environment for Mission 2.

## Detailed Requirements:
1. **12 Mission Resources**:
   - In `resources/missions/`: `mission_01.tres` through `mission_12.tres`.
   - Linear reward scaling: $500 -> $6,000 ($500 * mission_number: M1=$500, M2=$1000, M3=$1500, ..., M12=$6000).
   - Each mission must specify: `wave_count = 3`, `unlock_requirement_id` chained sequentially ("" -> "mission_01" -> ... -> "mission_11"), and appropriate target counts.
   - Mission 1 (`mission_01.tres`) MUST preserve `scene_path = "res://scenes/environments/AirportTerminal.tscn"` or `UrbanStreet.tscn` to ensure Mission 1 remains intact.
   - Mission 2 (`mission_02.tres`) must point to `res://scenes/environments/AirportServiceRoad.tscn`.
2. **MissionData & 3-Wave Engine**:
   - Update `scripts/MissionData.gd` if needed so each mission has `wave_count = 3` and optional structured wave configurations.
   - In `scripts/GameManager.gd`:
     - Ensure each mission spawns exactly 3 substantial waves.
     - Emit `EventBus.wave_started.emit(current_wave, total_waves)` on wave initiation so the HUD can update.
     - Pacing: Wave 1 initial assault, Wave 2 multi-directional escalation, Wave 3 climactic assault.
3. **Single-Claim Bounty Enforcement**:
   - In `scripts/MissionManager.gd`:
     - When completing a mission (`finish_mission(true)`), award cash ONLY if the mission has not been previously completed:
       ```gdscript
       if save_mgr and not save_mgr.is_mission_completed(current_mission.mission_id):
           save_mgr.add_cash(current_mission.reward_cash)
           last_stats["bounty_awarded"] = current_mission.reward_cash
       else:
           last_stats["bounty_awarded"] = 0
       save_mgr.complete_mission(current_mission.mission_id)
       ```
     - Prevent duplicate cash rewards when replaying completed missions.
4. **Airport Service Road Scene**:
   - Create `scenes/environments/AirportServiceRoad.tscn` for Mission 2 with tarmac, barriers, directional lighting, and spawn points.
5. **Exclusive Write Ownership**:
   - `resources/missions/mission_*.tres`
   - `scripts/MissionData.gd`
   - `scripts/MissionManager.gd`
   - `scripts/GameManager.gd`
   - `scenes/environments/AirportServiceRoad.tscn`
   - DO NOT edit `scenes/test/TestRunner.gd`, `scenes/player/Player.gd`, or `scenes/UI/HUD.gd`.

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification:
- Run: `godot --headless -s scripts/Tools/test_mission1_gameplay.gd`
- Run custom verification of mission loading and single-claim cash reward.
- Document commands and results in your `handoff.md`.

## 2026-09-06T15:02:43Z
You are worker_campaign, the Campaign Architect & Wave Systems Specialist.
Your working directory is `/workspaces/targetkill/.agents/worker_campaign`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: You MUST read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md` before starting work.
Read your full assignment in `/workspaces/targetkill/.agents/worker_campaign/DISPATCH.md`.
Scope: Implement 12 missions (mission_01.tres through mission_12.tres in resources/missions/), linear cash scaling ($500 -> $6,000), single-claim bounty enforcement in MissionManager.gd (no duplicate cash rewards on replay), 3-wave campaign progression in GameManager.gd with EventBus.wave_started emission, and create AirportServiceRoad.tscn for Mission 2.
MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
Keep progress.md updated with your heartbeat. Run test commands to verify your work. When done, write handoff.md in your working directory and notify parent orchestrator via send_message.

