import zlib
import struct
import math
import random
import os

def write_png(filename, width, height, rgb_bytes):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + rgb_bytes[y * width * 3 : (y + 1) * width * 3] for y in range(height))
    idat = zlib.compress(raw, 6)
    
    with open(filename, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', ihdr))
        f.write(chunk(b'IDAT', idat))
        f.write(chunk(b'IEND', b''))
    print(f"Generated texture: {filename} ({width}x{height})")

def clamp(v, low=0, high=255):
    return int(max(low, min(high, v)))

def gen_weapon_metal(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            # Dark steel base (30-45) with fine brushed noise
            noise = random.randint(-6, 6)
            streak = int(math.sin(x * 0.1) * 3)
            val = clamp(38 + noise + streak)
            # Slight blueish gunmetal tint
            buf[idx] = clamp(val - 3)
            buf[idx+1] = clamp(val)
            buf[idx+2] = clamp(val + 5)
    return write_png('textures/pbr/tex_weapon_metal.png', size, size, bytes(buf))

def gen_swat_camo(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            # Ripstop grid
            grid = 6 if (x % 16 == 0 or y % 16 == 0) else 0
            noise = random.randint(-8, 8)
            base = 42 + grid + noise
            buf[idx] = clamp(base - 8)
            buf[idx+1] = clamp(base - 4)
            buf[idx+2] = clamp(base + 8)
    return write_png('textures/pbr/tex_swat_camo.png', size, size, bytes(buf))

def gen_zombie_normal(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-12, 12)
            # Sickly rotting olive green / pale flesh
            r = clamp(85 + noise)
            g = clamp(105 + noise)
            b = clamp(75 + noise)
            # Blood splatter patches
            if (x - 80)**2 + (y - 120)**2 < 1200 or (x - 190)**2 + (y - 70)**2 < 800:
                r = clamp(130 + random.randint(-15, 15))
                g = clamp(20 + random.randint(-10, 10))
                b = clamp(20 + random.randint(-10, 10))
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
    return write_png('textures/pbr/tex_zombie_normal.png', size, size, bytes(buf))

def gen_zombie_fast(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-10, 10)
            # Pale desiccated corpse flesh with crimson veining
            r = clamp(130 + noise)
            g = clamp(115 + noise)
            b = clamp(110 + noise)
            # Veins
            if (x * 3 + y * 2) % 32 < 2:
                r = clamp(110)
                g = clamp(30)
                b = clamp(40)
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
    return write_png('textures/pbr/tex_zombie_fast.png', size, size, bytes(buf))

def gen_zombie_heavy(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-8, 8)
            # Dark necrotic bruised skin (slate grey/purple)
            r = clamp(65 + noise)
            g = clamp(60 + noise)
            b = clamp(70 + noise)
            # Armored vest plate strip
            if 60 < y < 180 and 40 < x < 216:
                r = clamp(35 + noise)
                g = clamp(38 + noise)
                b = clamp(42 + noise)
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
    return write_png('textures/pbr/tex_zombie_heavy.png', size, size, bytes(buf))

def gen_zombie_boss(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-15, 15)
            # Deep mutated crimson & black carapace
            base = clamp(45 + noise)
            r = clamp(base + 50)
            g = clamp(base - 10)
            b = clamp(base - 10)
            # Glowing infected magma veins
            if ((x * 5 + y * 3) % 40 < 3) or ((x - 128)**2 + (y - 128)**2 < 400):
                r = clamp(235 + random.randint(-15, 15))
                g = clamp(60 + random.randint(-15, 15))
                b = clamp(20)
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
    return write_png('textures/pbr/tex_zombie_boss.png', size, size, bytes(buf))

def gen_airport_tile(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            # 64x64 tile grout lines
            is_grout = (x % 64 < 2) or (y % 64 < 2)
            if is_grout:
                r, g, b = 60, 62, 65
            else:
                noise = random.randint(-6, 6)
                # Polished light grey terrazzo
                val = clamp(180 + noise)
                r, g, b = val - 4, val, val + 6
            buf[idx] = r
            buf[idx+1] = g
            buf[idx+2] = b
    return write_png('textures/pbr/tex_airport_tile.png', size, size, bytes(buf))

def gen_station_concrete(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-12, 12)
            val = clamp(110 + noise)
            r, g, b = val, val, val
            # Yellow safety tactile warning strip at top
            if 0 <= y < 35:
                r, g, b = 210 + noise//2, 175 + noise//2, 30
            buf[idx] = clamp(r)
            buf[idx+1] = clamp(g)
            buf[idx+2] = clamp(b)
    return write_png('textures/pbr/tex_station_concrete.png', size, size, bytes(buf))

def gen_train_metal(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-5, 5)
            # Brushed stainless steel with dark blue stripe
            val = clamp(160 + noise)
            r, g, b = val, val + 2, val + 5
            if 100 < y < 140: # Metro corporate stripe
                r, g, b = 25, 80, 150
            buf[idx] = clamp(r)
            buf[idx+1] = clamp(g)
            buf[idx+2] = clamp(b)
    return write_png('textures/pbr/tex_train_metal.png', size, size, bytes(buf))

def gen_industrial_asphalt(size=256):
    buf = bytearray(size * size * 3)
    for y in range(size):
        for x in range(size):
            idx = (y * size + x) * 3
            noise = random.randint(-14, 14)
            val = clamp(55 + noise)
            # White parking / road line
            if 120 < x < 136:
                val = clamp(190 + noise)
            buf[idx] = val
            buf[idx+1] = val
            buf[idx+2] = val
    return write_png('textures/pbr/tex_industrial_asphalt.png', size, size, bytes(buf))

if __name__ == '__main__':
    gen_weapon_metal()
    gen_swat_camo()
    gen_zombie_normal()
    gen_zombie_fast()
    gen_zombie_heavy()
    gen_zombie_boss()
    gen_airport_tile()
    gen_station_concrete()
    gen_train_metal()
    gen_industrial_asphalt()
    print("All PBR textures generated successfully!")
