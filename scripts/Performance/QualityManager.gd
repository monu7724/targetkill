extends Node

enum Quality { LOW, MEDIUM, HIGH }

var current_quality: Quality = Quality.MEDIUM

func _ready():
	process_mode = Node.PROCESS_MODE_ALWAYS
	apply_quality(current_quality)

func apply_quality(level: Quality):
	current_quality = level
	match level:
		Quality.LOW:
			setup_low_quality()
		Quality.MEDIUM:
			setup_medium_quality()
		Quality.HIGH:
			setup_high_quality()
			
	_update_shadows(level)
	
	var event_bus = get_node_or_null("/root/EventBus")
	if event_bus:
		var q_name = "LOW" if level == Quality.LOW else ("MEDIUM" if level == Quality.MEDIUM else "HIGH")
		event_bus.quality_changed.emit(q_name)

func setup_low_quality():
	var vp = get_viewport()
	if vp:
		vp.msaa_3d = Viewport.MSAA_DISABLED
		vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
		vp.use_hdr_2d = false
		vp.scaling_3d_scale = 0.85
	_update_environment(false, false, false)

func setup_medium_quality():
	var vp = get_viewport()
	if vp:
		vp.msaa_3d = Viewport.MSAA_2X
		vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA
		vp.use_hdr_2d = true
		vp.scaling_3d_scale = 1.0
	_update_environment(true, false, true)

func setup_high_quality():
	var vp = get_viewport()
	if vp:
		vp.msaa_3d = Viewport.MSAA_4X
		vp.screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA
		vp.use_hdr_2d = true
		vp.scaling_3d_scale = 1.0
	_update_environment(true, true, true)

func _update_shadows(level: Quality):
	var sun = get_tree().root.find_child("DirectionalLight3D", true, false)
	if sun and sun is DirectionalLight3D:
		match level:
			Quality.LOW:
				sun.shadow_enabled = false
			Quality.MEDIUM:
				sun.shadow_enabled = true
				sun.directional_shadow_mode = DirectionalLight3D.SHADOW_ORTHOGONAL
			Quality.HIGH:
				sun.shadow_enabled = true
				sun.directional_shadow_mode = DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS

func _update_environment(glow: bool, ssao: bool, fog: bool):
	var world_env = get_tree().root.find_child("WorldEnvironment", true, false)
	if world_env and world_env.environment:
		var env = world_env.environment
		env.glow_enabled = glow
		env.ssao_enabled = ssao
		env.fog_enabled = fog
