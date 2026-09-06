Core Gameplay / Mission Framework - Brief

Branch: agent/core-gameplay

Scope
- scripts/GameManager.gd
- scripts/MissionManager.gd
- resources/missions/*
- scripts/data/WaveData.gd (new)

Deliverables
- Add `WaveData` resource/class representing waves and spawn groups.
- Ensure mission loader can read `WaveData` and emit wave_started/wave_completed signals.
- Add a headless test that loads 3 missions and verifies `wave_count` progression.

Acceptance criteria
- `WaveData.gd` exists and is loadable as a resource.
- Test `scenes/test/TestRunner.tscn` (or a new test) includes a check that `MissionManager` composes waves using `WaveData` entries.

Initial tasks
1. Add `scripts/data/WaveData.gd` resource stub.
2. Add short example `resources/missions/mission_13.tres` sample (if needed) referencing `WaveData`.
3. Run headless tests.
