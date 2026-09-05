import wave
import struct
import math
import random
import os

SAMPLE_RATE = 44100

def write_wav(filepath, samples, sample_rate=SAMPLE_RATE):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1) # mono
        wav_file.setsampwidth(2) # 16-bit
        wav_file.setframerate(sample_rate)
        # Normalize to avoid clipping
        max_val = max(max(abs(s) for s in samples), 0.001)
        scaling = 30000.0 / max_val if max_val > 1.0 else 30000.0
        frames = bytearray()
        for s in samples:
            val = int(max(-32767, min(32767, s * scaling)))
            frames.extend(struct.pack('<h', val))
        wav_file.writeframes(frames)
    print(f"Generated {filepath} ({len(samples)/sample_rate:.2f}s)")

def gen_noise(duration, decay=5.0):
    samples = []
    n = int(SAMPLE_RATE * duration)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-decay * t)
        val = (random.random() * 2.0 - 1.0) * env
        samples.append(val)
    return samples

def gen_pistol_shot():
    # Crisp punchy gunshot with fast attack, noise burst and body resonance
    duration = 0.45
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        env = math.exp(-18.0 * t)
        body = math.sin(2.0 * math.pi * 140.0 * math.exp(-30.0 * t) * t) * math.exp(-12.0 * t)
        click = math.sin(2.0 * math.pi * 1200.0 * t) * math.exp(-60.0 * t)
        s = (noise * 0.7 + body * 0.5 + click * 0.3) * env
        samples.append(s)
    return samples

def gen_rifle_shot():
    # Snappy crack with rapid metallic punch
    duration = 0.35
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        env = math.exp(-22.0 * t)
        body = math.sin(2.0 * math.pi * 180.0 * math.exp(-40.0 * t) * t) * math.exp(-15.0 * t)
        mech = math.sin(2.0 * math.pi * 2400.0 * t) * math.exp(-80.0 * t)
        s = (noise * 0.8 + body * 0.4 + mech * 0.4) * env
        samples.append(s)
    return samples

def gen_shotgun_shot():
    # Heavy explosive blast with deep sub rumble
    duration = 0.7
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        env = math.exp(-9.0 * t)
        sub = math.sin(2.0 * math.pi * 65.0 * math.exp(-10.0 * t) * t) * math.exp(-8.0 * t)
        mid = math.sin(2.0 * math.pi * 220.0 * t) * math.exp(-15.0 * t)
        s = (noise * 0.85 + sub * 0.8 + mid * 0.3) * env
        samples.append(s)
    return samples

def gen_empty_click():
    duration = 0.1
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-70.0 * t)
        click = math.sin(2.0 * math.pi * 2800.0 * t) * env
        samples.append(click)
    return samples

def gen_reload():
    # Click-slide-click reload sound
    duration = 1.2
    n = int(SAMPLE_RATE * duration)
    samples = [0.0] * n
    def add_click(start_t, freq, decay):
        start_idx = int(start_t * SAMPLE_RATE)
        for i in range(int(0.08 * SAMPLE_RATE)):
            idx = start_idx + i
            if idx < n:
                t = i / SAMPLE_RATE
                val = math.sin(2.0 * math.pi * freq * t) * math.exp(-decay * t)
                val += (random.random() * 2.0 - 1.0) * math.exp(-decay * t) * 0.3
                samples[idx] += val * 0.6
    add_click(0.05, 1800, 50)  # Mag release
    add_click(0.5, 900, 40)    # Mag insert
    add_click(0.9, 2400, 60)   # Slide rack forward
    return samples

def gen_zombie_growl():
    duration = 1.4
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.sin(math.pi * (t / duration)) ** 1.5
        # Low frequency AM modulated growl
        mod = math.sin(2.0 * math.pi * 14.0 * t) * 0.5 + 0.5
        pitch = 75.0 + math.sin(2.0 * math.pi * 2.5 * t) * 20.0
        tone = math.sin(2.0 * math.pi * pitch * t) + 0.5 * math.sin(2.0 * math.pi * pitch * 2.2 * t)
        noise = (random.random() * 2.0 - 1.0) * 0.4
        s = (tone * mod + noise) * env * 0.8
        samples.append(s)
    return samples

def gen_zombie_attack():
    duration = 0.9
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-3.5 * t)
        pitch = 140.0 - (t / duration) * 60.0
        tone = math.sin(2.0 * math.pi * pitch * t)
        noise = (random.random() * 2.0 - 1.0) * 0.6
        s = (tone * 0.7 + noise) * env
        samples.append(s)
    return samples

def gen_zombie_death():
    duration = 1.5
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-2.2 * t)
        pitch = max(35.0, 95.0 - (t / duration) * 70.0)
        tone = math.sin(2.0 * math.pi * pitch * t)
        noise = (random.random() * 2.0 - 1.0) * 0.3
        s = (tone * 0.8 + noise) * env
        samples.append(s)
    return samples

