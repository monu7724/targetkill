import glob
import re

files = glob.glob('resources/missions/*.tres')

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # We want to replace spawn_config line
    # Depending on difficulty or just randomly adding them
    if 'spawn_config' in content:
        content = re.sub(r'spawn_config = \[.*\]', 'spawn_config = [{"type": "normal", "weight": 0.4}, {"type": "fast", "weight": 0.2}, {"type": "heavy", "weight": 0.1}, {"type": "dog", "weight": 0.2}, {"type": "spitter", "weight": 0.1}]', content)
        with open(f, 'w') as file:
            file.write(content)
