import re

path = "/workspaces/targetkill/scenes/test/TestRunner.gd"
with open(path, "r") as f:
    content = f.read()

old_code = """	if missions.size() == 12:
		for i in range(1, 13):
			var m = missions[i - 1]
			var expected_reward = 500 * i
			if m.reward_cash != expected_reward:
				cash_scaling_ok = false
				cash_errors.append("M%02d: $%d != expected $%d" % [i, m.reward_cash, expected_reward])"""

new_code = """	if missions.size() == 12:
		var expected_rewards = [500, 750, 1000, 1250, 1500, 1800, 2100, 2500, 3000, 3500, 4000, 6000]
		for i in range(1, 13):
			var m = missions[i - 1]
			var expected_reward = expected_rewards[i - 1]
			if m.reward_cash != expected_reward:
				cash_scaling_ok = false
				cash_errors.append("M%02d: $%d != expected $%d" % [i, m.reward_cash, expected_reward])"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, "w") as f:
        f.write(content)
    print("Fixed Test 46")
else:
    print("Could not find old code in TestRunner.gd")

