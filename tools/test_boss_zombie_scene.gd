extends SceneTree

func _init():
    print("--- UNIT TEST: DEDICATED BOSS ZOMBIE SCENE ---")
    await process_frame
    
    var event_bus = root.get_node_or_null("EventBus")
    assert(event_bus != null, "EventBus must be found in tree")
    
    var state = {
        "spawned": false,
        "name": "",
        "hp": 0.0,
        "health_changed": false,
        "cur_hp": 0.0
    }
    
    event_bus.boss_spawned.connect(func(bname, hp):
        state["spawned"] = true
        state["name"] = bname
        state["hp"] = hp
    )
    
    event_bus.boss_health_changed.connect(func(cur, max_hp):
        state["health_changed"] = true
        state["cur_hp"] = cur
    )
    
    var scene = load("res://scenes/zombies/BossZombie.tscn")
    assert(scene != null, "BossZombie.tscn must load")
    
    var boss = scene.instantiate()
    assert(boss != null, "BossZombie must instantiate")
    assert(boss.is_in_group("zombies"), "Boss must be in zombies group")
    assert(boss.archetype == "boss", "Archetype must be boss")
    assert(boss.move_speed == 1.2, "Move speed must be 1.2")
    assert(boss.attack_range == 3.0, "Attack range must be 3.0")
    
    root.add_child(boss)
    await process_frame
    
    assert(boss.health_component.max_health == 500.0, "Boss max health must be 500.0")
    assert(state["spawned"] == true, "EventBus.boss_spawned must have been emitted")
    assert(state["name"] == "THE ALPHA MUTANT", "Boss name must match")
    assert(state["hp"] == 500.0, "Boss initial max HP must match")
    print("[PASS] EventBus.boss_spawned verified: %s, HP: %f" % [state["name"], state["hp"]])
    
    # HitZones
    var head_zone: HitZone = boss.get_node_or_null("HeadHitZone")
    var chest_zone: HitZone = boss.get_node_or_null("ChestHitZone")
    assert(head_zone != null, "HeadHitZone must exist")
    assert(chest_zone != null, "ChestHitZone must exist")
    
    # Take damage and verify EventBus.boss_health_changed
    head_zone.take_hit(20.0) # 20 * 2.5 = 50 damage
    assert(state["health_changed"] == true, "EventBus.boss_health_changed must have been emitted")
    assert(state["cur_hp"] == 450.0, "HP must be 450.0")
    print("[PASS] EventBus.boss_health_changed verified: Current HP = %f" % state["cur_hp"])
    
    # Check 24 bones and ScytheBlade
    var skel: Skeleton3D = boss.find_child("Skeleton3D", true, false)
    assert(skel != null, "Skeleton3D must exist in boss")
    assert(skel.get_bone_count() == 24, "Boss armature must have 24 bones")
    var has_scythe = false
    for i in range(skel.get_bone_count()):
        if skel.get_bone_name(i) == "ScytheBlade":
            has_scythe = true
    assert(has_scythe, "Boss must have ScytheBlade bone")
    print("[PASS] Boss 24-bone armature with ScytheBlade verified")
    
    # Animations
    assert(boss.active_anim_player != null, "Active anim player must exist")
    var anims = boss.active_anim_player.get_animation_list()
    for a in ["idle", "walk", "attack_windup", "heavy_attack", "roar", "hit", "stagger", "death"]:
        assert(anims.has(a), "Boss must have animation: " + a)
    print("[PASS] All required boss animations verified")
    
    boss.queue_free()
    rm_temp_debug()
    print("ALL DEDICATED BOSS ZOMBIE TESTS PASSED!")
    quit(0)

func rm_temp_debug():
    var dir = DirAccess.open("res://tools")
    if dir and dir.file_exists("test_boss_debug.gd"):
        dir.remove("test_boss_debug.gd")
