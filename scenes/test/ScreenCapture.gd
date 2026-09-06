extends Node

var scenes = [
    {"name": "MainMenu", "path": "res://scenes/UI/MainMenu.tscn"},
    {"name": "MissionSelect", "path": "res://scenes/UI/MissionSelect.tscn"},
    {"name": "Armory", "path": "res://scenes/UI/ArmoryUI.tscn"},
    {"name": "Result", "path": "res://scenes/UI/ResultUI.tscn"},
    {"name": "HUD", "path": "res://scenes/UI/HUD.tscn"}
]

var idx = 0
var current = null

func _ready():
    print("[ScreenCapture] Start")
    RenderingServer.frame_post_draw.connect(_on_frame)
    _load_next()

func _load_next():
    if current:
        current.queue_free()
        
    if idx >= scenes.size():
        print("[ScreenCapture] Done")
        get_tree().quit()
        return
        
    var s = load(scenes[idx].path).instantiate()
    add_child(s)
    current = s
    
    if scenes[idx].name == "Result":
        # Simulate result modal
        if current.has_method("_on_mission_completed"):
            current.show()
            var lbl = current.find_child("Title", true, false)
            if lbl: lbl.text = "MISSION COMPLETE"
            
    print("[ScreenCapture] Loaded " + scenes[idx].name)

var wait_frames = 10
func _on_frame():
    wait_frames -= 1
    if wait_frames == 0:
        var img = get_viewport().get_texture().get_image()
        var fname = "preview_" + scenes[idx].name + ".png"
        img.save_png(fname)
        print("[ScreenCapture] Saved " + fname)
        idx += 1
        wait_frames = 10
        _load_next()
