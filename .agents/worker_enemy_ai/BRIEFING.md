# BRIEFING — 2026-09-06T15:03:00Z

## Mission
Implement scalable EnemyBase hierarchy supporting diverse enemy variants (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) with clean state-machine AI, dedicated quadruped Infected Dog implementation (scenes/zombies/InfectedDog.tscn with HeadHitZone 2.5x and BodyHitZone 1.0x), and Boss zombie with EventBus signals, while keeping existing regression tests passing.

## 🔒 My Identity
- Archetype: worker_enemy_ai
- Roles: implementer, qa, specialist
- Working directory: /workspaces/targetkill/.agents/worker_enemy_ai
- Original parent: c79ae718-8ffc-44d8-a0c8-b2f9295d053f
- Milestone: M3 / Enemy AI & Character Specialization

## 🔒 Key Constraints
- DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent intended tasks.
- Ensure regression tests pass without breaking (TestRunner 50/50, Zombie360Test, test_skeletal_zombies_runtime).
- Exclusive Write Ownership: scenes/zombies/, scripts/Zombies/ (and enemy AI scripts). DO NOT edit scenes/test/TestRunner.gd or resources/missions/.
- Keep progress.md updated with heartbeat.

## Current Parent
- Conversation ID: c79ae718-8ffc-44d8-a0c8-b2f9295d053f
- Updated: 2026-09-06T15:03:00Z

## Task Summary
- **What to build**: Scalable EnemyBase hierarchy, state-machine AI (IDLE, CHASE/NAVIGATE, ATTACK, STAGGER, DEAD), variant parameters (Normal, Fast, Heavy, Special/spitter, Dogs, Rats, Bats, Boss), dedicated quadruped Infected Dog scene `scenes/zombies/InfectedDog.tscn` (with HeadHitZone 2.5x and BodyHitZone 1.0x), Boss zombie with EventBus signals (`boss_spawned`, `boss_health_changed`), ensure backward compatibility with `Zombie.tscn`.
- **Success criteria**: All tests pass genuine execution, clean architecture, proper hitzones and animations.
- **Interface contracts**: PROJECT.md § Interface Contracts
- **Code layout**: PROJECT.md § Code Layout

## Key Decisions Made
- Inspect existing Zombie.gd and scenes before modifying or extending.
- Maintain full compatibility with Zombie.tscn while establishing clean EnemyBase hierarchy.

## Change Tracker
- **Files modified**: None yet
- **Build status**: Baseline passing (50/50 TestRunner, 15/15 InfectedDogTest, Zombie360Test, test_skeletal_zombies_runtime)
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pass
- **Lint status**: Clean
- **Tests added/modified**: None yet

## Loaded Skills
None loaded.

## Artifact Index
- /workspaces/targetkill/scenes/zombies/Zombie.tscn — Existing zombie scene
- /workspaces/targetkill/scenes/zombies/Zombie.gd — Current zombie implementation
