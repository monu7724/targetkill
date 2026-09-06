extends SceneTree

func _init():
	var sc = load("res://scenes/environments/AirportTerminal.tscn")
	var inst = sc.instantiate()
	for m in inst.find_children("*", "MeshInstance3D", true, false):
		var mesh_name = m.mesh.resource_path if m.mesh else "no mesh"
		print(m.name, " parent: ", m.get_parent().name, " mesh: ", mesh_name, " pos: ", m.global_position)
		for s in range(m.get_surface_override_material_count()):
			print("  override mat ", s, ": ", m.get_surface_override_material(s))
	inst.free()
	quit()
