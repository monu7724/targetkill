extends Node3D

func _ready() -> void:
	print("=== RUNNING CITY PROPS TEST (Coding Creature CC0) ===")
	var count = 0
	for child in get_children():
		if child is Node3D and child.name.begins_with("Prop_"):
			count += 1
			print("[OK] Verified prop loaded: %s at %s" % [child.name, str(child.position)])
	print("[OK] Total verified urban props in scene: %d" % count)
	
	if DisplayServer.get_name() == "headless":
		await get_tree().create_timer(0.5).timeout
		get_tree().quit()
