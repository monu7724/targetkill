# Sector Zero: Lockdown - Development Guide

## Project Overview
A ₹0 budget realistic Android zombie FPS built with Godot 4.x. 

## Current Progress (Phase 5: Final Content & Launch Prep)
- [x] **Game Identity:**
    - Final title: **Sector Zero: Lockdown**.
    - Original branding implemented in `MainMenu.tscn`.
- [x] **Tutorial:**
    - `TutorialUI.tscn`: Interactive 5-step onboarding for new players.
    - Logic integrated into `UrbanStreet.tscn` (automatic skip if completed).
- [x] **Weapon Balancing:**
    - USP-45 (Pistol), M4A1 Sentinel (Rifle), Remington 870 (Shotgun) balanced for distinct roles.
- [x] **HUD Polish:**
    - Integrated Boss Health Bar and Mission Objective display in `HUD.tscn`.
    - Added responsive `RELOAD` button for mobile touch.
- [x] **Launch Assets:**
    - `STORE_LISTING.md`: Original marketing copy for Google Play.
    - `ASSET_LICENSES.md`: Finalized third-party legal documentation.
- [x] **Persistence:**
    - Settings (Volume, Graphics) and Tutorial state saved in `SaveManager`.

## Final QA Gate
1. **Boot:** `MainMenu.tscn` launches with 'Sector Zero' branding.
2. **Onboarding:** Tutorial triggers on Mission 1 for new saves.
3. **Combat:** Shooting, reloading, and headshots work as expected.
4. **Progression:** Coins earned, weapons upgraded, missions unlocked.
5. **Persistence:** Progression survives app restart.
6. **Android:** Signed .aab generated for Play Store.

## Release Metadata
- **Version Name:** 1.0.0
- **Version Code:** 1
- **Package ID:** com.targetzero.lockdown (example)
- **Min SDK:** 24 (Android 7.0)
- **Target SDK:** 34 (Android 14)
