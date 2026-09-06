import re

with open("scenes/UI/UpgradeUI.tscn", "r") as f:
    content = f.read()

# Add node for HeavyGunTab
shotgun_block = """[node name="ShotgunTab" type="Button" parent="ContentContainer/TabsBar"]
custom_minimum_size = Vector2(0, 44)
layout_mode = 2
size_flags_horizontal = 3
theme_override_font_sizes/font_size = 16
text = "REMINGTON 870 (SHOTGUN)"
"""

heavygun_block = """[node name="HeavyGunTab" type="Button" parent="ContentContainer/TabsBar"]
custom_minimum_size = Vector2(0, 44)
layout_mode = 2
size_flags_horizontal = 3
theme_override_font_sizes/font_size = 16
text = "M249 SAW (LMG)"
"""

content = content.replace(shotgun_block, shotgun_block + "\n" + heavygun_block)

# Add connection for HeavyGunTab
shotgun_conn = '[connection signal="pressed" from="ContentContainer/TabsBar/ShotgunTab" to="." method="_on_tab_pressed" binds= ["shotgun"]]'
heavygun_conn = '[connection signal="pressed" from="ContentContainer/TabsBar/HeavyGunTab" to="." method="_on_tab_pressed" binds= ["heavy_gun"]]'

content = content.replace(shotgun_conn, shotgun_conn + "\n" + heavygun_conn)

with open("scenes/UI/UpgradeUI.tscn", "w") as f:
    f.write(content)

