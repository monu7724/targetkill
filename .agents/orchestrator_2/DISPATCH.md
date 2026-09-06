# DISPATCH — 2026-09-06T14:15:10Z

You are the Project Orchestrator (orchestrator_2) for Sector Zero: Lockdown.

Working Directory: `/workspaces/targetkill/.agents/orchestrator_2`
Project Workspace: `/workspaces/targetkill`
Original Request: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` (and `/workspaces/targetkill/ORIGINAL_REQUEST.md`)

## User Request:
Expand the existing prototype into a premium, 12-mission tactical stationary 3D shooter with a fully functional economy, upgrades, diverse enemy types, and a polished Android target.
Integrity mode: development.
Requested team: Full-scale team (multiple workstreams).

### Requirements:
- **R1. Campaign & Gameplay Framework**: Build a 12-mission campaign with 3 substantial waves per mission. Player is primarily stationary with 360-degree aiming. Implement scalable EnemyBase architecture (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) with clean state-machine AI.
- **R2. Weapons, Upgrades & Economy**: Implement 10 distinct 3D weapons with upgrade paths (Damage, Magazine, Reload, Accuracy) using a fictional CASH economy. Cash persists across sessions and is earned by completing missions.
- **R3. UI/UX & Polish**: Create a unified premium dark-tactical UI: Main Menu, Mission Select, Briefings, Gameplay HUD, Mission Complete/Failed screens, Armory, and Settings. Ensure mobile-friendly performance (720p target, controlled lighting).
- **R4. Integrity & Legal**: Do NOT copy commercial assets or clone proprietary code (e.g., Dead Target). Ensure every external asset is fully documented in `ASSET_LICENSES.md`.

### Acceptance Criteria:
- [ ] All 12 missions exist, each containing 3 substantial waves.
- [ ] Mission progression and save/load systems function correctly.
- [ ] CASH economy and weapon upgrade progression operate seamlessly.
- [ ] 10 unique weapons are implemented (or explicitly documented as unavailable).
- [ ] Distinct enemy variants (including Final Boss) are implemented and functional.
- [ ] The benchmark quality of Mission 1 is preserved and functional.
- [ ] Automated regression test suite completely passes.
- [ ] An ARM64 Android APK can be successfully exported.
- [ ] `ASSET_LICENSES.md` is populated for all external assets.

Please decompose the work, dispatch specialists, maintain progress tracking in your `progress.md`, and report back when the project is ready for victory audit.

## 2026-09-06T14:15:21Z
You are the Project Orchestrator (orchestrator_2) for Sector Zero: Lockdown. Your working directory is `/workspaces/targetkill/.agents/orchestrator_2`. The project workspace is `/workspaces/targetkill`. Read your dispatch briefing at `/workspaces/targetkill/.agents/orchestrator_2/DISPATCH.md` and original requirements at `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`. Initialize your BRIEFING.md and progress.md, decompose the tasks across workstreams, dispatch specialists, maintain tight progress logs in your progress.md, and notify the Sentinel when completion is ready for Victory Audit.
