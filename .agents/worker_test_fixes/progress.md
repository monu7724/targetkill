# Progress — worker_test_fixes

**Last visited**: 2026-09-06T15:07:15Z
**Status**: All regression tests fixed, test suite expanded (54/54 passed), headless tools verified. Ready for handoff.

## Plan & Progress
- [x] 1. Run `godot --headless scenes/test/TestRunner.tscn` to observe current test status and exact failures.
- [x] 2. Examine `scenes/test/TestRunner.gd` around test 5 (Movement) and tests 7 & 10 (3D weapons & Weapon switch).
- [x] 3. Fix hermetic SaveManager isolation in Suite 2 (`unlocked_weapons = ["pistol", "rifle", "shotgun"]` with explicit `save_game()` and player weapon re-init fallback).
- [x] 4. Fix stationary movement test assertion in Suite 2 (test 5) to validate player stationary 360-aim/movement mechanics within stationary boundaries without asserting prohibited free roaming.
- [x] 5. Implement and expand Suite 7 with comprehensive tests covering:
  - 12-mission resource registry (`mission_01` to `mission_12`) & sequential chaining
  - Cash bounty scaling ($500 -> $6,000 in $500 increments)
  - Single-claim bounty enforcement (replaying a completed mission awards $0)
  - No duplicate CASH on save/load restart
  - Mission 2 dog spawner & HitZones Head(2.5x)/Body(1.0x)
  - 12-Mission Sequential Campaign Unlock Progression (M01->M12 unlock gating)
  - Multi-Mission Single-Claim Bounty Isolation (M1+$500 -> M2+$750 -> replay awards $0)
  - 3-Wave Campaign Wave Progression Structure (escalation across waves 1, 2, 3)
  - Wave and Cash EventBus Signal Integration (`wave_started` and `cash_changed`)
- [x] 6. Run and verify all required headless test targets:
  - `godot --headless scenes/test/TestRunner.tscn`: 54 / 54 PASSED (0 failures)
  - `godot --headless assets_tests/Zombie360Test.tscn`: All 5 phases PASS
  - `godot --headless -s scripts/Tools/test_mission1_gameplay.gd`: ALL TESTS PASSED
  - `godot --headless -s tools/test_skeletal_zombies_runtime.gd`: ALL SKELETAL RIG TESTS PASSED
- [x] 7. Document results in `handoff.md` and report to parent orchestrator.
