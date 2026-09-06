# DISPATCH — E2E Test Writer: Test Infra & Campaign Test Suite

## Objective
Design and implement the E2E Testing Track artifacts for Sector Zero: Lockdown 12-Mission Campaign and Mission 2.
Publish `/workspaces/targetkill/TEST_INFRA.md` and `/workspaces/targetkill/TEST_READY.md`.

## Context & Inputs
- Read `/workspaces/targetkill/ORIGINAL_REQUEST.md` (mandatory).
- Read `/workspaces/targetkill/PROJECT.md`.
- Read `/workspaces/targetkill/.agents/spec_miner_survey/handoff.md`.
- Read `/workspaces/targetkill/.agents/explorer_campaign/handoff.md`.

## Tasks
1. **Hermetic Test Harness Decoupling**:
   - In `scenes/test/TestRunner.gd`, ensure test setup initializes `SaveManager.data.unlocked_weapons = ["pistol", "rifle", "shotgun"]` so tests 1-44 pass hermetically regardless of host save files.
2. **Add Test Suite 7 (Campaign Architecture & Waves)**:
   Implement tests 45–50+ in `scenes/test/TestRunner.gd`:
   - Test 45: `12-Mission Registry & Chaining` (verifies all 12 mission `.tres` resources load, valid IDs, sequential unlock chaining).
   - Test 46: `Gradual Cash Rewards ($500 -> $6,000)` (verifies monotonic linear scaling $500 -> $6,000 across missions 1-12).
   - Test 47: `3-Wave Structure` (verifies all missions have `wave_count == 3`).
   - Test 48: `Single-Claim CASH Reward Logic` (reset cash, complete mission -> cash increases by reward; re-complete same mission -> cash does NOT increase).
   - Test 49: `No Duplicate CASH on Save/Load Restart` (save game, reload -> cash stays identical, cannot re-claim).
   - Test 50: `Mission 2 Dog Spawner & Hit Zones` (verifies Mission 2 configuration for infected dogs and hit zones).
3. **Execute & Verify**:
   - Run `godot --headless scenes/test/TestRunner.tscn`. Verify output passes with exit code 0.
   - Run `godot --headless assets_tests/Zombie360Test.tscn`. Verify output passes with exit code 0.
4. **Publish Documentation**:
   - Create `/workspaces/targetkill/TEST_INFRA.md` according to the template in `PROJECT.md` / Project Pattern.
   - Create `/workspaces/targetkill/TEST_READY.md` summarizing runner commands, tier counts, and feature checklist.

## Output Requirements
Write your detailed report to `/workspaces/targetkill/.agents/test_writer_e2e/handoff.md`.
Report back via message when `TEST_READY.md` is published and test runner passes.

## 2026-09-06T13:14:39Z
You are the E2E Test Writer.
Your working directory is /workspaces/targetkill/.agents/test_writer_e2e/.
Read /workspaces/targetkill/ORIGINAL_REQUEST.md (mandatory), /workspaces/targetkill/PROJECT.md, /workspaces/targetkill/.agents/spec_miner_survey/handoff.md, and /workspaces/targetkill/.agents/test_writer_e2e/DISPATCH.md.
Follow your tasks to decouple TestRunner setup from user saves, implement tests 45-50+ in scenes/test/TestRunner.gd, create TEST_INFRA.md and TEST_READY.md.
Verify with godot --headless scenes/test/TestRunner.tscn and Zombie360Test.tscn.
Write your handoff to /workspaces/targetkill/.agents/test_writer_e2e/handoff.md and notify orchestrator when done.

