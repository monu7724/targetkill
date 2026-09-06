Enemies AI - Brief

Branch: agent/enemies-ai

Scope
- scripts/Characters/*
- scenes/zombies/*
- scripts/AI/*

Deliverables
- Provide `EnemyBase.gd` FSM stub with states (IDLE, SPAWN, APPROACH, ATTACK_PREPARE, ATTACK, HIT, STAGGER, DEATH).
- Implement unit tests in `tools/test_enemy_variants.gd` that instantiate each archetype and verify state transitions.

Acceptance criteria
- `scripts/AI/EnemyBase.gd` exists and exposes state constants and transition methods.
- Tests assert that heavy damage triggers STAGGER and death triggers DEATH.

Initial tasks
1. Add `scripts/AI/EnemyBase.gd` stub.
2. Add or update `tools/test_enemy_variants.gd` to reference `EnemyBase` where appropriate.
3. Run headless tests.
