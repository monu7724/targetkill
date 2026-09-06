# BRIEFING — 2026-09-06T15:03:00Z

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
- Linear cash reward scaling: $500 -> $6,000 ($500 * mission_number)
- Single-claim bounty enforcement in MissionManager.gd (no duplicate cash rewards on replay)
- 3-wave campaign progression in GameManager.gd with EventBus.wave_started emission
- Create scenes/environments/AirportServiceRoad.tscn for Mission 2
- Mission 1 (mission_01.tres and UrbanStreet.tscn/AirportTerminal.tscn) MUST remain intact and functional
- Exclusive write ownership: resources/missions/mission_*.tres, scripts/MissionData.gd, scripts/MissionManager.gd, scripts/GameManager.gd, scenes/environments/AirportServiceRoad.tscn
- DO NOT edit scenes/test/TestRunner.gd, scenes/player/Player.gd, or scenes/UI/HUD.gd
- DO NOT cheat, fake tests, or create dummy/facade implementations.

## Current Parent
- Conversation ID: c79ae718-8ffc-44d8-a0c8-b2f9295d053f
- Updated: not yet

## Task Summary
- **What to build**: 12 mission resources, 3-wave spawning logic in GameManager.gd, single-claim reward logic in MissionManager.gd, AirportServiceRoad environment scene
- **Success criteria**: All 12 missions load correctly, cash scaling verified, single-claim logic verified, wave progression emits wave_started, AirportServiceRoad.tscn created and valid, regression tests pass
- **Interface contracts**: /workspaces/targetkill/PROJECT.md
- **Code layout**: /workspaces/targetkill/PROJECT.md § Code Layout

## Key Decisions Made
- Initializing workspace and reviewing existing files

## Artifact Index
- /workspaces/targetkill/.agents/worker_campaign/DISPATCH.md — Assignment instructions
- /workspaces/targetkill/.agents/worker_campaign/progress.md — Liveness heartbeat and progress log
- /workspaces/targetkill/.agents/worker_campaign/handoff.md — Final 5-component report

## Change Tracker
- **Files modified**: none yet
- **Build status**: pending initial run
- **Pending issues**: none

## Quality Status
- **Build/test result**: pending
- **Lint status**: clean
- **Tests added/modified**: pending

## Loaded Skills
- None specified in prompt
