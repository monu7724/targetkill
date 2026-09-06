# BRIEFING — 2026-09-06T13:12:30Z

## Mission
Probe and document the authoritative specification of the test harness, existing regression test suite, headless Godot runner, Zombie360Test, and save/progression systems for Sector Zero: Lockdown.

## 🔒 My Identity
- Archetype: specification_miner
- Roles: Test Harness & Regression Suite Specialist
- Working directory: /workspaces/targetkill/.agents/spec_miner_survey
- Original parent: 99c0ac96-a596-4724-a7a2-034957bdda66
- Milestone: Survey existing test harness, regression suite, headless runners, and persistence/reward specifications

## 🔒 Key Constraints
- Read-only investigation: do NOT implement anything.
- Probe authoritative sources (codebase, test runner scenes/scripts, test cases, Godot CLI invocation).
- Report findings in 5-component handoff report (\`handoff.md\`) with Features Discovered and Edge Cases tables.
- All workspace writes restricted to \`.agents/spec_miner_survey/\`.

## Current Parent
- Conversation ID: 99c0ac96-a596-4724-a7a2-034957bdda66
- Updated: 2026-09-06T13:12:30Z

## Task Summary
- **What to build**: Specification mining report for test harness, 44+ existing tests, Zombie360Test, headless runner, and reward/persistence architecture.
- **Success criteria**: Exhaustive enumeration of all existing test cases, runner mechanics, headless execution command/exit codes, assets test behavior, and precise integration recommendations for 12-mission campaign tests.
- **Interface contracts**: \`scenes/test/TestRunner.tscn\`, \`assets_tests/Zombie360Test.tscn\`, \`scripts/SaveManager.gd\`, \`scripts/GameManager.gd\`
- **Code layout**: \`scenes/test/\`, \`assets_tests/\`, \`scripts/\`

## Key Decisions Made
- Confirmed Godot 4.5.1 stable at \`/usr/local/bin/godot\` executes headless tests cleanly.
- Diagnosed state coupling between \`Player.gd\` and user save file on disk (\`user://savegame.json\`), and verified 44/44 test pass condition.
- Verified \`Zombie360Test.tscn\` 5-phase automated audit passes completely.
- Formulated concrete recommendations for single-claim CASH bounty enforcement and 12-mission campaign test integration.

## Artifact Index
- \`/workspaces/targetkill/.agents/spec_miner_survey/handoff.md\` — Complete 5-component handoff report
- \`/workspaces/targetkill/.agents/spec_miner_survey/progress.md\` — Progress tracker
- \`/workspaces/targetkill/.agents/spec_miner_survey/DISPATCH.md\` — Task assignment log
