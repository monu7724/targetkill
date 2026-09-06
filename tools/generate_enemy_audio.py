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
        max_val = max(max(abs(s) for s in samples), 0.001)
        scaling = 28000.0 / max_val if max_val > 1.0 else 28000.0
        frames = bytearray()
        for s in samples:
            val = int(max(-32767, min(32767, s * scaling)))
            frames.extend(struct.pack('<h', val))
        wav_file.writeframes(frames)
    print(f"Generated {filepath} ({len(samples)/sample_rate:.2f}s)")

def gen_dog_bark():
    # Raspy guttural canine bark / snarl
    duration = 0.65
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        env = math.exp(-6.0 * t) if t < 0.2 else math.exp(-8.0 * (t - 0.2)) * 0.8
        f0 = 260.0 - 90.0 * (t / duration)
        growl = math.sin(2.0 * math.pi * f0 * t) + 0.5 * math.sin(2.0 * math.pi * (f0 * 1.5) * t)
        v = (growl * 0.6 + noise * 0.4) * env
        samples.append(v)
    return samples

def gen_dog_attack():
    # Vicious snappy biting attack snap
    duration = 0.5
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        noise = (random.random() * 2.0 - 1.0)
        # Snarl into tooth-clack
        env = math.exp(-12.0 * t)
        snap = math.sin(2.0 * math.pi * 950.0 * math.exp(-40.0 * t) * t) * math.exp(-35.0 * t)
        f0 = 340.0 * math.exp(-15.0 * t)
        growl = math.sin(2.0 * math.pi * f0 * t)
        v = (growl * 0.4 + noise * 0.3 + snap * 0.5) * env
        samples.append(v)
    return samples

def gen_dog_death():
    # Pained yelping whimper / collapse
    duration = 1.1
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = math.exp(-3.5 * t)
        f0 = 750.0 - 450.0 * (t / duration)
        vibrato = math.sin(2.0 * math.pi * 14.0 * t) * 40.0
        yelp = math.sin(2.0 * math.pi * (f0 + vibrato) * t)
        breath = (random.random() * 2.0 - 1.0) * math.exp(-5.0 * t) * 0.25
        v = (yelp * 0.7 + breath) * env
        samples.append(v)
    return samples

def gen_boss_slam():
    # Massive ground slam shockwave rumble
    duration = 1.4
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        impact = (random.random() * 2.0 - 1.0) * math.exp(-25.0 * t)
        sub = math.sin(2.0 * math.pi * 48.0 * math.exp(-6.0 * t) * t) * math.exp(-3.5 * t)
        rumble = math.sin(2.0 * math.pi * 75.0 * t) * math.exp(-2.5 * t)
        v = impact * 0.5 + sub * 0.8 + rumble * 0.4
        samples.append(v)
    return samples

def gen_boss_roar():
    # Deep earth-shaking mutant beast roar
    duration = 2.2
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        env = (t / 0.3) if t < 0.3 else math.exp(-1.5 * (t - 0.3))
        f0 = 110.0 + 35.0 * math.sin(2.0 * math.pi * 3.5 * t)
        f1 = f0 * 1.5
        noise = (random.random() * 2.0 - 1.0) * 0.35
        roar = math.sin(2.0 * math.pi * f0 * t) * 0.6 + math.sin(2.0 * math.pi * f1 * t) * 0.3
        v = (roar + noise) * env
        samples.append(v)
    return samples

if __name__ == '__main__':
    write_wav("audio/zombies/sfx_dog_bark.wav", gen_dog_bark())
    write_wav("audio/zombies/sfx_dog_attack.wav", gen_dog_attack())
    write_wav("audio/zombies/sfx_dog_death.wav", gen_dog_death())
    write_wav("audio/zombies/sfx_boss_slam.wav", gen_boss_slam())
    write_wav("audio/zombies/sfx_boss_roar.wav", gen_boss_roar())
    print("Enemy audio generated successfully.")
