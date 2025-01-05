import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
from dataclasses import dataclass
from typing import Tuple, List

# Configuration constants
MAX_BRIGHTNESS = 254
MAX_SATURATION = 254
HUE_MAGENTA = 56227
HUE_BLUE = 39780
CYCLE_INTERVAL = 60

# Bridge configuration 
HUE_BRIDGE_IP = None  # Replace with actual IP
HUE_USERNAME = None   # Replace with actual username

@dataclass
class LightSystem:
    lifx: LifxLAN
    philips: List
    
def initialize_lights() -> LightSystem:
    """Initialize light system connections.
    
    Returns:
        LightSystem: Connected light system objects
    """
    bridge = Bridge(ip=HUE_BRIDGE_IP, username=HUE_USERNAME)
    return LightSystem(
        lifx=LifxLAN(),
        philips=bridge.lights
    )

def set_all_lights_max_brightness(lights: LightSystem) -> None:
    """Set all lights to maximum brightness and saturation.
    
    Args:
        lights: LightSystem containing light connections
    """
    lights.lifx.set_power_all_lights("on")
    for light in lights.philips:
        light.brightness = MAX_BRIGHTNESS
        light.saturation = MAX_SATURATION
        light.on = True

def cycle_colors(lights: LightSystem) -> None:
    """Continuously cycle lights between magenta and blue.
    
    Args:
        lights: LightSystem containing light connections
    """
    is_magenta = False
    while True:
        hue = HUE_MAGENTA if is_magenta else HUE_BLUE
        
        # Update all lights simultaneously
        lights.lifx.set_color_all_lights(color=[hue, 65535, 65535, 3500])
        for light in lights.philips:
            light.hue = hue
            
        is_magenta = not is_magenta
        sleep(CYCLE_INTERVAL)

def main():
    lights = initialize_lights()
    set_all_lights_max_brightness(lights)
    cycle_colors(lights)

if __name__ == "__main__":
    main()
