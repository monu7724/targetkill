# BRIEFING — 2026-09-06T13:15:30Z

## Mission
Implement Milestone 1 (Campaign Architecture, Wave Engine & Reward Integrity) for Sector Zero: Lockdown.

## 🔒 My Identity
- Archetype: worker
- Roles: [implementer, qa, specialist]
- Working directory: /workspaces/targetkill/.agents/worker_m1
- Original parent: 99c0ac96-a596-4724-a7a2-034957bdda66
- Milestone: M1 (Campaign Architecture, Wave Engine & Reward Integrity)

## 🔒 Key Constraints
- DO NOT CHEAT: All implementations genuine, no hardcoded test results or dummy facades.
- DO NOT touch scenes/environments/UrbanStreet.tscn or scenes/environments/AirportTerminal.tscn (Mission 1 must remain 100% intact).
- Write ownership: resources/missions/ (mission_01.tres - mission_12.tres), scripts/MissionData.gd, scripts/MissionManager.gd, scripts/SaveManager.gd, scripts/GameManager.gd, scripts/MissionSelectUI.gd, scenes/UI/HUD.gd, scripts/ResultUI.gd.
- Linear cash rewards: $500 -> $6,000 in $500 increments for missions 1 to 12.
- Single-claim cash reward enforcement: Replaying a completed mission yields $0 bounty.
- 3 large waves per mission with directional groups in GameManager.gd.
- HUD wave indicator synced via EventBus.wave_started.
- MissionSelectUI expanded to display all 12 missions.
- Headless test verification: scenes/test/TestRunner.tscn (>= 44/44), assets_tests/Zombie360Test.tscn (5/5), scripts/Tools/test_mission1_gameplay.gd.

## Current Parent
- Conversation ID: 99c0ac96-a596-4724-a7a2-034957bdda66
- Updated: not yet

## Task Summary
- **What to build**: 12 mission resources with linear cash rewards, single-claim reward enforcement, 3-wave spawning engine with directional support and HUD sync, and 12-mission selection UI.
- **Success criteria**: All regression tests pass (>= 44/44), Zombie360Test passes, test_mission1_gameplay passes, cash scaling is exact ($500-$6000), replay grants $0 cash, wave indicator displays WAVE X / 3.
- **Interface contracts**: PROJECT.md § Interface Contracts
- **Code layout**: PROJECT.md § Code Layout

## Key Decisions Made
- [Initial]: Follow spec miner and campaign explorer findings; structure waves in MissionData as Array[Dictionary]; preserve procedural fallback in GameManager if mission waves are empty to guarantee Mission 1 compatibility.

## Artifact Index
- /workspaces/targetkill/.agents/worker_m1/DISPATCH.md — Assignment instructions
- /workspaces/targetkill/.agents/worker_m1/BRIEFING.md — Working memory & status
- /workspaces/targetkill/.agents/worker_m1/progress.md — Liveness & progress tracker
- /workspaces/targetkill/.agents/worker_m1/handoff.md — Final completion handoff

## Change Tracker
- **Files modified**: None yet
- **Build status**: Untested
- **Pending issues**: None

## Quality Status
- **Build/test result**: Baseline 44/44 expected
- **Lint status**: Clean
- **Tests added/modified**: TBD

## Loaded Skills
- None
