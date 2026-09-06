Weapons & Armory - Brief

Branch: agent/weapons-armory

Scope
- resources/weapons/*
- scenes/weapons/*
- scripts/Weapons/*
- scripts/Characters/Player.gd

Deliverables
- Ensure the registry contains 10 weapons (or document unavailable assets).
- Add headless tests for equip/switch/fire/reload flows.
- Expose armory UI hooks for unlock/purchase.

Acceptance criteria
- `scripts/Weapons/WeaponManager.gd` provides `get_all_weapon_ids()` and `get_weapon_data()` (already present) and tests verify expected IDs.
- Armory UI shows available weapons per save data.

Initial tasks
1. Add `scripts/Weapons/armory_stub.gd` as a small integration helper.
2. Add headless test `tools/test_weapons_economy.gd` invocation or update existing tests.
3. Run headless tests.