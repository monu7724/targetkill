import os

armory_tscn = """[gd_scene load_steps=7 format=3 uid="uid://cy8xx1234abcd"]

[ext_resource type="Script" path="res://scripts/UI/ArmoryUI.gd" id="1_armory"]
[ext_resource type="PackedScene" path="res://scenes/UI/Components/PrimaryButton.tscn" id="2_btn"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_bg"]
bg_color = Color(0.08, 0.09, 0.11, 1)

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_panel"]
bg_color = Color(0.12, 0.14, 0.17, 0.9)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.25, 0.3, 0.35, 1)
corner_radius_top_left = 8
corner_radius_top_right = 8
corner_radius_bottom_right = 8
corner_radius_bottom_left = 8

[node name="ArmoryUI" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_armory")

[node name="Background" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_bg")

[node name="3DView" type="SubViewportContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
stretch = true

[node name="SubViewport" type="SubViewport" parent="3DView"]
transparent_bg = true
handle_input_locally = false
size = Vector2i(1280, 720)
render_target_update_mode = 4

[node name="WeaponPreviewCam" type="Camera3D" parent="3DView/SubViewport"]
transform = Transform3D(0.866025, -0.17101, 0.469846, 0, 0.939693, 0.34202, -0.5, -0.296198, 0.813798, 1.2, 0.8, 2)
current = true

[node name="WeaponPivot" type="Node3D" parent="3DView/SubViewport"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="3DView/SubViewport"]
transform = Transform3D(0.707107, -0.5, 0.5, 0, 0.707107, 0.707107, -0.707107, -0.5, 0.5, 0, 5, 0)
light_color = Color(0.9, 0.95, 1, 1)
light_energy = 1.5

[node name="OmniLight3D" type="OmniLight3D" parent="3DView/SubViewport"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.5, 0.5, 1)
light_color = Color(1, 0.8, 0.6, 1)
light_energy = 2.0
omni_range = 3.0

[node name="TopBar" type="HBoxContainer" parent="."]
layout_mode = 1
anchors_preset = 10
anchor_right = 1.0
offset_left = 32.0
offset_top = 32.0
offset_right = -32.0
offset_bottom = 72.0
grow_horizontal = 2

[node name="BackButton" parent="TopBar" instance=ExtResource("2_btn")]
layout_mode = 2
custom_minimum_size = Vector2(150, 40)
text = "BACK"

[node name="Spacer" type="Control" parent="TopBar"]
layout_mode = 2
size_flags_horizontal = 3

[node name="CashLabel" type="Label" parent="TopBar"]
layout_mode = 2
theme_override_colors/font_color = Color(0.5, 1, 0.5, 1)
theme_override_font_sizes/font_size = 28
text = "CASH: $0"

[node name="WeaponListPanel" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 9
anchor_bottom = 1.0
offset_left = 32.0
offset_top = 100.0
offset_right = 382.0
offset_bottom = -32.0
grow_vertical = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_panel")

[node name="Scroll" type="ScrollContainer" parent="WeaponListPanel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 16.0
offset_top = 16.0
offset_right = -16.0
offset_bottom = -16.0
grow_horizontal = 2
grow_vertical = 2

[node name="VBox" type="VBoxContainer" parent="WeaponListPanel/Scroll"]
layout_mode = 2
size_flags_horizontal = 3
theme_override_constants/separation = 12

[node name="StatsPanel" type="Panel" parent="."]
layout_mode = 1
anchors_preset = 11
anchor_left = 1.0
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = -450.0
offset_top = 100.0
offset_right = -32.0
offset_bottom = -32.0
grow_horizontal = 0
grow_vertical = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_panel")

[node name="Margin" type="MarginContainer" parent="StatsPanel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 24.0
offset_top = 24.0
offset_right = -24.0
offset_bottom = -24.0
grow_horizontal = 2
grow_vertical = 2

[node name="VBox" type="VBoxContainer" parent="StatsPanel/Margin"]
layout_mode = 2
theme_override_constants/separation = 20

[node name="WeaponTitle" type="Label" parent="StatsPanel/Margin/VBox"]
layout_mode = 2
theme_override_font_sizes/font_size = 36
text = "WEAPON NAME"
horizontal_alignment = 1

[node name="WeaponSubtitle" type="Label" parent="StatsPanel/Margin/VBox"]
layout_mode = 2
theme_override_colors/font_color = Color(0.6, 0.6, 0.6, 1)
theme_override_font_sizes/font_size = 18
text = "Description here"
horizontal_alignment = 1
autowrap_mode = 2

[node name="HSeparator" type="HSeparator" parent="StatsPanel/Margin/VBox"]
layout_mode = 2

[node name="DamageRow" type="HBoxContainer" parent="StatsPanel/Margin/VBox"]
layout_mode = 2
alignment = 1

[node name="Label" type="Label" parent="StatsPanel/Margin/VBox/DamageRow"]
custom_minimum_size = Vector2(100, 0)
layout_mode = 2
text = "DAMAGE"

[node name="Value" type="Label" parent="StatsPanel/Margin/VBox/DamageRow"]
layout_mode = 2
size_flags_horizontal = 3
text = "100"
horizontal_alignment = 2

[node name="UpgradeBtn" parent="StatsPanel/Margin/VBox/DamageRow" instance=ExtResource("2_btn")]
layout_mode = 2
custom_minimum_size = Vector2(120, 40)
text = "$1500"

[node name="MagRow" type="HBoxContainer" parent="StatsPanel/Margin/VBox"]
layout_mode = 2
alignment = 1

[node name="Label" type="Label" parent="StatsPanel/Margin/VBox/MagRow"]
custom_minimum_size = Vector2(100, 0)
layout_mode = 2
text = "AMMO"

[node name="Value" type="Label" parent="StatsPanel/Margin/VBox/MagRow"]
layout_mode = 2
size_flags_horizontal = 3
text = "30"
horizontal_alignment = 2

[node name="UpgradeBtn" parent="StatsPanel/Margin/VBox/MagRow" instance=ExtResource("2_btn")]
layout_mode = 2
custom_minimum_size = Vector2(120, 40)
text = "$1000"

[node name="ReloadRow" type="HBoxContainer" parent="StatsPanel/Margin/VBox"]
layout_mode = 2
alignment = 1

[node name="Label" type="Label" parent="StatsPanel/Margin/VBox/ReloadRow"]
custom_minimum_size = Vector2(100, 0)
layout_mode = 2
text = "RELOAD"

[node name="Value" type="Label" parent="StatsPanel/Margin/VBox/ReloadRow"]
layout_mode = 2
size_flags_horizontal = 3
text = "2.5s"
horizontal_alignment = 2

[node name="UpgradeBtn" parent="StatsPanel/Margin/VBox/ReloadRow" instance=ExtResource("2_btn")]
layout_mode = 2
custom_minimum_size = Vector2(120, 40)
text = "$1200"

[node name="HSeparator2" type="HSeparator" parent="StatsPanel/Margin/VBox"]
layout_mode = 2

[node name="UnlockBtn" parent="StatsPanel/Margin/VBox" instance=ExtResource("2_btn")]
layout_mode = 2
custom_minimum_size = Vector2(0, 60)
text = "UNLOCK (WATCH AD OR $5000)"

"""
os.makedirs("/workspaces/targetkill/scenes/UI", exist_ok=True)
os.makedirs("/workspaces/targetkill/scripts/UI", exist_ok=True)
with open("/workspaces/targetkill/scenes/UI/ArmoryUI.tscn", "w") as f:
    f.write(armory_tscn)

