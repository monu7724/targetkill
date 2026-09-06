with open("scripts/UpgradeUI.gd", "r") as f:
    content = f.read()

# Add weapon_resources
new_weapons = """
	"heavy_m134": "res://resources/weapons/heavy_m134.tres",
	"heavy_rpg7": "res://resources/weapons/heavy_rpg7.tres",
	"heavy_rpd": "res://resources/weapons/heavy_rpd.tres",
	"heavy_mg42": "res://resources/weapons/heavy_mg42.tres",
	"heavy_l86": "res://resources/weapons/heavy_l86.tres",
	"heavy_m249": "res://resources/weapons/heavy_m249.tres",
	"heavy_pkm": "res://resources/weapons/heavy_pkm.tres",
	"heavy_m60": "res://resources/weapons/heavy_m60.tres",
	"heavy_m2browning": "res://resources/weapons/heavy_m2browning.tres",
	"heavy_flamethrower": "res://resources/weapons/heavy_flamethrower.tres"
"""

content = content.replace('"heavy_gun": "res://resources/weapons/heavy_gun.tres"', '"heavy_gun": "res://resources/weapons/heavy_gun.tres",' + new_weapons)

# Fix modulation in _on_tab_pressed (since we have dynamically added tabs, we can't hardcode modulate them easily without a group, let's just ignore color for unselected tabs)
# Remove old hardcoded modulate lines
import re
content = re.sub(r'\t\w+_tab\.modulate = .*\n', '', content)

# Change COINS to CASH $
content = content.replace('COINS', 'CASH $')
content = content.replace('COIN', 'CASH')
content = content.replace('coins_label.text = "CASH $: %d" % coins', 'coins_label.text = "CASH $: $%d" % coins')
content = content.replace('NOT ENOUGH CASH $', 'NOT ENOUGH CASH')
content = content.replace('CASH $S', 'CASH')
content = content.replace('UPGRADE (%d CASH $)', 'UPGRADE ($%d)')
content = content.replace('NOT ENOUGH CASH (%d)', 'NOT ENOUGH CASH ($%d)')

with open("scripts/UpgradeUI.gd", "w") as f:
    f.write(content)
