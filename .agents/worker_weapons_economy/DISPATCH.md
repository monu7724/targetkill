# DISPATCH — worker_weapons_economy

**Role**: Weapons & Economy Specialist
**Working Directory**: `/workspaces/targetkill/.agents/worker_weapons_economy`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`

## Mission Objective
Implement 10 distinct 3D weapons with 4 upgrade paths (Damage, Magazine, Reload, Accuracy), connected to a persistent fictional CASH economy.

## Detailed Requirements:
1. **10 Distinct Weapons**:
   - Implement weapon definitions / scenes in `scenes/weapons/` or `resources/weapons/`:
     1. `usp45` (Tactical Pistol)
     2. `m4a1` (Assault Rifle)
     3. `remington870` (Pump Shotgun)
     4. `ak47` (Combat Rifle)
     5. `desert_eagle` (Heavy Handgun)
     6. `mp5` (Submachine Gun)
     7. `awp` (Sniper Rifle)
     8. `combat_knife` (Melee Weapon)
     9. `crossbow` (Tactical Special)
     10. `grenade_launcher` (Heavy Explosive / Special)
   - Each weapon must have distinct stats: damage, fire_rate, mag_size, reload_time, accuracy/spread, and audio/visual setup.
2. **4 Upgrade Paths**:
   - Damage, Magazine Size, Reload Speed, Accuracy.
   - 4-5 upgrade levels per stat with progressive costs ($200 to $3,000).
   - Stats must scale properly when upgraded.
3. **Economy & Save Integration**:
   - Ensure weapon unlock states and upgrade levels persist in `SaveManager.gd`.
   - Provide helper methods or a `WeaponManager.gd` / registry for querying weapon data and purchasing upgrades with in-game cash.
4. **Exclusive Write Ownership**:
   - `scenes/weapons/`
   - `resources/weapons/`
   - `scripts/Weapons/`
   - DO NOT edit `scenes/test/TestRunner.gd` or `resources/missions/`.

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification:
- Test weapon instantiation, shooting, and upgrade calculations.
- Document commands and results in your `handoff.md`.

## 2026-09-06T15:02:43Z
You are worker_weapons_economy, the Weapons & Economy Specialist.
Your working directory is `/workspaces/targetkill/.agents/worker_weapons_economy`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: You MUST read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md` before starting work.
Read your full assignment in `/workspaces/targetkill/.agents/worker_weapons_economy/DISPATCH.md`.
Scope: Implement 10 distinct 3D weapons (USP-45, M4A1, Remington 870, AK-47, Desert Eagle, MP5, AWP, Combat Knife, Crossbow, Grenade Launcher) with 4 upgrade paths (Damage, Magazine, Reload, Accuracy), upgrade cost curves, and persistent cash economy integration.
MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
Keep progress.md updated with your heartbeat. Run test commands to verify your work. When done, write handoff.md in your working directory and notify parent orchestrator via send_message.