armory_gd = """extends Control

@onready var cash_label = $TopBar/CashLabel
@onready var weapon_list = $WeaponListPanel/Scroll/VBox
@onready var pivot = $3DView/SubViewport/WeaponPivot

@onready var weapon_title = $StatsPanel/Margin/VBox/WeaponTitle
@onready var weapon_subtitle = $StatsPanel/Margin/VBox/WeaponSubtitle

@onready var dmg_val = $StatsPanel/Margin/VBox/DamageRow/Value
@onready var dmg_btn = $StatsPanel/Margin/VBox/DamageRow/UpgradeBtn

@onready var mag_val = $StatsPanel/Margin/VBox/MagRow/Value
@onready var mag_btn = $StatsPanel/Margin/VBox/MagRow/UpgradeBtn

@onready var reload_val = $StatsPanel/Margin/VBox/ReloadRow/Value
@onready var reload_btn = $StatsPanel/Margin/VBox/ReloadRow/UpgradeBtn

@onready var unlock_btn = $StatsPanel/Margin/VBox/UnlockBtn

var current_weapon_id: String = "rifle"
var active_mesh: Node3D = null
var current_res: Resource = null

var weapons = [
    "pistol", "rifle", "shotgun", "m4a1", "ak47", "scar_l", "g36", "famas", "aug", "mp5", "spas12", "svd", "m249"
]

var meshes = {
    "pistol": "res://models/weapons/pistol.obj",
    "rifle": "res://models/weapons/rifle.obj",
    "shotgun": "res://models/weapons/shotgun.obj",
    "m4a1": "res://models/weapons/m4a1.obj",
    "ak47": "res://models/weapons/ak47.obj",
    "scar_l": "res://models/weapons/scar_l.obj",
    "g36": "res://models/weapons/g36.obj",
    "famas": "res://models/weapons/famas.obj",
    "aug": "res://models/weapons/aug.obj",
    "mp5": "res://models/weapons/mp5.obj",
    "spas12": "res://models/weapons/spas12.obj",
    "svd": "res://models/weapons/svd.obj",
    "m249": "res://models/weapons/m249.obj"
}

func _ready():
    $TopBar/BackButton.pressed.connect(_on_back)
    dmg_btn.pressed.connect(_on_upgrade.bind("damage"))
    mag_btn.pressed.connect(_on_upgrade.bind("mag"))
    reload_btn.pressed.connect(_on_upgrade.bind("reload"))
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
        var btn = Button.new()
        btn.custom_minimum_size = Vector2(0, 60)
        btn.text = wid.to_upper()
        btn.pressed.connect(_select_weapon.bind(wid))
        weapon_list.add_child(btn)

func _select_weapon(wid: String):
    current_weapon_id = wid
    if active_mesh:
        active_mesh.queue_free()
    
    var mesh_path = meshes.get(wid)
    if mesh_path and ResourceLoader.exists(mesh_path):
        var m = load(mesh_path)
        if m:
            var mi = MeshInstance3D.new()
            mi.mesh = m
            pivot.add_child(mi)
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
    
    dmg_val.text = str(current_res.base_damage * (1.0 + d_lvl * 0.2))
    dmg_btn.text = "$%d" % (current_res.upgrade_cost_damage * (d_lvl + 1))
    dmg_btn.disabled = cash < (current_res.upgrade_cost_damage * (d_lvl + 1))
    
    mag_val.text = str(int(current_res.base_mag_size * (1.0 + m_lvl * 0.5)))
    mag_btn.text = "$%d" % (current_res.upgrade_cost_mag * (m_lvl + 1))
    mag_btn.disabled = cash < (current_res.upgrade_cost_mag * (m_lvl + 1))
    
    reload_val.text = str(current_res.base_reload_time * max(0.5, 1.0 - r_lvl * 0.15)) + "s"
    reload_btn.text = "$%d" % (current_res.upgrade_cost_reload * (r_lvl + 1))
    reload_btn.disabled = cash < (current_res.upgrade_cost_reload * (r_lvl + 1))
    
    if wid_needs_unlock(save_mgr):
        unlock_btn.visible = true
        dmg_btn.disabled = true
        mag_btn.disabled = true
        reload_btn.disabled = true
    else:
        unlock_btn.visible = false

func wid_needs_unlock(save_mgr) -> bool:
    return not (current_weapon_id in save_mgr.data.unlocked_weapons)

func _on_upgrade(type: String):
    var save_mgr = get_node_or_null("/root/SaveManager")
    if not save_mgr or not current_res: return
    
    var upgrades = save_mgr.data.weapon_upgrades
    if not upgrades.has(current_weapon_id):
        upgrades[current_weapon_id] = {"damage": 0, "mag": 0, "reload": 0}
        
    var lvl = upgrades[current_weapon_id].get(type, 0)
    var cost = 0
    if type == "damage": cost = current_res.upgrade_cost_damage * (lvl + 1)
    if type == "mag": cost = current_res.upgrade_cost_mag * (lvl + 1)
    if type == "reload": cost = current_res.upgrade_cost_reload * (lvl + 1)
    
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
"""
with open("/workspaces/targetkill/scripts/UI/ArmoryUI.gd", "w") as f:
    f.write(armory_gd)

print("Generated ArmoryUI scene and script")
