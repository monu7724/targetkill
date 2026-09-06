import glob
import re

files = glob.glob('scenes/environments/*.tscn')

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    if "glow_enabled" not in content and "Environment" in content:
        content = re.sub(
            r'(tonemap_white = [^\n]+)',
            r'\1\nssao_enabled = true\nssao_radius = 1.2\nssao_intensity = 1.5\nglow_enabled = true\nglow_intensity = 1.2\nglow_bloom = 0.15',
            content
        )
        
        with open(f, 'w') as file:
            file.write(content)

