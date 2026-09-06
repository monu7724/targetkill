import re

with open("scenes/UI/UpgradeUI.tscn", "r") as f:
    content = f.read()

# Change TabsBar from HBoxContainer to ScrollContainer, and put an HBox inside
if '[node name="TabsBar" type="HBoxContainer"' in content:
    content = content.replace('[node name="TabsBar" type="HBoxContainer" parent="ContentContainer"]', 
        '[node name="TabsBar" type="ScrollContainer" parent="ContentContainer"]\n'
        'custom_minimum_size = Vector2(0, 60)\n'
        '[node name="TabsHBox" type="HBoxContainer" parent="ContentContainer/TabsBar"]\n'
        'layout_mode = 2\n'
        'size_flags_horizontal = 3\n'
        'size_flags_vertical = 3\n'
        'theme_override_constants/separation = 10'
    )
    # Now all buttons under TabsBar need to be reparented to TabsHBox
    content = content.replace('parent="ContentContainer/TabsBar"]', 'parent="ContentContainer/TabsBar/TabsHBox"]')
    content = content.replace('from="ContentContainer/TabsBar/', 'from="ContentContainer/TabsBar/TabsHBox/')

    # Add the 10 new heavy gun tabs
    ids = ["m134", "rpg7", "rpd", "mg42", "l86", "m249", "pkm", "m60", "m2browning", "flamethrower"]
    names = ["M134 MINIGUN", "RPG-7", "RPD", "MG42", "L86 LSW", "M249 SAW", "PKM", "M60", "M2 BROWNING", "FLAMETHROWER"]
    
    new_tabs = ""
    new_connections = ""
    for i, (id, name) in enumerate(zip(ids, names)):
        tab_name = f"HeavyTab{i}"
        new_tabs += f"""
[node name="{tab_name}" type="Button" parent="ContentContainer/TabsBar/TabsHBox"]
custom_minimum_size = Vector2(180, 44)
layout_mode = 2
theme_override_font_sizes/font_size = 14
text = "{name}"
"""
        new_connections += f'[connection signal="pressed" from="ContentContainer/TabsBar/TabsHBox/{tab_name}" to="." method="_on_tab_pressed" binds= ["heavy_{id}"]]\n'

    content = content.replace('[node name="Panel" type="PanelContainer"', new_tabs + '\n[node name="Panel" type="PanelContainer"')
    content += new_connections

    with open("scenes/UI/UpgradeUI.tscn", "w") as f:
        f.write(content)
