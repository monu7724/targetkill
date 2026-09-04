extends Node

enum Quality { LOW, MEDIUM, HIGH }

var current_quality = Quality.MEDIUM

func _ready():
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

func setup_low_quality():
	# Graphics quality adjustments for low-end mobile
	get_viewport().msaa_3d = Viewport.MSAA_DISABLED
	get_viewport().screen_space_aa = Viewport.SCREEN_SPACE_AA_DISABLED
	get_viewport().use_hdr_2d = false
	
	RenderingServer.directional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_1X)
	RenderingServer.positional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_1X)
	
	# Disable expensive post-processing globally if handled via environment
	# This usually involves modifying the WorldEnvironment resource at runtime
	_update_environment(false, false, false)

func setup_medium_quality():
	get_viewport().msaa_3d = Viewport.MSAA_2X
	get_viewport().screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA
	get_viewport().use_hdr_2d = true
	
	RenderingServer.directional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_STATISTICS)
	RenderingServer.positional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_STATISTICS)
	
	_update_environment(true, false, true)

func setup_high_quality():
	get_viewport().msaa_3d = Viewport.MSAA_4X
	get_viewport().screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA
	get_viewport().use_hdr_2d = true
	
	RenderingServer.directional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_STATISTICS)
	RenderingServer.positional_soft_shadow_filter_set(RenderingServer.SHADOW_SOFT_FILTER_STATISTICS)
	
	_update_environment(true, true, true)

func _update_environment(glow: bool, ssao: bool, fog: bool):
	var world_env = get_tree().root.find_child("WorldEnvironment", true, false)
	if world_env and world_env.environment:
		var env = world_env.environment
		env.glow_enabled = glow
		env.ssao_enabled = ssao
		env.fog_enabled = fog
