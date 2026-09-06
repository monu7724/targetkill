#!/usr/bin/env python3
"""
Tripo AI v3 -> Godot Asset Pipeline
Downloads and validates AI-generated 3D GLB assets from Tripo AI v3.
Strictly reads TRIPO_API_KEY from environment variables.
Never hardcodes or prints API credentials.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

TRIPO_API_BASE = "https://openapi.tripo3d.ai/v3"

PLANNED_ASSETS = [
    {
        "id": "zombie",
        "name": "Realistic Infected Zombie",
        "destination": "assets/ai_generated/zombie/tripo_zombie_security.glb",
        "prompt": (
            "realistic adult male infected zombie for a mobile survival horror FPS game, "
            "natural human anatomy and proportions, worn airport security uniform, "
            "realistic skin and clothing materials, subtle viral infection, "
            "dirty worn fabric, realistic hands and feet, full body, "
            "neutral T-pose suitable for rigging, "
            "high quality PBR textures, realistic game asset, "
            "optimized topology, no fantasy creature anatomy, "
            "no exaggerated mutations"
        ),
        "params": {
            "texture": True,
            "pbr": True,
        }
    },
    {
        "id": "infected_dog",
        "name": "Infected Dog",
        "destination": "assets/ai_generated/infected_dog/tripo_infected_dog.glb",
        "prompt": (
            "realistic infected stray dog for a mobile survival horror FPS game, "
            "accurate canine anatomy and proportions, dirty worn fur, "
            "subtle viral infection, realistic materials, "
            "full body standing quadruped pose, "
            "game-ready optimized mesh, PBR textures, "
            "realistic survival horror style, no fantasy monster anatomy"
        ),
        "params": {
            "texture": True,
            "pbr": True,
        }
    },
    {
        "id": "rifle",
        "name": "Realistic FPS Assault Rifle",
        "destination": "assets/ai_generated/weapons/tripo_assault_rifle.glb",
        "prompt": (
            "high-detail realistic modern assault rifle for a mobile FPS game, "
            "realistic metal and polymer materials, detailed receiver, "
            "magazine, sights and barrel, realistic proportions, "
            "PBR textures, game-ready optimized mesh, "
            "no logos, no brand markings, isolated object"
        ),
        "params": {
            "texture": True,
            "pbr": True,
        }
    }
]

def get_api_key():
    key = os.environ.get("TRIPO_API_KEY", "").strip()
    if not key:
        print("[ERROR] TRIPO_API_KEY environment variable is not set.", file=sys.stderr)
        print("Please configure it before running: export TRIPO_API_KEY=\"your_key_here\"", file=sys.stderr)
        sys.exit(1)
    return key

def make_request(url, data=None, headers=None):
    if headers is None:
        headers = {}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return json.loads(body)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8', errors='ignore')
        print(f"[HTTP ERROR {e.code}] {e.reason}: {err_msg}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"[NETWORK ERROR] {e}", file=sys.stderr)
        raise

def create_task(api_key, asset_spec):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "prompt": asset_spec["prompt"],
        "texture": asset_spec["params"].get("texture", True),
        "pbr": asset_spec["params"].get("pbr", True)
    }
    
    endpoints = [
        f"{TRIPO_API_BASE}/generation/text-to-model",
        f"{TRIPO_API_BASE}/tasks"
    ]
    
    data = json.dumps(payload).encode('utf-8')
    for endpoint in endpoints:
        try:
            print(f"[TRIPO] Submitting task to {endpoint}...")
            res = make_request(endpoint, data=data, headers=headers)
            task_id = None
            if isinstance(res, dict):
                if "data" in res and isinstance(res["data"], dict):
                    task_id = res["data"].get("task_id") or res["data"].get("id")
                elif "task_id" in res:
                    task_id = res["task_id"]
                elif "id" in res:
                    task_id = res["id"]
            if task_id:
                print(f"[TRIPO] Task created successfully: {task_id}")
                return task_id, res
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
    raise RuntimeError("Failed to create task with Tripo API endpoints.")

def poll_task(api_key, task_id, poll_interval=5, max_wait=600):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    endpoint = f"{TRIPO_API_BASE}/tasks/{task_id}"
    start_time = time.time()
    
    print(f"[TRIPO] Polling task {task_id} (timeout: {max_wait}s)...")
    while time.time() - start_time < max_wait:
        res = make_request(endpoint, headers=headers)
        data = res.get("data", res)
        status = data.get("status", "").lower()
        progress = data.get("progress", 0)
        print(f"[TRIPO] Task {task_id} status: {status} ({progress}%)")
        
        if status in ("success", "completed"):
            return data
        elif status in ("failed", "error", "cancelled"):
            err_details = data.get("error", "Unknown error")
            raise RuntimeError(f"Tripo task {task_id} ended with status '{status}': {err_details}")
        
        time.sleep(poll_interval)
    
    raise TimeoutError(f"Tripo task {task_id} timed out after {max_wait} seconds.")

def validate_glb(filepath):
    if not os.path.exists(filepath):
        return False, "File does not exist"
    size = os.path.getsize(filepath)
    if size == 0:
        return False, "File size is 0 bytes"
    with open(filepath, "rb") as f:
        magic = f.read(4)
        if magic != b"glTF":
            return False, f"Invalid GLB magic header: {magic} (expected b'glTF')"
        version = int.from_bytes(f.read(4), "little")
        total_len = int.from_bytes(f.read(4), "little")
        return True, f"Valid glTF binary v{version}, size: {size} bytes ({size / (1024*1024):.2f} MB)"

def download_asset(model_url, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print(f"[DOWNLOAD] Downloading model to {dest_path}...")
    urllib.request.urlretrieve(model_url, dest_path)
    valid, reason = validate_glb(dest_path)
    if not valid:
        raise ValueError(f"Downloaded model is not a valid GLB: {reason}")
    print(f"[OK] {dest_path} verified: {reason}")
    return os.path.getsize(dest_path)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("=== TRIPO AI ASSET PIPELINE (DRY RUN) ===")
        print(f"Total planned assets: {len(PLANNED_ASSETS)}")
        for idx, a in enumerate(PLANNED_ASSETS, 1):
            print(f"\n[{idx}/{len(PLANNED_ASSETS)}] {a['name']}")
            print(f"  Destination: {a['destination']}")
            print(f"  Prompt: {a['prompt']}")
            print(f"  PBR: {a['params']['pbr']} | Texture: {a['params']['texture']}")
        print("\nDry run completed.")
        return

    api_key = get_api_key()
    print("=== STARTING TRIPO AI GENERATION PIPELINE ===")
    print(f"Processing {len(PLANNED_ASSETS)} assets...")

if __name__ == "__main__":
    main()
