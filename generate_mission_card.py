import os

card_tscn = """[gd_scene load_steps=5 format=3 uid="uid://cxmissioncard"]

[ext_resource type="Script" path="res://scripts/MissionCardUI.gd" id="1_mcard"]
[ext_resource type="PackedScene" path="res://scenes/UI/Components/PrimaryButton.tscn" id="2_btn"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_card_bg"]
bg_color = Color(0.12, 0.14, 0.17, 0.95)
border_width_left = 4
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.3, 0.3, 0.35, 1)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
shadow_color = Color(0, 0, 0, 0.6)
shadow_size = 8

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_thumb"]
bg_color = Color(0, 0, 0, 1)
corner_radius_top_left = 10
corner_radius_bottom_left = 10

[node name="MissionCard" type="PanelContainer"]
custom_minimum_size = Vector2(800, 200)
theme_override_styles/panel = SubResource("StyleBoxFlat_card_bg")
script = ExtResource("1_mcard")

[node name="HBox" type="HBoxContainer" parent="."]
layout_mode = 2
theme_override_constants/separation = 16

[node name="ThumbnailPanel" type="Panel" parent="HBox"]
custom_minimum_size = Vector2(250, 0)
layout_mode = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_thumb")

[node name="Thumbnail" type="TextureRect" parent="HBox/ThumbnailPanel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
expand_mode = 1
stretch_mode = 6

[node name="VBox" type="VBoxContainer" parent="HBox"]
layout_mode = 2
size_flags_horizontal = 3
theme_override_constants/separation = 8
alignment = 1

[node name="Title" type="Label" parent="HBox/VBox"]
layout_mode = 2
theme_override_colors/font_color = Color(1, 0.85, 0.3, 1)
theme_override_font_sizes/font_size = 28
text = "MISSION TITLE"

[node name="Objective" type="Label" parent="HBox/VBox"]
layout_mode = 2
theme_override_colors/font_color = Color(0.8, 0.8, 0.8, 1)
theme_override_font_sizes/font_size = 18
text = "Objective: Eliminate targets"

[node name="Reward" type="Label" parent="HBox/VBox"]
layout_mode = 2
theme_override_colors/font_color = Color(0.5, 1, 0.5, 1)
theme_override_font_sizes/font_size = 20
text = "REWARD: $1000"

[node name="Status" type="Label" parent="HBox/VBox"]
layout_mode = 2
theme_override_colors/font_color = Color(0.5, 0.5, 0.5, 1)
theme_override_font_sizes/font_size = 16
text = "STATUS: UNLOCKED"

[node name="Margin" type="MarginContainer" parent="HBox"]
layout_mode = 2
theme_override_constants/margin_right = 16

[node name="PlayButton" parent="HBox/Margin" instance=ExtResource("2_btn")]
layout_mode = 2
size_flags_vertical = 4
custom_minimum_size = Vector2(220, 60)
text = "DEPLOY"

[connection signal="pressed" from="HBox/Margin/PlayButton" to="." method="_on_play_button_pressed"]

"""

with open("/workspaces/targetkill/scenes/UI/MissionCard.tscn", "w") as f:
    f.write(card_tscn)

print("Generated new MissionCard.tscn")
