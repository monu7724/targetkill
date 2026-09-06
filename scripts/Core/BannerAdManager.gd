extends Node

var is_banner_visible: bool = false

func _ready():
    print("[BannerAdManager] Initialized.")

func show_banner():
    if not is_banner_visible:
        print("[BannerAdManager] Showing Banner Ad at bottom.")
        is_banner_visible = true

func hide_banner():
    if is_banner_visible:
        print("[BannerAdManager] Hiding Banner Ad.")
        is_banner_visible = false
