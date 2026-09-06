extends Node

class_name ArmoryStub

func list_available_weapons(save_mgr):
    if not save_mgr:
        return []
    return save_mgr.data.get("unlocked_weapons", [])

func purchase(save_mgr, weapon_id: String):
    # Placeholder: forward to WeaponManager.purchase_weapon when integrated
    return false
