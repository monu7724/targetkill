extends SceneTree

func _init():
    print("==================================================")
    print("  ALL 8 ENEMY VARIANTS VERIFICATION TEST SUITE    ")
    print("==================================================")
    await process_frame
    
    var zombie_scene = load("res://scenes/zombies/Zombie.tscn")
    assert(zombie_scene != null, "Zombie.tscn must load")
    
    var variants_to_test = [
        {"type": "normal", "hp": 50.0, "speed": 1.4, "range": 1.7},
        {"type": "fast", "hp": 30.0, "speed": 2.8, "range": 1.7},
        {"type": "heavy", "hp": 160.0, "speed": 0.8, "range": 2.2},
        {"type": "special", "hp": 40.0, "speed": 1.2, "range": 14.0},
        {"type": "spitter", "hp": 40.0, "speed": 1.2, "range": 14.0},
        {"type": "dog", "hp": 50.0, "speed": 4.5, "range": 2.0},
        {"type": "rat", "hp": 15.0, "speed": 3.8, "range": 1.2},
        {"type": "rats", "hp": 15.0, "speed": 3.8, "range": 1.2},
        {"type": "bat", "hp": 12.0, "speed": 3.6, "range": 1.5, "fly_height": 2.2},
        {"type": "bats", "hp": 12.0, "speed": 3.6, "range": 1.5, "fly_height": 2.2},
        {"type": "boss", "hp": 500.0, "speed": 1.1, "range": 2.5}
    ]
    
    for v in variants_to_test:
        var e = zombie_scene.instantiate()
        e.archetype = v["type"]
        root.add_child(e)
        await process_frame
        
        assert(e.health_component.max_health == v["hp"], "Variant %s HP must be %f" % [v["type"], v["hp"]])
        assert(e.move_speed == v["speed"], "Variant %s speed must be %f" % [v["type"], v["speed"]])
        assert(e.attack_range == v["range"], "Variant %s attack_range must be %f" % [v["type"], v["range"]])
        if v.has("fly_height"):
            assert(e.fly_height == v["fly_height"], "Variant %s fly_height must be %f" % [v["type"], v["fly_height"]])
            
        print("[PASS] Variant '%s' successfully configured: HP=%.1f, Speed=%.1f, Range=%.1f" % [
            v["type"], e.health_component.max_health, e.move_speed, e.attack_range
        ])
        e.queue_free()
        await process_frame
        
    print("\n[PASS] All 8 variants verified successfully in Zombie/EnemyBase hierarchy!")
    quit(0)
