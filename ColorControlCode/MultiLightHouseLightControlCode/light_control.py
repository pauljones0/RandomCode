import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
import requests
from math import fabs, fmod, floor
from random import uniform
from typing import Tuple, List, Dict, Any, Optional
from dataclasses import dataclass
from .config import LightConfig

# Configuration constants
MAX_BRIGHTNESS = 254
MAX_SATURATION = 254
MAX_HUE = 65535
TRANSITION_TIME = 1  # seconds
CYCLE_TIME = 15  # seconds

@dataclass
class LightSystem:
    """Container for different light system connections"""
    govee: 'GoveeLights'
    lifx: 'LifxLAN'
    philips: List['PhilipsLight']  # Type hint for Philips lights

class ColorUtils:
    """Utility class for color conversions"""
    _HUE_SEGMENT_SIZE = 10922.6667  # Pre-calculated constant (65536/6)
    _COLOR_MAP = {  # Pre-calculated color mappings
        0: lambda x: (255, x, 0),
        1: lambda x: (x, 255, 0),
        2: lambda x: (0, 255, x),
        3: lambda x: (0, x, 255),
        4: lambda x: (x, 0, 255),
        5: lambda x: (255, 0, x)
    }

    @staticmethod
    def hsv_to_rgb(hue: int) -> Tuple[int, int, int]:
        """Convert 16-bit HSV hue to RGB values - O(1) time complexity"""
        segment = int(hue / ColorUtils._HUE_SEGMENT_SIZE) % 6
        x = 1 - abs((segment % 2) - 1)
        x = 255 if x >= 0.999 else int(x * 256)
        
        return ColorUtils._COLOR_MAP[segment](x)

class GoveeLights:
    """Handles Govee light strip control via their API"""
    [Reference to existing GoveeLights class implementation]
    ```python:ColorControlCode/HouseLightControlCode/RGB_cycler.py
    startLine: 34
    endLine: 104
    ```

class LightController:
    """Core light control functionality"""
    def __init__(self, lights: LightSystem, config: LightConfig):
        self.lights = lights
        self.config = config
        self._running = False
        self._cached_brightness: Optional[int] = None
        self._cached_hue: Optional[int] = None
    
    def set_max_brightness(self) -> None:
        """Set all lights to maximum brightness - O(n) where n is number of lights"""
        # Batch operations where possible
        self.lights.govee.turn(signal='on')
        self.lights.lifx.set_power_all_lights("on")
        
        # Cache the max brightness settings
        if self._cached_brightness != self.config.MAX_BRIGHTNESS:
            self._cached_brightness = self.config.MAX_BRIGHTNESS
            for light in self.lights.philips:
                light.transitiontime = self.config.TRANSITION_TIME * 10
                light.brightness = self.config.MAX_BRIGHTNESS
                light.saturation = self.config.MAX_SATURATION
                light.on = True

    def dim_lights(self) -> None:
        """Set all lights to minimum brightness - O(n)"""
        # Use pre-defined minimum values
        MIN_BRIGHTNESS = 1
        MIN_SATURATION = 0
        
        self.lights.govee.set_color((MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS))
        self.lights.lifx.set_color_all_lights([40000, 0, MIN_BRIGHTNESS, 4000])
        
        # Cache the minimum brightness settings
        if self._cached_brightness != MIN_BRIGHTNESS:
            self._cached_brightness = MIN_BRIGHTNESS
            for light in self.lights.philips:
                light.brightness = MIN_BRIGHTNESS
                light.saturation = MIN_SATURATION

    def cycle_colors(self, brightness_delta: float = 0.0) -> None:
        """Cycle all lights through the color spectrum - O(n) per cycle"""
        hue = 0
        hue_increment = self.config.MAX_HUE / self.config.CYCLE_TIME
        
        while self._running:
            # Calculate new values only if they've changed
            if self._cached_hue != hue:
                self._cached_hue = hue
                brightness = int(self.config.MAX_BRIGHTNESS * (1 - brightness_delta))
                brightness_hsv = int(self.config.MAX_HUE * (1 - brightness_delta))

                # Batch update all lights simultaneously
                self._update_all_lights(hue, brightness, brightness_hsv)

            hue = (hue + hue_increment) % self.config.MAX_HUE
            sleep(self.config.TRANSITION_TIME)

    def _update_all_lights(self, hue: int, brightness: int, brightness_hsv: int) -> None:
        """Update all light systems simultaneously - O(n)"""
        # Update LIFX lights (batch operation)
        self.lights.lifx.set_color_all_lights(
            color=[hue, self.config.MAX_HUE, brightness_hsv, 3500],
            duration=self.config.TRANSITION_TIME * 1000,
            rapid=True
        )
        
        # Update Govee lights
        self.lights.govee.set_hue(hue)
        
        # Update Philips lights
        for light in self.lights.philips:
            light.hue = hue
            light.brightness = brightness

    def start(self) -> None:
        """Start the light control system"""
        self._running = True
        self.set_max_brightness()
        self.cycle_colors()

    def stop(self) -> None:
        """Stop the light control system and turn off all lights"""
        self._running = False
        self.lights.govee.turn(signal='off')
        self.lights.lifx.set_power_all_lights("off")
        for light in self.lights.philips:
            light.on = False