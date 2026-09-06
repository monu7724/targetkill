extends SceneTree

func _init() -> void:
	print("Capturing 1280x720 previews with SubViewport...")
	var vp = SubViewport.new()
	vp.size = Vector2i(1280, 720)
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	
	await _capture(vp, "res://assets_tests/RealHumanTest.tscn", "assets_tests/preview_human.png")
	await _capture(vp, "res://assets_tests/InfectedZombieTest.tscn", "assets_tests/preview_zombie.png")
	await _capture(vp, "res://assets_tests/Zombie360Test.tscn", "assets_tests/preview_360test.png")
	await _capture(vp, "res://scenes/environments/AirportTerminal.tscn", "assets_tests/preview_mission1.png", 40)
	await _capture(vp, "res://assets_tests/CityPropsTest.tscn", "assets_tests/preview_props.png")
	await _capture(vp, "res://assets_tests/PBRMaterialTest.tscn", "assets_tests/preview_materials.png")
	
	print("Completed preview capture.")
	quit()

func _capture(vp: SubViewport, path: String, out_path: String, frames: int = 10) -> void:
	var scene = load(path) as PackedScene
	if not scene:
		print("Failed loading ", path)
		return
	var inst = scene.instantiate()
	vp.add_child(inst)
	
	# Wait several frames for rendering
	for i in range(frames):
		await process_frame
	
	var img = vp.get_texture().get_image()
	if img:
		img.save_png(out_path)
		print("[OK] Saved: ", out_path, " size: ", img.get_size())
	else:
		print("[FAIL] No image from viewport")
	
	inst.queue_free()
	for i in range(3):
		await process_frame
