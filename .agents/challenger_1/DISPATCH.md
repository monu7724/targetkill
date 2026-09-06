# DISPATCH — challenger_1

**Role**: Adversarial Correctness Challenger 1
**Working Directory**: `/workspaces/targetkill/.agents/challenger_1`
**Project Workspace**: `/workspaces/targetkill`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`

## Challenge Objective
Empirically stress-test the implementation against adversarial edge cases and user constraints.

## Challenge Focus:
1. **Adversarial Single-Claim Bounty Test**:
   - Write and execute a test script that completes a mission multiple times sequentially (first clear, then 3 replays).
   - Verify that cash balance increases ONLY on the first clear, and stays unchanged (0 duplicate cash) on all subsequent replays.
   - Verify persistence across save file reload.
2. **Adversarial Weapon Upgrades & Economy Test**:
   - Write and execute a test script verifying that purchasing upgrades properly deducts cash, upgrades all 4 stats (Damage, Magazine, Reload, Accuracy), caps out at max level without allowing negative cash or exceeding level limits, and calculates costs progressively ($200 to $3,000).
3. **12-Mission Registry & Wave Progression Stress Test**:
   - Verify all 12 missions exist, have valid 3-wave arrays, unlock sequentially, and emit `EventBus.wave_started(current_wave, total_waves)` on wave advancement.
4. **Infected Dog Combat & HitZone Accuracy**:
   - Verify `scenes/zombies/InfectedDog.tscn` has dedicated HeadHitZone (2.5x multiplier) and BodyHitZone (1.0x multiplier), and receives damage correctly.
5. **Headless Regression Baseline**:
   - Run: `godot --headless scenes/test/TestRunner.tscn` (54/54 pass)
   - Run: `godot --headless assets_tests/Zombie360Test.tscn`

Deliver your verdict (`APPROVE` or `REQUEST_CHANGES`) with full rationale in `/workspaces/targetkill/.agents/challenger_1/handoff.md` and notify orchestrator_3.

## 2026-09-06T15:15:51Z
You are challenger_1, Adversarial Correctness Challenger.
Your working directory is `/workspaces/targetkill/.agents/challenger_1`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: Read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md`.
Read your full assignment in `/workspaces/targetkill/.agents/challenger_1/DISPATCH.md`.
Empirically stress-test:
1. Single-claim bounty enforcement: test 5 sequential completions of a mission (verify cash increases only on clear 1, +$0 on replays 2-5).
2. Weapon upgrades and economy: test cash deduction, all 4 stats (Damage, Mag, Reload, Accuracy), cost scaling ($200 to $3,000), and max level clamping.
3. 12-mission registry and 3-wave progression.
4. Infected Dog HeadHitZone (2.5x) vs BodyHitZone (1.0x).
5. Headless regression suite (54/54 pass).
Deliver your verdict (APPROVE or REQUEST_CHANGES) with empirical evidence in `/workspaces/targetkill/.agents/challenger_1/handoff.md` and notify orchestrator_3 via send_message.

