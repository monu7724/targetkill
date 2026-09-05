#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

command="$1"

case "$command" in
    run_tests)
        echo "=== RUNNING AUTOMATED UNIT & INTEGRATION TESTS ==="
        godot --headless --path "$PROJECT_DIR" scenes/test/TestRunner.tscn
        echo "=== RUNNING VISUAL ACCEPTANCE TEST ==="
        godot --headless -s scripts/Tools/test_visual_acceptance.gd
        ;;
    validate_assets)
        echo "=== VALIDATING 3D GLB ASSETS ==="
        for f in assets/3d/characters/*.glb assets/3d/weapons/*.glb assets/3d/zombies/*.glb assets/3d/environments/*.glb; do
            if [ -f "$f" ]; then
                echo "[OK] $(basename "$f") ($(du -h "$f" | cut -f1))"
            else
                echo "[FAIL] Missing $f"
                exit 1
            fi
        done
        ;;
    validate_android)
        echo "=== VALIDATING ANDROID CONFIGURATION ==="
        if command -v apksigner >/dev/null 2>&1 || [ -f "/opt/android-sdk/build-tools/34.0.0/apksigner" ]; then
            echo "[OK] apksigner located"
        fi
        godot --headless --editor --quit
        echo "[OK] Godot editor scan succeeded"
        ;;
    build_debug|build_apk)
        echo "=== EXPORTING SIGNED ANDROID DEBUG APK ==="
        godot --headless --export-debug "Android" "$PROJECT_DIR/SectorZero-Lockdown-debug.apk"
        ls -lh "$PROJECT_DIR/SectorZero-Lockdown-debug.apk"
        sha256sum "$PROJECT_DIR/SectorZero-Lockdown-debug.apk"
        ;;
    *)
        echo "Usage: $0 {run_tests|validate_assets|validate_android|build_debug|build_apk}"
        exit 1
        ;;
esac
