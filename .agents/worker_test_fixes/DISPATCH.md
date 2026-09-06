# DISPATCH — worker_test_fixes

**Role**: Test Suite & Regression Engineer
**Working Directory**: `/workspaces/targetkill/.agents/worker_test_fixes`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`

## Mission Objective
Fix all current regression test issues in `scenes/test/TestRunner.gd`, ensuring 100% of existing 44 tests pass hermetically, expand the test suite to validate new campaign, economy, wave, and enemy features, and maintain regression safety.

## Detailed Requirements:
1. **Fix Existing `TestRunner.gd` Failures**:
   - Hermetic Save Isolation: In `scenes/test/TestRunner.gd` Suite 2 setup, ensure `SaveManager.data.unlocked_weapons = ["pistol", "rifle", "shotgun"]` before running tests, so tests 7 (`3D weapons`) and 10 (`Weapon switch`) ALWAYS pass regardless of save file state on disk.
   - Stationary Movement: Ensure test 5 (`Movement`) validates player stationary 360-aim/movement mechanics without asserting prohibited free movement or failing when movement constraints are applied.
   - Ensure all 44/44 regression tests pass with `TOTAL: 44 / 44 PASSED` (or higher).
2. **Expand Test Suite (Suite 7+)**:
   - Add tests covering:
     - 12-mission resource registry (`mission_01` to `mission_12`).
     - Cash bounty scaling ($500 -> $6,000 in $500 increments).
     - Single-claim bounty enforcement (replaying a completed mission awards $0).
     - 3-wave campaign progression structure.
3. **Headless Execution Verification**:
   - Run and verify:
     - `godot --headless scenes/test/TestRunner.tscn` (Must achieve >= 44/44 PASSED, ideally 50+/50+).
     - `godot --headless assets_tests/Zombie360Test.tscn` (Must report all 5 phases PASS).
     - `godot --headless -s scripts/Tools/test_mission1_gameplay.gd`.
     - `godot --headless -s tools/test_skeletal_zombies_runtime.gd`.
4. **Exclusive Write Ownership**:
   - `scenes/test/TestRunner.gd`
   - `scenes/test/TestRunner.tscn`
   - New test scripts in `scenes/test/` or `scripts/Tools/`
   - DO NOT edit production environment scenes (`AirportTerminal.tscn`, `UrbanStreet.tscn`) or `resources/missions/`.

## MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Verification:
- Run all test commands and capture the exact summary output.
- Document commands and results in your `handoff.md`.

## 2026-09-06T15:02:43Z
User dispatch received. Scope: Fix existing regression test issues in scenes/test/TestRunner.gd (hermetic SaveManager setup for unlocked weapons so 3D weapons and weapon switch tests always pass, fix stationary movement assertion so stationary mechanics pass cleanly). Ensure 44/44 tests pass. Expand test suite with Suite 7 to test 12 missions, 3 waves, cash scaling, and single-claim bounty enforcement. Verify headless execution of TestRunner.tscn and Zombie360Test.tscn.
