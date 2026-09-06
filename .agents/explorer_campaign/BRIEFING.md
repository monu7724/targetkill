# BRIEFING — 2026-09-06T13:12:00Z

## Mission
Investigate campaign architecture, wave management, spawning, stationary-FPS mechanics, progression, cash rewards ($500 -> $6000), and mission select UI in Sector Zero: Lockdown.

## 🔒 My Identity
- Archetype: Explorer
- Roles: Campaign Architecture & Wave System Explorer
- Working directory: /workspaces/targetkill/.agents/explorer_campaign/
- Original parent: 99c0ac96-a596-4724-a7a2-034957bdda66
- Milestone: 12-Mission Campaign Architecture & Mission 2 Foundation

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Write ONLY to /workspaces/targetkill/.agents/explorer_campaign/
- Never modify game source code or test files
- Ensure Mission 1 (UrbanStreet.tscn) remains intact and unmodified

## Current Parent
- Conversation ID: 99c0ac96-a596-4724-a7a2-034957bdda66
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `scenes/environments/UrbanStreet.tscn` & `AirportTerminal.tscn`
  - `scenes/player/Player.tscn` & `Player.gd`
  - `scripts/GameManager.gd`, `ZombieDirector.gd`, `SpawnPoint.gd`
  - `scripts/SaveManager.gd`, `MissionManager.gd`, `MissionData.gd`
  - `scenes/UI/MissionSelect.tscn`, `MissionCard.tscn`, `HUD.tscn`, `ResultUI.tscn`
  - `scenes/test/TestRunner.tscn`, `assets_tests/Zombie360Test.tscn`, `scripts/Tools/test_mission1_gameplay.gd`
- **Key findings**:
  - Mission 1 (`UrbanStreet.tscn` / `AirportTerminal.tscn`) is in full working order, verified by TestRunner (44/44 PASS) and Mission 1 audit.
  - Duplicate cash reward bug identified in `MissionManager.finish_mission`: rewards added unconditionally without `is_mission_completed()` check.
  - Cash reward progression mapped linearly across 12 missions: $500 -> $6,000 ($500 per mission).
  - Wave system in `GameManager.gd` needs unification to support 3 large waves per mission with grouped directional spawns, connected to `EventBus.wave_started` and `HUD.wave_label`.
  - `MissionSelectUI.gd` currently hardcodes only 5 missions and needs expansion to all 12 missions.
- **Unexplored areas**: None within campaign architecture scope.

## Key Decisions Made
- Confirmed Mission 1 scenes must remain completely unmodified.
- Established clean $500-step linear cash progression curve.
- Formalized first-time reward check logic to eliminate duplicate cash exploits.
- Prepared comprehensive handoff report in `handoff.md`.

## Artifact Index
- `/workspaces/targetkill/.agents/explorer_campaign/handoff.md` — Comprehensive handoff report
- `/workspaces/targetkill/.agents/explorer_campaign/progress.md` — Liveness heartbeat and task progress
- `/workspaces/targetkill/.agents/explorer_campaign/DISPATCH.md` — Incoming task dispatches
