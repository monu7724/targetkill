# DISPATCH — challenger_2

**Role**: Adversarial Correctness Challenger 2
**Working Directory**: `/workspaces/targetkill/.agents/challenger_2`
**Project Workspace**: `/workspaces/targetkill`
**Original Request**: `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md`
**Scope Document**: `/workspaces/targetkill/PROJECT.md`

## Challenge Objective
Empirically stress-test the implementation against adversarial edge cases, boundary conditions, and performance requirements.

## Challenge Focus:
1. **Adversarial Wave Engine & Director Stress Test**:
   - Verify that `scripts/GameManager.gd` accurately respects 3 substantial waves across diverse mission configs.
   - Verify enemy scaling across waves (Wave 1 initial, Wave 2 escalation, Wave 3 climactic assault) and that clearing wave 3 finishes the mission.
2. **Stationary FPS Movement Constraints Stress Test**:
   - Verify player stationary bounds: player cannot freely roam around the map, yet has full 360-degree rotation and touch aim pitch.
3. **Enemy Variant Hierarchy Stress Test**:
   - Verify all 8 variants (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) instantiate cleanly without missing mesh, material, or script errors.
   - Verify Boss zombie emits `boss_spawned` and `boss_health_changed`.
4. **Android APK & License Audit**:
   - Verify `SectorZero-Lockdown-arm64.apk` is a valid Android package with ARM64 binary and `com.targetzero.lockdown` ID.
   - Verify `ASSET_LICENSES.md` covers all external and generated assets with 100% CC0/MIT provenance.
5. **Headless Regression Baseline**:
   - Run: `godot --headless scenes/test/TestRunner.tscn` (54/54 pass)
   - Run: `godot --headless assets_tests/Zombie360Test.tscn`

Deliver your verdict (`APPROVE` or `REQUEST_CHANGES`) with full rationale in `/workspaces/targetkill/.agents/challenger_2/handoff.md` and notify orchestrator_3.

## 2026-09-06T15:15:51Z
You are challenger_2, Adversarial Correctness Challenger.
Your working directory is `/workspaces/targetkill/.agents/challenger_2`.
Your project workspace is `/workspaces/targetkill`.
MANDATORY: Read `/workspaces/targetkill/.agents/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/PROJECT.md`.
Read your full assignment in `/workspaces/targetkill/.agents/challenger_2/DISPATCH.md`.
Empirically stress-test:
1. Wave engine & Director: 3 substantial waves, escalation curve, wave 3 clear condition.
2. Stationary FPS movement bounds vs 360-aim rotation.
3. Enemy variants hierarchy (all 8 variants) & Boss signals (`boss_spawned`, `boss_health_changed`).
4. Android ARM64 APK verification (`SectorZero-Lockdown-arm64.apk` package badging) and ASSET_LICENSES.md audit.
5. Headless regression suite (54/54 pass).
Deliver your verdict (APPROVE or REQUEST_CHANGES) with empirical evidence in `/workspaces/targetkill/.agents/challenger_2/handoff.md` and notify orchestrator_3 via send_message.

