class_name LightingProfiles
extends RefCounted

enum ProfileType {
	DAY_CLEAR,
	DAY_CLOUDY,
	INDOOR_DAY,
	BOSS_FACILITY
}

static func apply_lighting_profile(sun: DirectionalLight3D, env: Environment, profile: ProfileType):
	if not sun or not env: return
	
	match profile:
		ProfileType.DAY_CLEAR:
			sun.light_energy = 2.4
			sun.light_color = Color(1.0, 0.98, 0.93)
			sun.shadow_enabled = true
			env.background_mode = Environment.BG_SKY
			if env.sky and env.sky.sky_material is ProceduralSkyMaterial:
				var sky_mat = env.sky.sky_material as ProceduralSkyMaterial
				sky_mat.sky_top_color = Color(0.35, 0.58, 0.88)
				sky_mat.sky_horizon_color = Color(0.72, 0.82, 0.92)
				sky_mat.ground_bottom_color = Color(0.2, 0.22, 0.25)
				
		ProfileType.DAY_CLOUDY:
			sun.light_energy = 1.75
			sun.light_color = Color(0.92, 0.94, 0.97)
			sun.shadow_enabled = true
			if env.sky and env.sky.sky_material is ProceduralSkyMaterial:
				var sky_mat = env.sky.sky_material as ProceduralSkyMaterial
				sky_mat.sky_top_color = Color(0.5, 0.6, 0.72)
				sky_mat.sky_horizon_color = Color(0.68, 0.73, 0.8)
				
		ProfileType.INDOOR_DAY:
			sun.light_energy = 2.0
			sun.light_color = Color(0.98, 0.96, 0.92)
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_color = Color(0.55, 0.6, 0.65)
			env.ambient_light_energy = 1.0
			
		ProfileType.BOSS_FACILITY:
			sun.light_energy = 2.2
			sun.light_color = Color(0.95, 0.98, 1.0)
			env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
			env.ambient_light_color = Color(0.4, 0.45, 0.52)
			env.ambient_light_energy = 1.2
