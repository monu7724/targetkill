class_name MaterialLibrary
extends RefCounted

const MATERIALS = {
	"concrete": "res://resources/materials/mat_concrete.tres",
	"asphalt": "res://resources/materials/mat_asphalt.tres",
	"steel": "res://resources/materials/mat_steel.tres",
	"aluminum": "res://resources/materials/mat_aluminum.tres",
	"glass": "res://resources/materials/mat_glass.tres",
	"plastic": "res://resources/materials/mat_plastic.tres",
	"rubber": "res://resources/materials/mat_rubber.tres",
	"cloth": "res://resources/materials/mat_cloth.tres",
	"skin": "res://resources/materials/mat_skin.tres",
	"bone": "res://resources/materials/mat_bone.tres",
	"wood": "res://resources/materials/mat_wood.tres",
	"dirt": "res://resources/materials/mat_dirt.tres"
}

static var _cached_materials: Dictionary = {}

static func get_material(mat_name: String) -> Material:
	var key = mat_name.to_lower()
	if _cached_materials.has(key):
		return _cached_materials[key]
		
	if MATERIALS.has(key):
		var path = MATERIALS[key]
		if ResourceLoader.exists(path):
			var res = load(path)
			if res is Material:
				_cached_materials[key] = res
				return res
	return null

static func apply_to_mesh(mesh_instance: MeshInstance3D, mat_name: String, surface_idx: int = 0):
	if not mesh_instance: return
	var mat = get_material(mat_name)
	if mat:
		mesh_instance.set_surface_override_material(surface_idx, mat)
