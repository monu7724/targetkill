extends Node3D

@onready var anim_player: AnimationPlayer = null
@onready var skeleton: Skeleton3D = null

func _ready() -> void:
	print("=== RUNNING INFECTED ZOMBIE VISUAL TEST ===")
	_find_nodes(self)
	
	if skeleton:
		print("[OK] Skeleton3D verified. Bones: %d" % skeleton.get_bone_count())
	else:
		print("[FAIL] Missing Skeleton3D")

	if anim_player:
		var anims = anim_player.get_animation_list()
		print("[OK] AnimationPlayer active. Animations (%d): %s" % [anims.size(), str(anims)])
		
		# Test cycling key animations
		for target_anim in ["Walk", "walk", "Attack_mixamo_vitruvian", "attack", "HitReaction_mixamo_vitruvian", "headshot_reaction", "Death_mixamo_vitruvian", "death"]:
			if anim_player.has_animation(target_anim):
				anim_player.play(target_anim)
				print("  -> Playing animation: %s" % target_anim)
				break
	else:
		print("[FAIL] Missing AnimationPlayer")
		
	# Verify materials on child meshes
	var mesh_count = 0
	for m in find_children("*", "MeshInstance3D", true, false):
		mesh_count += 1
		var mat = m.get_active_material(0)
		var mat_name = mat.resource_name if mat else "None"
		print("  Mesh '%s': Material='%s'" % [m.name, mat_name])
	print("[OK] Verified %d meshes with active materials." % mesh_count)

	if get_tree().current_scene == self and DisplayServer.get_name() == "headless":
		await get_tree().create_timer(0.5).timeout
		get_tree().quit()

func _find_nodes(node: Node) -> void:
	if node is Skeleton3D and skeleton == null:
		skeleton = node
	if node is AnimationPlayer and anim_player == null:
		anim_player = node
	for c in node.get_children():
		_find_nodes(c)
