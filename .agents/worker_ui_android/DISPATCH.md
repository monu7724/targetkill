# DISPATCH — worker_ui_android

**Role**: UI/UX & Android Platform Specialist
**Working Directory**: `/workspaces/targetkill/.agents/worker_ui_android`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`

## Mission Objective
Deliver a unified dark-tactical UI across all game screens (Main Menu, 12-Mission Select, Gameplay HUD, ResultUI, Armory, Settings), configure Android ARM64 export, and ensure complete legal compliance in `ASSET_LICENSES.md`.

## Detailed Requirements:
1. **Unified Dark-Tactical UI Screens**:
   - `MainMenu.tscn`: 'Sector Zero: Lockdown' branding, sleek military HUD theme, buttons for Campaign, Armory, Settings.
   - `MissionSelectUI.tscn` / `MissionSelectUI.gd`: Display grid of all 12 missions with tactical briefings, difficulty/threat ratings, single-claim cash rewards, and unlocked/locked/completed states.
   - `HUD.tscn` / `HUD.gd`: Wave indicator `WAVE: X / 3` connected to `EventBus.wave_started`, Boss health bar connected to `EventBus.boss_health_changed`, responsive touch controls (fire, reload, switch, pause), reticle, hitmarker.
   - `ArmoryUI.tscn` / `ArmoryUI.gd`: Clean tactical weapon selection, weapon stats display, upgrade purchase buttons for Damage, Magazine, Reload, Accuracy, and persistent cash display.
   - `ResultUI.tscn` / `ResultUI.gd`: Mission clear/failed display, stats (kills, headshots, accuracy), single-claim bounty awarded (shows $0 if mission was replayed).
2. **Android ARM64 Export**:
   - Configure `export_presets.cfg`:
     - Android platform preset.
     - Package format: ARM64-v8a.
     - Min SDK: 24 (Android 7.0), Target SDK: 34 (Android 14).
     - Package name: `com.targetzero.lockdown`.
     - Version: 1.0.0 (Code 1).
3. **Legal Compliance (`ASSET_LICENSES.md`)**:
   - Fully document all external assets and procedural generators (Poly Haven PBR textures, Vitruvian humanoid model, CC0 city props, procedural meshes/audio, 3D weapons, dog rig).
   - Ensure 100% CC0 / MIT compliance with zero proprietary or cloned assets.
4. **Exclusive Write Ownership**:
   - `scenes/UI/`
   - `scenes/menu/`
   - `export_presets.cfg`
   - `ASSET_LICENSES.md`
   - DO NOT edit `scenes/test/TestRunner.gd` or `resources/missions/`.

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification:
- Verify UI scenes load without headless errors.
- Validate `export_presets.cfg` syntax and configuration.
- Verify `ASSET_LICENSES.md` covers all assets.
- Document commands and results in your `handoff.md`.

## 2026-09-06T15:02:43Z
You are worker_ui_android, the UI/UX & Android Platform Specialist.
Your working directory is `/workspaces/targetkill/.agents/worker_ui_android`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: You MUST read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md` before starting work.
Read your full assignment in `/workspaces/targetkill/.agents/worker_ui_android/DISPATCH.md`.
Scope: Deliver unified dark-tactical UI across MainMenu.tscn (branding), MissionSelectUI.tscn (12 missions grid + briefings), HUD.tscn (wave indicator WAVE: X / 3, boss bar, touch controls), ArmoryUI.tscn (10 weapons + upgrades), and ResultUI.tscn (stats + single-claim bounty). Configure export_presets.cfg for Android ARM64 export (SDK 24-34, com.targetzero.lockdown). Update ASSET_LICENSES.md for complete legal coverage.
MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
Keep progress.md updated with your heartbeat. Run test commands to verify your work. When done, write handoff.md in your working directory and notify parent orchestrator via send_message.
