# DISPATCH — Explorer: Environment Complexes, Infected Dogs & Android Performance

## Objective
Investigate environment assets, dog enemy models/rigs/animations, and Android performance constraints in `/workspaces/targetkill`.

## Scope & Tasks
1. Read `/workspaces/targetkill/ORIGINAL_REQUEST.md` and `/workspaces/targetkill/GEMINI.md`.
2. Survey existing 3D environments, materials, textures, shaders, and lighting setups across the project.
3. Check status and assets for the 5 requested environment complexes:
   - Airport (Service road, tarmac, hangars)
   - Railway
   - Urban
   - Industrial
   - Quarantine
4. Inspect existing enemy implementations (e.g., `Zombie.tscn`, character models, skeletons, animations, hit zones).
5. Search for any dog models, animations, rigs, or audio assets in the project or determine what CC0/commercial-safe assets are available or needed. Check `ASSET_LICENSES.md`.
6. Detail requirements for Mission 2 Infected Dogs:
   - Skeletal animations (run, attack, hit, death; no T-posing or floating limbs)
   - Realistic PBR materials
   - Distinct hit zones (Head, Body)
   - Wave compositions (Wave 1: small groups; Wave 2: larger groups + varied spawn directions; Wave 3: largest assault + special final group).
7. Review performance settings, project settings (Godot 4 renderer, Mobile/Forward+/Compatibility, resolution, shadows, particle limits) for 720p 60fps on Android.

## Output Requirements
Write your comprehensive report to `/workspaces/targetkill/.agents/explorer_assets/handoff.md`.
Report back when done with your key findings and handoff path.

## 2026-09-06T13:06:59Z
You are the Environment and Assets Explorer.
Your working directory is /workspaces/targetkill/.agents/explorer_assets/.
Read /workspaces/targetkill/ORIGINAL_REQUEST.md, /workspaces/targetkill/GEMINI.md, and /workspaces/targetkill/.agents/explorer_assets/DISPATCH.md.
Investigate 3D environment assets (Airport, Railway, Urban, Industrial, Quarantine), zombie/dog enemy models, rigs, skeletal animations, hit zones, ASSET_LICENSES.md, and Android performance constraints (720p 60fps).
Write your findings to /workspaces/targetkill/.agents/explorer_assets/handoff.md.
When done, send a message to orchestrator with your summary and handoff path.
