# BRIEFING — 2026-09-06T15:15:00Z

## Mission
Implement 12-mission campaign framework with structured 3-wave progression, gradual cash reward scaling ($500 -> $6,000), single-claim bounty enforcement, and Airport Service Road environment for Mission 2.

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa, specialist
- Working directory: /workspaces/targetkill/.agents/worker_campaign
- Original parent: c79ae718-8ffc-44d8-a0c8-b2f9295d053f
- Milestone: M1 & M2 (Campaign Framework & AirportServiceRoad)

## 🔒 Key Constraints
- Scope: 12 missions (mission_01.tres through mission_12.tres in resources/missions/)
- Linear cash reward scaling: $500 -> $6,000 ($500 * mission_number curve)
- Single-claim bounty enforcement in MissionManager.gd (no duplicate cash rewards on replay)
- 3-wave campaign progression in GameManager.gd with EventBus.wave_started emission
- Create scenes/environments/AirportServiceRoad.tscn for Mission 2
- Mission 1 (mission_01.tres and UrbanStreet.tscn/AirportTerminal.tscn) MUST remain intact and functional
- Exclusive write ownership: resources/missions/mission_*.tres, scripts/MissionData.gd, scripts/MissionManager.gd, scripts/GameManager.gd, scenes/environments/AirportServiceRoad.tscn
- DO NOT edit scenes/test/TestRunner.gd, scenes/player/Player.gd, or scenes/UI/HUD.gd
- DO NOT cheat, fake tests, or create dummy/facade implementations.

## Current Parent
- Conversation ID: c79ae718-8ffc-44d8-a0c8-b2f9295d053f
- Updated: 2026-09-06T15:13:45Z

## Task Summary
- **What to build**: 12 mission resources with structured 3 waves, 3-wave spawning logic in GameManager.gd with EventBus.wave_started, single-claim bounty enforcement in MissionManager.gd, AirportServiceRoad environment scene for Mission 2
- **Success criteria**: 12 missions loaded and valid, cash scaling verified, single-claim logic verified, wave progression emits wave_started, AirportServiceRoad.tscn created and valid, regression tests 54/54 pass
- **Interface contracts**: /workspaces/targetkill/PROJECT.md
- **Code layout**: /workspaces/targetkill/PROJECT.md § Code Layout

## Key Decisions Made
- Implemented structured 3 waves in all 12 mission resources (`waves: Array[Dictionary]`) with directional spawning groups.
- Mission 2 configured with 3 escalating waves of infected dogs: Wave 1 (6 dogs front), Wave 2 (12 dogs across 3 directions), Wave 3 (14 dogs across 3 directions), totaling 32 dogs.
- Created `AirportServiceRoad.tscn` using tarmac asphalt material, jersey barriers, hazard barrels, cones, airport terminal hangar section, directional lighting, and 6 cardinal spawn points.
- Refactored `finish_mission()` in `MissionManager.gd` to strictly enforce single-claim bounty rewards (`bounty_awarded = 0` and no cash addition on replays).
- Refactored `GameManager.gd` to emit `EventBus.wave_started.emit(current_wave, total_waves)` on wave initiation, support structured wave group spawning, and fallback gracefully to procedural 3 waves.

## Artifact Index
- /workspaces/targetkill/.agents/worker_campaign/DISPATCH.md — Assignment instructions
- /workspaces/targetkill/.agents/worker_campaign/progress.md — Liveness heartbeat and progress log
- /workspaces/targetkill/.agents/worker_campaign/handoff.md — Final 5-component report
- /workspaces/targetkill/tools/test_campaign_worker.gd — Dedicated verification test suite

## Change Tracker
- **Files modified**:
  - `resources/missions/mission_01.tres` through `mission_12.tres`: 12 campaign mission resources with 3-wave configs, linear cash scaling, sequential unlock chaining
  - `scenes/environments/AirportServiceRoad.tscn`: Mission 2 environment with tarmac, barriers, hangars, and 6 spawn points
  - `scripts/MissionManager.gd`: Single-claim cash bounty enforcement
  - `scripts/GameManager.gd`: 3-wave structured spawning engine and EventBus.wave_started emission
  - `tools/test_campaign_worker.gd`: Campaign verification suite
- **Build status**: PASS (54/54 in TestRunner.tscn, 6/6 in test_campaign_worker.gd, 15/15 in InfectedDogTest.tscn, 100% in test_mission1_gameplay.gd)
- **Pending issues**: none

## Quality Status
- **Build/test result**: PASS across all suites
- **Lint status**: clean
- **Tests added/modified**: `tools/test_campaign_worker.gd` (6/6 tests covering all dispatch acceptance criteria)

## Loaded Skills
- none
