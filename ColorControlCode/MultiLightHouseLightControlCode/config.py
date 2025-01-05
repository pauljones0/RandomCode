from dataclasses import dataclass

@dataclass
class LightConfig:
    """Light system configuration"""
    HUE_BRIDGE_IP: str = "YOUR_BRIDGE_IP"
    HUE_USERNAME: str = "YOUR_USERNAME"
    MAX_BRIGHTNESS: int = 254
    MAX_SATURATION: int = 254
    MAX_HUE: int = 65535
    TRANSITION_TIME: int = 1  # seconds
    CYCLE_TIME: int = 15  # seconds