extends Node3D

@onready var anim_player: AnimationPlayer = null
@onready var skeleton: Skeleton3D = null

func _ready() -> void:
	print("=== RUNNING REAL HUMAN TEST (Vitruvian CC0) ===")
	_find_skeleton_and_anim(self)
	
	if skeleton:
		print("[OK] Skeleton3D located. Bone count: ", skeleton.get_bone_count())
		for i in range(mini(8, skeleton.get_bone_count())):
			print("  Bone %d: %s" % [i, skeleton.get_bone_name(i)])
	else:
		print("[WARN] Skeleton3D not found!")

	if anim_player:
		var anim_list = anim_player.get_animation_list()
		print("[OK] AnimationPlayer located. Total animations: ", anim_list.size())
		for a in anim_list:
			print("  Animation: ", a)
		
		if anim_player.has_animation("Walk"):
			anim_player.play("Walk")
			print("[OK] Walk animation started successfully.")
	else:
		print("[WARN] AnimationPlayer not found!")

	# Auto-exit if run non-interactively
	if get_tree().current_scene == self and (OS.has_feature("template") or DisplayServer.get_name() == "headless"):
		await get_tree().create_timer(0.5).timeout
		get_tree().quit()

func _find_skeleton_and_anim(node: Node) -> void:
	if node is Skeleton3D and skeleton == null:
		skeleton = node
	if node is AnimationPlayer and anim_player == null:
		anim_player = node
	for child in node.get_children():
		_find_skeleton_and_anim(child)
