extends Control

@onready var cash_label = $TopBar/CashLabel
@onready var weapon_list = $WeaponListPanel/Scroll/VBox
@onready var pivot = $"3DView/SubViewport/WeaponPivot"

@onready var weapon_title = $StatsPanel/Margin/VBox/WeaponTitle
@onready var weapon_subtitle = $StatsPanel/Margin/VBox/WeaponSubtitle

@onready var dmg_val = $StatsPanel/Margin/VBox/DamageRow/Value
@onready var dmg_btn = $StatsPanel/Margin/VBox/DamageRow/UpgradeBtn

@onready var mag_val = $StatsPanel/Margin/VBox/MagRow/Value
@onready var mag_btn = $StatsPanel/Margin/VBox/MagRow/UpgradeBtn

@onready var reload_val = $StatsPanel/Margin/VBox/ReloadRow/Value
@onready var reload_btn = $StatsPanel/Margin/VBox/ReloadRow/UpgradeBtn

@onready var acc_val = $StatsPanel/Margin/VBox/AccuracyRow/Value
@onready var acc_btn = $StatsPanel/Margin/VBox/AccuracyRow/UpgradeBtn

@onready var unlock_btn = $StatsPanel/Margin/VBox/UnlockBtn

var current_weapon_id: String = "rifle"
var active_mesh: Node3D = null
var current_res: Resource = null

var weapons = [
    "pistol", "rifle", "shotgun", "m4a1", "ak47", "scar_l", "g36", "famas", "aug", "mp5", "spas12", "svd", "m249"
]

var meshes = {
    "pistol": "res://assets/3d/weapons/pistol.glb",
    "rifle": "res://assets/3d/weapons/rifle.glb",
    "shotgun": "res://assets/3d/weapons/shotgun.glb",
    "m4a1": "res://assets/3d/weapons/rifle.glb",
    "ak47": "res://assets/3d/weapons/rifle.glb",
    "scar_l": "res://assets/3d/weapons/rifle.glb",
    "g36": "res://assets/3d/weapons/rifle.glb",
    "famas": "res://assets/3d/weapons/rifle.glb",
    "aug": "res://assets/3d/weapons/rifle.glb",
    "mp5": "res://assets/3d/weapons/rifle.glb",
    "spas12": "res://assets/3d/weapons/shotgun.glb",
    "svd": "res://assets/3d/weapons/rifle.glb",
    "m249": "res://assets/3d/weapons/rifle.glb"
}

func _ready():
    $TopBar/BackButton.pressed.connect(_on_back)
    dmg_btn.pressed.connect(_on_upgrade.bind("damage"))
    mag_btn.pressed.connect(_on_upgrade.bind("mag"))
    reload_btn.pressed.connect(_on_upgrade.bind("reload"))
    acc_btn.pressed.connect(_on_upgrade.bind("accuracy"))
    unlock_btn.pressed.connect(_on_unlock)
    
    var event_bus = get_node_or_null("/root/EventBus")
    if event_bus:
        event_bus.cash_changed.connect(_on_cash_changed)
        
    var banner = get_node_or_null("/root/BannerAdManager")
    if banner:
        banner.show_banner()
        
    _populate_list()
    _select_weapon("rifle")
    _update_ui()

func _exit_tree():
    var banner = get_node_or_null("/root/BannerAdManager")
    if banner:
        banner.hide_banner()

func _process(delta):
    if pivot:
        pivot.rotation.y += delta * 0.5

func _populate_list():
    for child in weapon_list.get_children():
        child.queue_free()
        
    for wid in weapons:
        var res_path = "res://resources/weapons/" + wid + ".tres"
        var d_name = wid.to_upper()
        if ResourceLoader.exists(res_path):
            var res = load(res_path)
            if res and "display_name" in res and res.display_name != "":
                d_name = res.display_name
                
        var btn = Button.new()
        btn.custom_minimum_size = Vector2(0, 52)
        btn.text = d_name
        btn.pressed.connect(_select_weapon.bind(wid))
        weapon_list.add_child(btn)

func _select_weapon(wid: String):
    current_weapon_id = wid
    if active_mesh:
        active_mesh.queue_free()
        active_mesh = null
    
    var mesh_path = meshes.get(wid)
    if mesh_path and ResourceLoader.exists(mesh_path):
        var m = load(mesh_path)
        if m is PackedScene:
            var inst = m.instantiate()
            pivot.add_child(inst)
            inst.scale = Vector3(2.5, 2.5, 2.5)
            active_mesh = inst
        elif m is Mesh:
            var mi = MeshInstance3D.new()
            mi.mesh = m
            pivot.add_child(mi)
            mi.scale = Vector3(2.5, 2.5, 2.5)
            active_mesh = mi
            
    current_res = load("res://resources/weapons/" + wid + ".tres")
    _update_ui()