def gen_impact_concrete():
    duration = 0.2
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-35.0 * t)
        noise = (random.random() * 2.0 - 1.0) * env
        chip = math.sin(2.0 * math.pi * 3200.0 * t) * env * 0.5
        samples.append(noise + chip)
    return samples

def gen_impact_flesh():
    duration = 0.25
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-25.0 * t)
        thud = math.sin(2.0 * math.pi * 90.0 * t) * env
        squish = (random.random() * 2.0 - 1.0) * math.exp(-40.0 * t) * 0.6
        samples.append(thud + squish)
    return samples

def gen_footstep():
    duration = 0.15
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-30.0 * t)
        thump = math.sin(2.0 * math.pi * 70.0 * t) * env * 0.7
        scuff = (random.random() * 2.0 - 1.0) * math.exp(-45.0 * t) * 0.4
        samples.append(thump + scuff)
    return samples

def gen_ui_click():
    duration = 0.06
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-80.0 * t)
        s = math.sin(2.0 * math.pi * 1500.0 * t) * env
        samples.append(s)
    return samples

def gen_victory():
    # Major triad fanfare: C4, E4, G4, C5
    notes = [261.63, 329.63, 392.00, 523.25]
    duration = 2.2
    n = int(SAMPLE_RATE * duration)
    samples = [0.0] * n
    for idx, freq in enumerate(notes):
        st = idx * 0.35
        start_idx = int(st * SAMPLE_RATE)
        note_len = int(1.2 * SAMPLE_RATE)
        for i in range(note_len):
            cur = start_idx + i
            if cur < n:
                t = i / SAMPLE_RATE
                env = math.exp(-2.5 * t)
                harm = math.sin(2.0 * math.pi * freq * t) + 0.3 * math.sin(2.0 * math.pi * freq * 2.0 * t)
                samples[cur] += harm * env * 0.4
    return samples

def gen_defeat():
    # Descending minor stinger: G4 -> Eb4 -> D4 -> C4
    notes = [392.00, 311.13, 293.66, 261.63]
    duration = 2.5
    n = int(SAMPLE_RATE * duration)
    samples = [0.0] * n
    for idx, freq in enumerate(notes):
        st = idx * 0.45
        start_idx = int(st * SAMPLE_RATE)
        note_len = int(1.4 * SAMPLE_RATE)
        for i in range(note_len):
            cur = start_idx + i
            if cur < n:
                t = i / SAMPLE_RATE
                env = math.exp(-2.0 * t)
                harm = math.sin(2.0 * math.pi * freq * t) + 0.4 * math.sin(2.0 * math.pi * (freq * 0.5) * t)
                samples[cur] += harm * env * 0.45
    return samples

def gen_ambience(duration=5.0, low_hum=60.0):
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        hum = math.sin(2.0 * math.pi * low_hum * t) * 0.25
        sub = math.sin(2.0 * math.pi * (low_hum * 0.5) * t) * 0.15
        wind = (random.random() * 2.0 - 1.0) * 0.05
        # Subtle modulation
        mod = 0.8 + 0.2 * math.sin(2.0 * math.pi * 0.2 * t)
        samples.append((hum + sub + wind) * mod * 0.5)
    return samples

if __name__ == '__main__':
    write_wav('audio/weapons/sfx_pistol_shoot.wav', gen_pistol_shot())
    write_wav('audio/weapons/sfx_rifle_shoot.wav', gen_rifle_shot())
    write_wav('audio/weapons/sfx_shotgun_shoot.wav', gen_shotgun_shot())
    write_wav('audio/weapons/sfx_empty.wav', gen_empty_click())
    write_wav('audio/weapons/sfx_reload.wav', gen_reload())
    
    write_wav('audio/zombies/sfx_zombie_growl.wav', gen_zombie_growl())
    write_wav('audio/zombies/sfx_zombie_attack.wav', gen_zombie_attack())
    write_wav('audio/zombies/sfx_zombie_death.wav', gen_zombie_death())
    
    write_wav('audio/impacts/sfx_impact_concrete.wav', gen_impact_concrete())
    write_wav('audio/impacts/sfx_impact_flesh.wav', gen_impact_flesh())
    
    write_wav('audio/player/sfx_footstep.wav', gen_footstep())
    
    write_wav('audio/ui/sfx_ui_click.wav', gen_ui_click())
    write_wav('audio/ui/sfx_victory.wav', gen_victory())
    write_wav('audio/ui/sfx_defeat.wav', gen_defeat())
    
    write_wav('audio/ambience/sfx_ambience_airport.wav', gen_ambience(5.0, 55.0))
    write_wav('audio/ambience/sfx_ambience_metro.wav', gen_ambience(5.0, 48.0))
    print("All audio files generated successfully!")
