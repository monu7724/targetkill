# Sector Zero: Lockdown — Production Architecture Specification

## 1. Architectural Modules

```
scripts/
├── Core/
│   ├── GameStateManager.gd    # 11-state flow, single-state enforcement, tree pause controller
│   └── EventBus.gd            # Decoupled global signal dispatcher
├── Gameplay/
│   ├── InputController.gd     # Multitouch tracking (Fingers 1, 2, 3) & keyboard fallback
│   ├── CameraController.gd    # Smooth yaw/pitch, breathing sway, movement bob, recoil kick
│   └── GameManager.gd         # Wave lifecycle and mission controller
├── Combat/
│   ├── HitZone.gd             # Regional hitboxes: Head (2.5x), Chest (1.0x), Arm (0.7x), Leg (0.7x)
│   └── DamageSystem.gd        # Falloff calculation, headshot multipliers, hit validation
├── Characters/
│   └── Player.gd              # Mobile FPS CharacterBody3D with smooth acceleration/deceleration
├── Zombies/
│   ├── ZombieAI.gd            # 9-state AI (IDLE, WANDER, NOTICE, CHASE, ATTACK, STAGGER, SEARCH, LOST, DEAD)
│   ├── ZombieDirector.gd      # Tension-curve wave pacing & active zombie capping (max 10 on mobile)
│   └── SpawnPoint.gd          # Safe distance (>12m) spawn positioning
├── Weapons/
│   ├── WeaponData.gd          # Data-driven weapon resource (damage, spread, recoil, mag, pellets)
│   └── WeaponController.gd    # Synchronized pipeline: Input -> Recoil -> Muzzle -> Sound -> Raycast -> Reaction
├── Missions/
│   ├── MissionData.gd         # Data-driven mission resource (Kill Count, Survive Waves, Boss Kill)
│   ├── MissionManager.gd      # Objective tracker, rewards, and safe transition
│   └── DifficultyManager.gd   # Easy, Normal, Hard scalability
├── UI/
│   ├── TacticalButton.gd      # Reusable 150ms bounce scale button with tactile click
│   ├── ModalPanel.gd          # Animated modal container with input isolation
│   ├── ToastMessage.gd        # Non-intrusive slide-in/fade-out notification
│   ├── HUD.gd                 # Landscape touch HUD, joystick, look area, boss health bar
│   ├── MainMenuUI.gd          # Menu controller with hidden 5-tap developer diagnostics
│   ├── MissionSelectUI.gd     # Mission selector and card scroller
│   ├── ResultUI.gd            # Animated count-up rewards and victory/defeat screens
│   └── SettingsUI.gd          # Audio sliders and graphics quality selectors
├── Audio/
│   └── AudioManager.gd        # Layered buses (Master, Music, SFX, Ambience) with dynamic ducking
├── VFX/
│   └── VFXManager.gd          # High-performance object pooling for blood, sparks, dust, muzzle flash
├── World/
│   ├── LightingProfiles.gd    # Reusable daylight profiles (DAY_CLEAR, DAY_CLOUDY, INDOOR_DAY, BOSS_FACILITY)
│   └── WorldStreamer.gd       # Distance culling for active, near, and distant prop visibility
├── Save/
│   └── SaveManager.gd         # Version 2 format with atomic .tmp write and backup recovery
├── Loading/
│   └── LoadingManager.gd      # Threaded async loader with animated UI and crash fallback
├── Performance/
│   └── PerformanceManager.gd  # Real-time FPS monitoring, adaptive throttling, and dev diagnostics overlay
└── Tools/
    ├── build_pipeline.sh      # Automated build and validation script
    └── test_visual_acceptance.gd # 9-step visual verification runner
```

---

## 2. Game State Flow

```
[BOOT] ───────────────► [MAIN_MENU] ◄──────────────┐
                             │                     │
                             ▼                     │
                     [MISSION_SELECT] ◄────────┐   │
                             │                 │   │
                             ▼                 │   │
                     [LOADING] (Async)         │   │
                             │                 │   │
                             ▼                 │   │
                     [GAMEPLAY] ◄──┐           │   │
                         │   ▲     │           │   │
             Pause/Resume│   │     │           │   │
                         ▼   │     │           │   │
                      [PAUSED]     │           │   │
                         │         │           │   │
            Complete/Fail│         │           │   │
                         ▼         │           │   │
                 [MISSION_RESULT] ─┘           │   │
                         │                     │   │
                         └─────────────────────┴───┘
```

---

## 3. Weapon Handling Data Table

| Weapon | Damage | Headshot Mult | Fire Rate | Mag Size | Reserve | Pellets | Spread | Recoil |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **USP-45** | 25.0 | 2.5x | 0.25s (Semi) | 12 | 96 | 1 | 0.005 (Accurate) | 1.2 |
| **M4A1 Sentinel** | 22.0 | 2.0x | 0.12s (Auto) | 30 | 180 | 1 | 0.020 (Controlled) | 0.85 |
| **Remington 870** | 95.0 | 1.8x | 0.80s (Pump) | 6 | 36 | 8 | 0.065 (Cone) | 2.8 |

---

## 4. Hardware Quality Tiers

* **LOW (Older devices / Low-tier Android):**
  * 3D Viewport Scale: 0.85
  * Directional Shadows: Disabled
  * Antialiasing: Disabled
  * HDR: Disabled
  * Active Zombie Cap: 8
* **MEDIUM (Standard modern mobile devices):**
  * 3D Viewport Scale: 1.0
  * Directional Shadows: Orthogonal (2048 atlas)
  * Antialiasing: FXAA + MSAA 2X
  * HDR: Enabled
  * Active Zombie Cap: 10
* **HIGH (Flagship devices):**
  * 3D Viewport Scale: 1.0
  * Directional Shadows: Parallel 4-Splits (4096 atlas)
  * Antialiasing: FXAA + MSAA 4X
  * SSAO & Glow: Enabled
  * Active Zombie Cap: 12
