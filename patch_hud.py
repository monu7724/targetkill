import re

with open("scenes/UI/HUD.tscn", "r") as f:
    content = f.read()

# Hide Joystick by default
if 'visible = false' not in content.split('[node name="VirtualJoystick"')[1].split('[node')[0]:
    content = content.replace('[node name="VirtualJoystick" type="Control" parent="Control"]\n', '[node name="VirtualJoystick" type="Control" parent="Control"]\nvisible = false\n')

# Add Grenade Button near Reload Button
grenade_btn = """[node name="GrenadeButton" type="Button" parent="Control"]
layout_mode = 1
anchors_preset = 3
anchor_left = 1.0
anchor_top = 1.0
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = -320.0
offset_top = -140.0
offset_right = -220.0
offset_bottom = -40.0
grow_horizontal = 0
grow_vertical = 0
theme_override_styles/normal = SubResource("StyleBoxFlat_tactical_btn")
text = "GRENADE"
"""

if "GrenadeButton" not in content:
    content = content.replace('[node name="SwitchButton"', grenade_btn + '\n[node name="SwitchButton"')

with open("scenes/UI/HUD.tscn", "w") as f:
    f.write(content)
