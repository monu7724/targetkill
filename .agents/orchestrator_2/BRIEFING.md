# BRIEFING — 2026-09-06T14:16:30Z

## Mission
Orchestrate the full-scale expansion of Sector Zero: Lockdown into a 12-mission tactical stationary 3D shooter with 10 weapons, full cash economy/upgrades, scalable enemy hierarchy (including Boss), dark-tactical UI/UX, and exportable Android APK.

## 🔒 My Identity
- Archetype: orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: /workspaces/targetkill/.agents/orchestrator_2
- Original parent: parent
- Original parent conversation ID: 3392fafd-488f-494c-8e29-f1dea390ac0c

## 🔒 My Workflow
- **Pattern**: Project
- **Scope document**: /workspaces/targetkill/PROJECT.md
1. **Decompose**: Decompose full-scale 12-mission campaign, 10 weapons & economy, enemy variants & boss, UI/UX polish, and Android export into verifiable milestones.
2. **Dispatch & Execute** (pick ONE):
   - **Direct (iteration loop)**: Explorer -> Worker -> Reviewer -> Challenger -> Forensic Auditor -> Gate.
   - **Delegate (sub-orchestrator)**: Delegate independent milestones to sub-orchestrators or specialists.
3. **On failure** (in this order):
   - Retry: nudge stuck agent or re-send task
   - Replace: spawn fresh agent with partial progress
   - Skip: proceed without (only if non-critical)
   - Redistribute: split stuck agent's remaining work
   - Redesign: re-partition decomposition
   - Escalate: report to parent (sub-orchestrators only, last resort)
4. **Succession**: Self-succeed at 16 spawns: write handoff.md, cancel crons, spawn successor.
- **Work items**:
  1. Survey & Codebase Baseline Assessment [in-progress]
  2. Campaign Architecture & 12 Missions (3 Waves each) [pending]
  3. Weapons (10 weapons), Cash Economy & Upgrades [pending]
  4. Scalable EnemyBase & Variant AI (Normal, Fast, Heavy, Special, Dogs, Rats, Bats, Boss) [pending]
  5. UI/UX Polish (Dark Tactical UI, Main Menu, Armory, HUD, Mission Select) [pending]
  6. Android Export & Verification (ARM64 APK, Performance, Asset Licenses) [pending]
  7. Automated Regression & Victory Audit [pending]
- **Current phase**: 0 (Survey)
- **Current focus**: Surveying current state of weapons, campaign, enemies, economy, and test suite

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- NEVER investigate or explore the problem at the code level — dispatch Explorers for technical investigation.
- You MAY use file-editing tools ONLY for metadata/state files (.md) in your .agents/ folder.
- DO NOT CHEAT. All implementations must be genuine.
- Forensic Auditor INTEGRITY VIOLATION is a non-negotiable binary veto.
- Never reuse a subagent after it has delivered its handoff — always spawn fresh.

## Current Parent
- Conversation ID: 3392fafd-488f-494c-8e29-f1dea390ac0c
- Updated: 2026-09-06T14:15:21Z

## Key Decisions Made
- Initiated Project Pattern orchestration for full-scale 12-mission expansion.
- Dispatched 3 specialized exploration agents for comprehensive Survey phase.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|

## Succession Status
- Succession required: no
- Spawn count: 0 / 16
- Pending subagents: none
- Predecessor: orchestrator_1
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: not started
- Safety timer: none
- On succession: kill all timers before spawning successor
- On context truncation: run `manage_task(Action="list")` — re-create if missing

## Artifact Index
- /workspaces/targetkill/.agents/orchestrator_2/DISPATCH.md — Project Orchestrator dispatch assignment
- /workspaces/targetkill/.agents/orchestrator_2/progress.md — Liveness heartbeat and milestone tracking
- /workspaces/targetkill/.agents/ORIGINAL_REQUEST.md — Authoritative user requirements
- /workspaces/targetkill/PROJECT.md — Global project specification and architecture
