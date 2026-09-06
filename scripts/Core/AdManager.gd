extends Node

signal reward_granted(reward_type: String, amount: int)
signal ad_failed(reason: String)

var is_ad_ready: bool = true

func _ready():
    print("[AdManager] Initialized. Rewarded Ads ready.")

func show_rewarded_ad(reward_type: String = "cash"):
    if not is_ad_ready:
        ad_failed.emit("Ad not ready")
        return
        
    print("[AdManager] Displaying Rewarded Ad...")
    # Fake delay
    await get_tree().create_timer(1.0).timeout
    
    print("[AdManager] Ad watched successfully.")
    var amount = 500 if reward_type == "cash" else 1
    reward_granted.emit(reward_type, amount)
