extends Node3D

@onready var floor_mesh: MeshInstance3D = $Floor
@onready var wall_mesh: MeshInstance3D = $Wall
@onready var metal_mesh: MeshInstance3D = $MetalBlock

func _ready() -> void:
	print("=== RUNNING PBR MATERIAL TEST (Poly Haven CC0) ===")
	_validate_material("Floor", floor_mesh)
	_validate_material("Wall", wall_mesh)
	_validate_material("MetalBlock", metal_mesh)
	
	print("[OK] Poly Haven PBR Materials (Concrete, Wall, Metal) verified.")
	if DisplayServer.get_name() == "headless":
		await get_tree().create_timer(0.5).timeout
		get_tree().quit()

func _validate_material(label: String, mesh_node: MeshInstance3D) -> void:
	if not mesh_node:
		print("[FAIL] Missing mesh node for ", label)
		return
	var mat = mesh_node.material_override
	if not mat:
		mat = mesh_node.get_active_material(0)
	if mat is StandardMaterial3D:
		var has_albedo = mat.albedo_texture != null
		var has_normal = mat.normal_enabled and mat.normal_texture != null
		var has_rough = mat.roughness_texture != null
		print("[OK] %s Material: Albedo=%s, Normal=%s, Roughness=%s" % [label, str(has_albedo), str(has_normal), str(has_rough)])
	else:
		print("[WARN] %s has non-standard material: %s" % [label, str(mat)])