func _update_ui():
    var save_mgr = get_node_or_null("/root/SaveManager")
    if not save_mgr or not current_res: return
    
    var cash = save_mgr.data.cash
    cash_label.text = "CASH: $%d" % cash
    
    weapon_title.text = current_res.display_name
    weapon_subtitle.text = "Cost to Unlock: $5000" if wid_needs_unlock(save_mgr) else "Owned"
    
    var upgrades = save_mgr.data.weapon_upgrades.get(current_weapon_id, {})
    var d_lvl = upgrades.get("damage", 0)
    var m_lvl = upgrades.get("mag", 0)
    var r_lvl = upgrades.get("reload", 0)
    var a_lvl = upgrades.get("accuracy", 0)
    
    dmg_val.text = str(current_res.base_damage * (1.0 + d_lvl * 0.2))
    dmg_btn.text = "$%d" % (current_res.upgrade_cost_damage * (d_lvl + 1))
    dmg_btn.disabled = cash < (current_res.upgrade_cost_damage * (d_lvl + 1))
    
    mag_val.text = str(int(current_res.base_mag_size * (1.0 + m_lvl * 0.5)))
    mag_btn.text = "$%d" % (current_res.upgrade_cost_mag * (m_lvl + 1))
    mag_btn.disabled = cash < (current_res.upgrade_cost_mag * (m_lvl + 1))
    
    reload_val.text = str(current_res.base_reload_time * max(0.5, 1.0 - r_lvl * 0.15)) + "s"
    reload_btn.text = "$%d" % (current_res.upgrade_cost_reload * (r_lvl + 1))
    reload_btn.disabled = cash < (current_res.upgrade_cost_reload * (r_lvl + 1))
    
    var base_spread = current_res.spread if "spread" in current_res else 0.02
    var cur_spread = max(0.001, base_spread * (1.0 - a_lvl * 0.15))
    var acc_pct = int(clamp((1.0 - cur_spread * 8.0) * 100.0, 50.0, 99.0))
    acc_val.text = "%d%%" % acc_pct
    var acc_cost = (current_res.upgrade_cost_damage if "upgrade_cost_damage" in current_res else 100) * (a_lvl + 1)
    acc_btn.text = "$%d" % acc_cost
    acc_btn.disabled = cash < acc_cost
    
    if wid_needs_unlock(save_mgr):
        unlock_btn.visible = true
        dmg_btn.disabled = true
        mag_btn.disabled = true
        reload_btn.disabled = true
        acc_btn.disabled = true
    else:
        unlock_btn.visible = false

func wid_needs_unlock(save_mgr) -> bool:
    return not (current_weapon_id in save_mgr.data.unlocked_weapons)

func _on_upgrade(type: String):
    var save_mgr = get_node_or_null("/root/SaveManager")
    if not save_mgr or not current_res: return
    
    var upgrades = save_mgr.data.weapon_upgrades
    if not upgrades.has(current_weapon_id):
        upgrades[current_weapon_id] = {"damage": 0, "mag": 0, "reload": 0, "accuracy": 0}
    elif not upgrades[current_weapon_id].has("accuracy"):
        upgrades[current_weapon_id]["accuracy"] = 0
        
    var lvl = upgrades[current_weapon_id].get(type, 0)
    var cost = 0
    if type == "damage": cost = current_res.upgrade_cost_damage * (lvl + 1)
    elif type == "mag": cost = current_res.upgrade_cost_mag * (lvl + 1)
    elif type == "reload": cost = current_res.upgrade_cost_reload * (lvl + 1)
    elif type == "accuracy": cost = (current_res.upgrade_cost_damage if "upgrade_cost_damage" in current_res else 100) * (lvl + 1)
    
    if save_mgr.data.cash >= cost:
        save_mgr.add_cash(-cost)
        upgrades[current_weapon_id][type] = lvl + 1
        save_mgr.save_game()
        _update_ui()

func _on_unlock():
    var save_mgr = get_node_or_null("/root/SaveManager")
    if not save_mgr: return
    
    if save_mgr.data.cash >= 5000:
        save_mgr.add_cash(-5000)
        _do_unlock(save_mgr)
    else:
        var ad_mgr = get_node_or_null("/root/AdManager")
        if ad_mgr:
            ad_mgr.reward_granted.connect(_on_ad_reward.bind(save_mgr), CONNECT_ONE_SHOT)
            ad_mgr.show_rewarded_ad("unlock")

func _on_ad_reward(reward_type, amount, save_mgr):
    if reward_type == "unlock":
        _do_unlock(save_mgr)

func _do_unlock(save_mgr):
    if not current_weapon_id in save_mgr.data.unlocked_weapons:
        save_mgr.data.unlocked_weapons.append(current_weapon_id)
        save_mgr.save_game()
    _update_ui()

func _on_cash_changed(amount: int):
    _update_ui()

func _on_back():
    get_tree().change_scene_to_file("res://scenes/UI/MainMenu.tscn")
