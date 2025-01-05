import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
from tkinter import Tk, Label, Button
import requests
from math import fabs, fmod, floor
from random import uniform
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass

# Configuration constants
MAX_BRIGHTNESS = 254
MAX_SATURATION = 254
MAX_HUE = 65535
TRANSITION_TIME = 1  # seconds
CYCLE_TIME = 15  # seconds

# API credentials - replace with your own
GOVEE_API_KEY = 'YOUR_API_KEY'  # Replace with actual API key
HUE_BRIDGE_IP = 'YOUR_BRIDGE_IP'  # Replace with actual bridge IP
HUE_USERNAME = 'YOUR_USERNAME'  # Replace with actual username

# Global state
loop = False
brightness_delta_toggle = False

@dataclass
class LightSystem:
    govee: 'GoveeLights'
    lifx: LifxLAN
    philips: List

class GoveeLights:
    """Handles Govee light strip control via their API"""
    
    def __init__(self, api_key: str):
        self.url = 'https://developer-api.govee.com/v1/devices'
        self.headers = {'Govee-API-KEY': api_key}
        self.devices = self._get_devices()

    def _get_devices(self) -> List[Dict[str, str]]:
        """Fetch and return list of Govee devices"""
        response = requests.get(self.url, headers=self.headers)
        self._check_response(response)
        data = response.json()
        return [{'device': x['device'], 'model': x['model']} 
                for x in data['data']['devices']]

    def turn(self, device_index: int = 0, signal: str = 'on') -> None:
        """Turn device on/off"""
        if signal not in ['on', 'off', '1', '0', 1, 0]:
            raise ValueError("Signal must be 'on'/'off' or 1/0")
            
        command = {'name': 'turn', 'value': 'on' if str(signal) in ['1', 'on'] else 'off'}
        self._send_command(device_index, command)

    def set_brightness(self, value: int, device_index: int = 0) -> None:
        """Set device brightness (0-100)"""
        value = max(0, min(value, 100))
        command = {'name': 'brightness', 'value': value}
        self._send_command(device_index, command)

    def set_color(self, color: Tuple[int, int, int], device_index: int = 0) -> None:
        """Set RGB color (each 0-255)"""
        r, g, b = [max(0, min(x, 255)) for x in color]
        command = {'name': 'color', 'value': {'r': r, 'g': g, 'b': b}}
        self._send_command(device_index, command)

    def set_hue(self, hue: int, device_index: int = 0) -> None:
        """Set light color using HSV hue value (0-65535)"""
        rgb = self._hsv_to_rgb(max(0, min(hue, MAX_HUE)))
        self.set_color(rgb, device_index)

    def _send_command(self, device_index: int, command: Dict) -> None:
        """Send command to Govee API"""
        payload = {**self.devices[device_index], 'cmd': command}
        response = requests.put(f'{self.url}/control', 
                              headers=self.headers,
                              json=payload)
        self._check_response(response)

    @staticmethod
    def _check_response(response: requests.Response) -> None:
        """Check API response for errors"""
        try:
            data = response.json()
            if data['code'] != 200:
                print(f"Error {data['code']}: {data['message']}")
        except ValueError:
            print(f"Failed to parse response: {response.text}")

    @staticmethod
    def _hsv_to_rgb(hue: int) -> Tuple[int, int, int]:
        """Convert HSV hue to RGB values"""
        segment = (hue / 10922.6667) % 6
        x = 1 - abs((segment % 2) - 1)
        x = 255 if x >= 0.999 else floor(x * 256)
        
        rgb_variants = [
            (255, x, 0), (x, 255, 0), (0, 255, x),
            (0, x, 255), (x, 0, 255), (255, 0, x)
        ]
        return rgb_variants[floor(segment)]

class LightGUI:
    """GUI interface for light control"""
    
    def __init__(self, master: Tk, lights: LightSystem):
        self.master = master
        self.lights = lights
        master.title("Lights GUI")

        Label(master, text="Light Control").pack()

        for text, command in [
            ("Start", self.start_lights),
            ("Stop", self.stop_lights),
            ("White", self.white_lights),
            ("Dim", self.dim_lights),
            ("Brightness Delta Toggle", self.bright_toggle)
        ]:
            Button(master, text=text, command=command).pack()

    def bright_toggle(self) -> None:
        global brightness_delta_toggle
        brightness_delta_toggle = not brightness_delta_toggle

    def start_lights(self) -> None:
        global loop
        loop = True
        self._set_max_brightness()
        self._cycle_colors()

    def stop_lights(self) -> None:
        global loop
        loop = False
        self.lights.govee.turn(signal='off')
        self.lights.lifx.set_power_all_lights("off")
        for light in self.lights.philips:
            light.on = False

    def white_lights(self) -> None:
        self.lights.govee.set_color((255, 255, 255))
        self.lights.lifx.set_color_all_lights([40000, 0, MAX_HUE, 4000])
        for light in self.lights.philips:
            light.brightness = MAX_BRIGHTNESS
            light.saturation = 0

    def dim_lights(self) -> None:
        self.lights.govee.set_color((1, 1, 1))
        self.lights.lifx.set_color_all_lights([40000, 0, 1, 4000])
        for light in self.lights.philips:
            light.brightness = 1
            light.saturation = 0

    def _set_max_brightness(self) -> None:
        self.lights.govee.turn(signal='on')
        self.lights.lifx.set_power_all_lights("on")
        for light in self.lights.philips:
            light.transitiontime = TRANSITION_TIME * 10
            light.brightness = MAX_BRIGHTNESS
            light.saturation = MAX_SATURATION
            light.on = True

    def _cycle_colors(self) -> None:
        hue = 0
        hue_increment = MAX_HUE / CYCLE_TIME
        
        while loop:
            brightness_delta = uniform(0.0, 0.3) if brightness_delta_toggle else 0.0
            brightness = int(MAX_BRIGHTNESS * (1 - brightness_delta))
            brightness_hsv = int(MAX_HUE * (1 - brightness_delta))

            for light in self.lights.philips:
                light.hue = hue
                light.brightness = brightness

            self.lights.lifx.set_color_all_lights(
                color=[hue, MAX_HUE, brightness_hsv, 3500],
                duration=TRANSITION_TIME * 1000,
                rapid=True
            )
            self.lights.govee.set_hue(hue)

            hue = (hue + hue_increment) % MAX_HUE
            sleep(TRANSITION_TIME)

def initialize_lights() -> LightSystem:
    """Initialize connections to all light systems"""
    return LightSystem(
        govee=GoveeLights(GOVEE_API_KEY),
        lifx=LifxLAN(),
        philips=Bridge(ip=HUE_BRIDGE_IP, username=HUE_USERNAME).lights
    )

def main():
    """Initialize and run the light control GUI"""
    lights = initialize_lights()
    root = Tk()
    LightGUI(root, lights)
    root.mainloop()

if __name__ == "__main__":
    main()
