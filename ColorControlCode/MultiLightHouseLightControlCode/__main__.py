from .light_control import LightSystem, GoveeLights
from .light_gui import LightGUI
from .config import LightConfig
from lifxlan import LifxLAN
from phue import Bridge

def initialize_lights(config: LightConfig) -> LightSystem:
    """Initialize connections to all light systems"""
    try:
        bridge = Bridge(ip=config.HUE_BRIDGE_IP, username=config.HUE_USERNAME)
        lifx = LifxLAN()
        govee = GoveeLights()
    except Exception as e:
        raise ConnectionError(f"Failed to initialize light systems: {e}")
    
    return LightSystem(
        govee=govee,
        lifx=lifx,
        philips=bridge.lights
    )

def main():
    config = LightConfig()
    try:
        light_system = initialize_lights(config)
        gui = LightGUI(light_system)
        gui.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'gui' in locals():
            gui.cleanup()

if __name__ == "__main__":
    main()