# DISPATCH — worker_enemy_ai

**Role**: Enemy AI & Character Specialist
**Working Directory**: `/workspaces/targetkill/.agents/worker_enemy_ai`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`

## Mission Objective
Implement a scalable EnemyBase hierarchy supporting diverse enemy variants (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) with clean state-machine AI, dedicated quadruped Infected Dog implementation for Mission 2, and Boss fight logic.

## Detailed Requirements:
1. **Scalable Enemy Architecture**:
   - `EnemyBase.gd` or unified state-machine supporting AI states: IDLE, CHASE/NAVIGATE, ATTACK, STAGGER, DEAD.
   - Variant parameters for Normal, Fast (sprinter), Heavy (tank), Special (spitter/acid), Dogs (quadruped), Rats (swarm), Bats (airborne), and Boss.
2. **Infected Dog (Mission 2 Focus)**:
   - Dedicated scene `scenes/zombies/InfectedDog.tscn` with quadruped mesh/armature.
   - Dedicated hit zones: `HeadHitZone` (SphereShape3D, 2.5x multiplier, headshot=true) and `BodyHitZone` (BoxShape3D, 1.0x multiplier).
   - Fast quadruped chase AI, biting attack animation/logic, yelping/death reactions.
3. **Boss Zombie**:
   - `scenes/zombies/BossZombie.tscn` (or `ZombieBoss.tscn`): High health pool, ground slam / ranged attack, emits `EventBus.boss_spawned` and `EventBus.boss_health_changed`.
4. **Preservation**:
   - Ensure `Zombie.tscn` and `RealisticZombie.tscn` continue to function without breaking existing regression tests.
5. **Exclusive Write Ownership**:
   - `scenes/zombies/`
   - `scripts/Zombies/`
   - DO NOT edit `scenes/test/TestRunner.gd` or `resources/missions/`.

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification:
- Run: `godot --headless assets_tests/Zombie360Test.tscn`
- Run: `godot --headless -s tools/test_skeletal_zombies_runtime.gd`
- Verify Infected Dog hit zones and headshot multiplier.
- Document commands and results in your `handoff.md`.

## 2026-09-06T15:02:43Z
You are worker_enemy_ai, the Enemy AI & Character Specialist.
Your working directory is `/workspaces/targetkill/.agents/worker_enemy_ai`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: You MUST read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md` before starting work.
Read your full assignment in `/workspaces/targetkill/.agents/worker_enemy_ai/DISPATCH.md`.
Scope: Scalable EnemyBase hierarchy supporting diverse enemy variants (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) with clean state-machine AI, dedicated quadruped Infected Dog implementation (scenes/zombies/InfectedDog.tscn with HeadHitZone 2.5x and BodyHitZone 1.0x), and Boss zombie with EventBus signals. Ensure regression tests pass without breaking.
MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
Keep progress.md updated with your heartbeat. Run test commands to verify your work. When done, write handoff.md in your working directory and notify parent orchestrator via send_message.
