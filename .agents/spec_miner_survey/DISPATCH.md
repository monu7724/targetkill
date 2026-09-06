# DISPATCH — Spec Miner: Test Harness & Regression Suite

## Objective
Thoroughly explore and document the test infrastructure and existing regression tests in `/workspaces/targetkill`.

## Scope & Tasks
1. Read `/workspaces/targetkill/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/GEMINI.md`.
2. Inspect the existing test runner (`scenes/test/TestRunner.tscn` and corresponding scripts).
3. Enumerate all 44 (or more) existing test cases across test files (e.g., in `scenes/test/` or wherever test scripts reside). List every test name, what it verifies, and its current pass/fail mechanism.
4. Inspect `assets_tests/Zombie360Test.tscn` and its requirements.
5. Inspect `SaveManager`, cash reward logic, progression systems, mission unlock logic, and tutorial state tracking.
6. Identify headless Godot execution commands and environment requirements (`godot --headless ...`).
7. Recommend how new tests for waves, mission completion, single-claim cash reward ($500 -> $6,000), unlocks, and save/load persistence should be structured to seamlessly integrate with `TestRunner.tscn`.

## Output Requirements
Write your comprehensive report to `/workspaces/targetkill/.agents/spec_miner_survey/handoff.md`.
Report back when done with your key findings and handoff path.

## 2026-09-06T13:06:59Z
You are the Test Harness Spec Miner.
Your working directory is /workspaces/targetkill/.agents/spec_miner_survey/.
Read /workspaces/targetkill/ORIGINAL_REQUEST.md, /workspaces/targetkill/GEMINI.md, and /workspaces/targetkill/.agents/spec_miner_survey/DISPATCH.md.
Investigate the existing test suite, scenes/test/TestRunner.tscn, all test scripts, how Godot runs tests headlessly, the 44 existing tests, assets_tests/Zombie360Test.tscn, and save/load/reward systems.
Write your findings to /workspaces/targetkill/.agents/spec_miner_survey/handoff.md.
When done, send a message to orchestrator with your summary and handoff path.
