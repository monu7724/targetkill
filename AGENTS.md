AGENTS
======

Purpose: define 10 parallel agent roles for implementing the production roadmap. Each agent receives a clear brief: scope, files/dirs to touch, acceptance criteria, tests to run, and branch naming.

Usage: create a branch per agent (e.g. `agent/core-gameplay`) and open a PR with changes and test results. Run headless tests on each PR.

Agent briefs
------------

1) Core Gameplay / Mission Framework
   - Scope: `scripts/GameManager.gd`, `scripts/MissionManager.gd`, `resources/missions/*`
   - Deliverables: data-driven mission loader, WaveData and SpawnGroup resources, tests ensuring 12 missions load and wave progression signals emit.
   - Branch: `agent/core-gameplay`

2) Enemy Systems & AI
   - Scope: `scripts/Characters/*`, `scenes/zombies/*`, `scripts/AI/*`, `tools/test_*` AI tests
   - Deliverables: `EnemyBase` refactor (if needed), FSM implementation for variants, unit tests for approach/attack/stagger windows.
   - Branch: `agent/enemies-ai`

3) Weapons & Armory
   - Scope: `resources/weapons/*`, `scenes/weapons/*`, `scripts/Weapons/*`, `scripts/Characters/Player.gd`
   - Deliverables: ensure 10 weapons registered, WeaponData resources present or documented unavailable, armory UI hooks, headless tests for equip/switch/fire/reload.
   - Branch: `agent/weapons-armory`

4) Weapon Upgrades & Balancing
   - Scope: `scripts/Weapons/WeaponManager.gd`, `scripts/UpgradeUI.gd`, `resources/weapons/*.tres`
   - Deliverables: upgrade cost formula, save/load integration, tests for purchase flow and level caps.
   - Branch: `agent/weapon-upgrades`

5) Maps & Environment Quality
   - Scope: `scenes/environments/*`, `assets/3d/environments/*`, lighting profiles, `project.godot` settings
   - Deliverables: 5 environment complexes, mobile-friendly lighting presets, scene test previews.
   - Branch: `agent/environments`

6) UI/UX Systems
   - Scope: `scenes/UI/*`, `scripts/UI/*`, `scenes/menu/*`
   - Deliverables: Main Menu, Mission Select, Armory, HUD components, UI tests for navigation and state retention.
   - Branch: `agent/ui-ux`

7) Audio Manager & SFX
   - Scope: `scripts/AudioManager.gd`, `audio/*` integration
   - Deliverables: audio groups, volume settings, event-driven SFX; verify licensed audio entries in `ASSET_LICENSES.md`.
   - Branch: `agent/audio`

8) Android Export & Build Automation
   - Scope: `BUILD.md`, `project.godot`, export templates, CI job
   - Deliverables: reproducible ARM64 export steps, CI workflow to run headless tests and build debug APK (if templates present). Document missing SDK steps.
   - Branch: `agent/android-export`

9) QA & Automated Tests
   - Scope: `scenes/test/*`, `tools/*`, GitHub Actions workflow
   - Deliverables: stable headless Godot CI job, tests executing `scenes/test/TestRunner.tscn`, regression report artifacts.
   - Branch: `agent/qa-tests`

10) Asset Licensing & Legal Audit
    - Scope: `ASSET_LICENSES.md`, `assets/*`, repo history for provenance
    - Deliverables: verified license entries for all external assets, replacement plan for any non-commercial assets, final `ASSET_LICENSES.md` approved for release.
    - Branch: `agent/asset-audit`

Agent brief template (use for each PR description)
- Summary: one-line goal
- Files changed: list
- Tests run: headless output or unit test results
- Acceptance: checkbox list mapping to deliverables

Coordination rules
- Use one branch per agent; do not merge until PR passes headless tests.
- Lock ownership for scene files to a single agent when editing (document in PR). Use small, focused patches.
- Central integrator (human or `agent/qa-tests`) will perform final integration and resolve conflicts.

If you approve, I will create per-agent branch briefs (this file is the canonical brief) and start with the top three agents: `core-gameplay`, `enemies-ai`, and `weapons-armory`.
