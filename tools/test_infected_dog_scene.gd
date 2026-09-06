extends SceneTree

func _init():
    print("--- UNIT TEST: DEDICATED INFECTED DOG SCENE ---")
    var scene = load("res://scenes/zombies/InfectedDog.tscn")
    assert(scene != null, "InfectedDog.tscn must load")
    
    var dog = scene.instantiate()
    assert(dog != null, "InfectedDog must instantiate")
    assert(dog.is_in_group("zombies"), "Dog must be in zombies group")
    assert(dog.move_speed == 4.5, "Dog move speed must be 4.5")
    assert(dog.attack_range == 2.0, "Dog attack range must be 2.0")
    assert(dog.attack_damage == 12.0, "Dog attack damage must be 12.0")
    
    root.add_child(dog)
    await process_frame
    
    # HitZone checks
    var head_zone: HitZone = dog.get_node_or_null("HeadHitZone")
    var body_zone: HitZone = dog.get_node_or_null("BodyHitZone")
    assert(head_zone != null, "HeadHitZone must exist")
    assert(body_zone != null, "BodyHitZone must exist")
    
    assert(head_zone.zone_type == HitZone.ZoneType.HEAD, "HeadHitZone must be HEAD zone_type (0)")
    assert(head_zone.damage_multiplier == 2.5, "HeadHitZone damage_multiplier must be 2.5")
    
    assert(body_zone.zone_type == HitZone.ZoneType.CHEST, "BodyHitZone must be CHEST zone_type (1)")
    assert(body_zone.damage_multiplier == 1.0, "BodyHitZone damage_multiplier must be 1.0")
    
    # Check positions
    print("Head position:", head_zone.position, "Expected: (0, 0.52, -0.45)")
    assert(head_zone.position.is_equal_approx(Vector3(0, 0.52, -0.45)), "HeadHitZone position mismatch")
    print("Body position:", body_zone.position, "Expected: (0, 0.38, 0.05)")
    assert(body_zone.position.is_equal_approx(Vector3(0, 0.38, 0.05)), "BodyHitZone position mismatch")
    
    # Check take_hit on HitZones
    var initial_hp = dog.health_component.current_health
    var r_head = head_zone.take_hit(10.0, Vector3.FORWARD)
    assert(r_head.is_headshot == true, "Headshot flag must be true")
    assert(r_head.final_damage == 25.0, "Final damage for 10 base on head must be 25.0")
    assert(dog.health_component.current_health == initial_hp - 25.0, "HP must drop by 25")
    
    var r_body = body_zone.take_hit(10.0, Vector3.FORWARD)
    assert(r_body.is_headshot == false, "Headshot flag on body must be false")
    assert(r_body.final_damage == 10.0, "Final damage for 10 base on body must be 10.0")
    assert(dog.health_component.current_health == initial_hp - 35.0, "HP must drop by another 10")
    
    # Check animations on dog
    assert(dog.active_anim_player != null, "Dog active_anim_player must not be null")
    var anims = dog.active_anim_player.get_animation_list()
    print("Dog animations:", anims)
    for a in ["run", "attack", "hit_head", "hit_body", "death"]:
        assert(anims.has(a), "Dog must have animation: " + a)
    print("[PASS] All required dog animations verified")
    
    # Check 18 bones
    var skel: Skeleton3D = dog.find_child("Skeleton3D", true, false)
    assert(skel != null, "Skeleton3D must exist")
    assert(skel.get_bone_count() == 18, "Dog armature must have 18 bones")
    print("[PASS] Dog 18-bone quadruped armature verified")
    
    dog.queue_free()
    print("ALL DEDICATED INFECTED DOG TESTS PASSED!")
    quit(0)
