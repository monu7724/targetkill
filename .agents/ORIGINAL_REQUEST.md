# Original User Request

## 2026-09-06T13:05:45Z

Sector Zero: Lockdown — Build out a 12-Mission Campaign architecture with progressive scaling, focusing specifically on implementing Mission 2 (Infected Dogs) as the immediate milestone.

Working directory: /workspaces/targetkill
Integrity mode: demo

## Requirements

### R1. Campaign Architecture (Workstream A & D)
Refactor the game into a 12-mission structure, where each mission consists of exactly 3 large waves. The wave system must handle multiple enemy groups, different spawn directions, escalating pressure, and varied stationary-FPS objectives. Implement gradual CASH rewards ($500 -> $6,000) granted exactly once upon completion, and update the UI (Mission Select, wave indicators, completion screen).

### R2. Reusable Environment Complexes (Workstream B)
Create 5 major reusable environment complexes (Airport, Railway, Urban, Industrial, Quarantine) using realistic PBR materials, believable scale, and atmospheric lighting (no primitive placeholders). Modify lighting, weather, and dressing to make reused maps feel distinct.

### R3. Mission 2 Implementation (Workstream C)
Focus active development on MISSION 2 — AIRPORT SERVICE ROAD. Primary enemy: Infected Dogs.
- Wave 1: Small dog groups.
- Wave 2: Larger groups + varied spawn directions.
- Wave 3: Largest assault + special final group.
Dogs must have proper skeletal animations (no T-posing or floating limbs), realistic materials, and distinct hit zones (Head, Body). Ensure CC0/commercial-safe assets are used.

### R4. Performance & Android Targeting (Workstream E)
Maintain 720p landscape 60 FPS performance. Avoid unnecessary 4K textures, excessive dynamic lights, or huge particle systems. Modularize scenes to prevent memory leaks and track APK size.

## Acceptance Criteria

### Testing & Validation (Workstream F)
- [ ] Existing regression tests (`godot --headless scenes/test/TestRunner.tscn`) must remain at 44/44 PASSED (or higher with new tests added).
- [ ] `assets_tests/Zombie360Test.tscn` must PASS.
- [ ] New tests created and passing for: wave progression, mission completion, CASH reward logic, mission unlock, and save/load persistence.
- [ ] No duplicate CASH rewards can be claimed on restart.

### Quality Criteria
- [ ] No ripped/copyrighted assets are used.
- [ ] Mission 2 is fully playable, visually validated, and stable before progressing to Mission 3.
- [ ] Mission 1 remains intact and unmodified.

## 2026-09-06T14:14:16Z

# Teamwork Project Prompt — Draft

> Status: Step 9 — Ready for launch — awaiting user approval.
> Goal: Craft prompt → get user approval → delegate to teamwork_preview
> Requested team: Full-scale team (multiple workstreams)

Sector Zero: Lockdown — Full-Scale Mobile Zombie FPS. Expand the existing prototype into a premium, 12-mission tactical stationary 3D shooter with a fully functional economy, upgrades, diverse enemy types, and a polished Android target.

Working directory: `/workspaces/targetkill`
Integrity mode: development

## Requirements

### R1. Campaign & Gameplay Framework
Build a 12-mission campaign with 3 substantial waves per mission. The player is primarily stationary with 360-degree aiming. Implement scalable EnemyBase architecture (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) with clean state-machine AI.

### R2. Weapons, Upgrades & Economy
Implement 10 distinct 3D weapons with upgrade paths (Damage, Magazine, Reload, Accuracy) using a fictional CASH economy. Cash persists across sessions and is earned by completing missions.

### R3. UI/UX & Polish
Create a unified premium dark-tactical UI: Main Menu, Mission Select, Briefings, Gameplay HUD, Mission Complete/Failed screens, Armory, and Settings. Ensure mobile-friendly performance (720p target, controlled lighting).

### R4. Integrity & Legal
Do NOT copy commercial assets or clone proprietary code (e.g., Dead Target). Ensure every external asset is fully documented in `ASSET_LICENSES.md`.

## Acceptance Criteria

### Project Completion
- [ ] All 12 missions exist, each containing 3 substantial waves.
- [ ] Mission progression and save/load systems function correctly.
- [ ] CASH economy and weapon upgrade progression operate seamlessly.
- [ ] 10 unique weapons are implemented (or explicitly documented as unavailable).
- [ ] Distinct enemy variants (including Final Boss) are implemented and functional.
- [ ] The benchmark quality of Mission 1 is preserved and functional.
- [ ] Automated regression test suite completely passes.
- [ ] An ARM64 Android APK can be successfully exported.
- [ ] `ASSET_LICENSES.md` is populated for all external assets.

## 2026-09-06T14:24:14Z

The server restarted and all subagents and background tasks were stopped. Please resume your execution, revive your orchestrator, and restart your monitoring crons to continue working on the Sector Zero: Lockdown project.

## 2026-09-06T14:41:52Z

The user has requested to expedite the execution ("fast work karao"). Please prioritize completing the core gameplay features, resolving the remaining test failures, and moving towards the final integration as quickly as possible. Skip exhaustive non-essential tasks if they are slowing down the critical path.

## 2026-09-06T14:45:33Z

The user has requested to add more agents to the workforce ("aur agent ko work par lagao"). Please scale up your team by spawning additional worker agents to execute the remaining workstreams in parallel and finish the project even faster.

## 2026-09-06T14:57:17Z

The server restarted again and all subagents and background tasks were stopped. Please resume your execution, revive your orchestrator and worker agents, and restart your monitoring crons to continue working on the Sector Zero: Lockdown project at maximum scale.

