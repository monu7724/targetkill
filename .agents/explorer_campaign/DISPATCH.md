# DISPATCH — Explorer: Campaign Architecture & Wave System

## Objective
Investigate the current campaign, mission, wave, HUD, UI, and progression architectures in `/workspaces/targetkill`.

## Scope & Tasks
1. Read `/workspaces/targetkill/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/GEMINI.md`.
2. Map out how missions are currently represented (scenes, resources, scripts, `MainMenu.tscn`, `MissionSelect`, `UrbanStreet.tscn`, etc.).
3. Analyze how waves, enemy spawning, stationary-FPS objectives, and wave progression currently work (or if waves need a unified system).
4. Analyze how cash rewards ($500 to $6,000 across 12 missions) are currently granted or should be granted upon first-time completion, avoiding duplicate rewards.
5. Identify UI components: Mission Select screen, wave indicators/HUD, completion/victory screens, boss health bar.
6. Verify how Mission 1 (`UrbanStreet.tscn` / tutorial) is implemented so it can remain completely intact and unmodified while supporting the new 12-mission campaign structure.

## Output Requirements
Write your comprehensive report to `/workspaces/targetkill/.agents/explorer_campaign/handoff.md`.
Report back when done with your key findings and handoff path.

## 2026-09-06T13:06:59Z
You are the Campaign Architecture Explorer.
Your working directory is /workspaces/targetkill/.agents/explorer_campaign/.
Read /workspaces/targetkill/ORIGINAL_REQUEST.md, /workspaces/targetkill/GEMINI.md, and /workspaces/targetkill/.agents/explorer_campaign/DISPATCH.md.
Investigate current mission scenes, Mission 1 (UrbanStreet.tscn), UI, wave management, spawning, stationary-FPS mechanics, progression, cash rewards ($500 -> $6000), and mission select UI.
Write your findings to /workspaces/targetkill/.agents/explorer_campaign/handoff.md.
When done, send a message to orchestrator with your summary and handoff path.
