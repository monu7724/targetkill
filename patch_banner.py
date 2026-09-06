import re

with open("scenes/UI/MainMenu.tscn", "r") as f:
    content = f.read()

# Add a fake banner ad at the bottom of the main menu
banner_ui = """
[node name="AdMobBanner" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 12
anchor_top = 1.0
anchor_right = 1.0
anchor_bottom = 1.0
offset_top = -60.0
grow_horizontal = 2
grow_vertical = 0
color = Color(0.1, 0.1, 0.1, 0.95)

[node name="Label" type="Label" parent="AdMobBanner"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
theme_override_colors/font_color = Color(0.5, 0.5, 0.5, 1)
theme_override_font_sizes/font_size = 18
text = "Google AdMob Banner Space (320x50)"
horizontal_alignment = 1
vertical_alignment = 1
"""

if "AdMobBanner" not in content:
    content += banner_ui

with open("scenes/UI/MainMenu.tscn", "w") as f:
    f.write(content)
