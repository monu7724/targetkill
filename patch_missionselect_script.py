with open("scripts/MissionSelectUI.gd", "r") as f:
    content = f.read()

content = content.replace('COINS', 'CASH')
content = content.replace('coins_label.text = "CASH: %d" % coins', 'coins_label.text = "CASH: $%d" % coins')

with open("scripts/MissionSelectUI.gd", "w") as f:
    f.write(content)
