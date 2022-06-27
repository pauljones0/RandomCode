import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
from tkinter import Tk, Label, Button
from math import fabs, fmod,floor
from random import uniform

#set global variables
loop=False
brightness_delta_toggle=False
HUE_BRIDGE_IP = none
HUE_USERNAME=none
#my python package is all bunked, so I put this here
sys.path.append('c:/users/bethe/appdata/local/programs/python/python310/lib/site-packages')
   
def initialize_lights():
    """Initializes the device objects respective to each API and returns to a global variable.
    Returns:
        Tuple: Containing a govee lights object, a lifxlan lights object and a phillips hue lights object.
    """
    #setup phillips hue and initialize the bridge
    b = Bridge(ip=HUE_BRIDGE_IP,username=HUE_USERNAME)
    philips = b.lights
    
    #setup Lifx bulbs
    #this can be done faster if the IP address and MAC addresses are already known
    lifx = LifxLAN() 
    return lifx,philips

def start_lights():
    def on_lights():
        """Sets all lights to max brightness, so that any future cycling can easily be seen.
        """
        lifx.set_power_all_lights("on")
        for light in philips:
            light.brightness = 254
            light.saturation = 254
            light.on = True # uncomment to turn all lights on
    
    def cycle():
        hue = 0
        magenta=False
        while True:
            for light in philips:
                light.hue = hue
            lifx.set_color_all_lights(color=[hue,65535,65535,3500])
            if magenta:
                hue = 56227
            else:
                hue = 39780
            sleep(60)
    
    on_lights()
    cycle()
    
    
lifx,philips = initialize_lights()
start_lights()
        
