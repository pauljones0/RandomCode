import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
from tkinter import Tk, Label, Button
import requests
from math import fabs, fmod,floor
from random import uniform

#set global variables
loop=False
brightness_delta_toggle=False
GOVEE_API_KEY='19d6dbe9-1265-4300-8420-1a96a3e53077'
HUE_BRIDGE_IP = '192.168.0.46'
HUE_USERNAME='C96oAnyvobNyGoFqics2hGt91BgGtrhYEqReFT46'
#my python package is all bunked, so I put this here
sys.path.append('c:/users/bethe/appdata/local/programs/python/python310/lib/site-packages')

class GoveeLights:
    """
    Handles calling Govee light strips. Once initialized, calls to individual devices can be handled individually by index 
    or looped through using self.devices. Sometimes the response from the API cannot be parsed into json. Still working on that.
    Raises:
        Exception: If parameters to turn on or off the light weren't correct, self.turn will raise an exception telling the user that there's an issue.
        Also JSON return object doesn't parse, it will print out a stringified version of said object.

    Returns:
        Calc:Tuple of RGB values
    """
    def __init__(self, API_KEY):
        self.URL='https://developer-api.govee.com/v1/devices'
        self.HEADERS={'Govee-API-KEY':API_KEY}
        answer = requests.get(self.URL, headers=self.HEADERS)
        self.status_check(answer)
        self.response = answer.json()
        self.devices=[{'device':x['device'],'model':x['model']} for x in self.response['data']['devices']]
    def turn(self,device_index=0,signal='on'):
        turn_on={'name': 'turn', 'value': 'on'}
        turn_off={'name': 'turn', 'value': 'off'}
        command=None
        if signal in [1,"1","on"]:
            command=turn_on
        elif signal in [0,"0","off"]:
            command=turn_off
        else:
            raise Exception("Signal parameter given to Turn method insufficient")
        answer = requests.put(url=self.URL+'/control', headers=self.HEADERS,json=self.devices[device_index] | {'cmd':command})
        self.status_check(answer)
    def brightness(self, device_index=0,value=100):
        brightness_level = lambda x: {'name': 'brightness', 'value': max(0,min(x,100))}
        answer = requests.put(url=self.URL+'/control', headers=self.HEADERS,json=self.devices[device_index] | {'cmd':brightness_level(value)})
        self.status_check(answer)
    def color(self, device_index=0,color=[255,255,255]):
        red,green, blue = [min(255,max(0,x)) for x in color]
        command = {'cmd':{'name': 'color', 'value': {"r":red,"g":green,"b":blue}}}
        answer = requests.put(url=self.URL+'/control', headers=self.HEADERS,json=self.devices[device_index] | {'cmd':command})
        self.status_check(answer)
    def status_check(self,raw):
        try:
            message=raw.json()
            if message['code'] != 200:
                print(message['code']+": "+message['message'])
        except:
            print(str(message)+'\n failed to be converted to json')
    def calc(self,hue):
        X= 1-fabs(fmod(hue/10922.6667,2)-1)
        X= 255 if X==1.0 else floor(X*256)
        Y=floor(fmod(hue/10922.6667,6))
        rgb_varient=[(255,X,0),(X,255,0),(0,255,X),(0,X,255),(X,0,255),(255,0,X)]
        return rgb_varient[Y]
    def update_hue(self,device_index=0,new_hue=65535):
        red,green, blue = self.calc(max(0,min(65535,new_hue)))
        command = {'cmd':{'name': 'color', 'value': {"r":red,"g":green,"b":blue}}}
        answer = requests.put(url=self.URL+'/control', headers=self.HEADERS,json=self.devices[device_index] | command)
        self.status_check(answer)
    
class LightGUI:
    '''
    Simple GUI interface, handles calls to individual functions to start, stop, dim or white out the lights.
    Brightness Delta Toggle allows for the lights to have a more random/candle like appearance when looping.
    '''
    def __init__(self, master):
        self.master = master
        master.title("Lights GUI")

        self.label = Label(master, text="What do you want to do with your lights?")
        self.label.pack()

        self.start_button = Button(master, text="Start", command=start_lights())
        self.start_button.pack()

        self.stop_button = Button(master, text="Stop", command=stop_lights())
        self.stop_button.pack()
        
        self.white_button = Button(master, text="White", command=white_lights())
        self.white_button.pack()
        
        self.dim_button = Button(master, text="Dim", command=dim_lights())
        self.dim_button.pack()
        
        self.bright_button = Button(master, text="Brightness Delta Toggle", command=self.bright_toggle)
        self.bright_button.pack()
        
    def bright_toggle(self):
        global brightness_delta_toggle
        brightness_delta_toggle = not(brightness_delta_toggle)
   
def initialize_lights():
    """Initializes the device objects respective to each API and returns to a global variable.

    Returns:
        Tuple: Containing a govee lights object, a lifxlan lights object and a phillips hue lights object.
    """
    govee = GoveeLights(GOVEE_API_KEY)
    #setup phillips hue and initialize the bridge
    b = Bridge(ip=HUE_BRIDGE_IP,username=HUE_USERNAME)
    philips = b.lights
    
    #setup Lifx bulbs
    #this can be done faster if the IP address and MAC addresses are already known
    lifx = LifxLAN() 
    return govee,lifx,philips
    
def stop_lights():
    """Turns all lights off
    """
    govee.turn(0,'off')
    for light in philips:
        light.on = False
    lifx.set_power_all_lights("off")
    
def white_lights():
    """Sets all lights to a white value
    """
    govee.color(0,[255,255,255])
    for light in philips:
        light.brightness = 254
        light.saturation = 0
    lifx.set_color_all_lights([40000,0,65535,4000])
        
def dim_lights():
    """Dims lights to the lowest level possible, as LED lights don't dim linearly.
    """
    govee.color(0,[1,1,1])
    for light in philips:
        light.brightness = 1
        light.saturation = 0
    lifx.set_color_all_lights([40000,0,1,4000])

    
def start_lights():
    """Runs a RGB cycle through all the lights. Currently uses sleep, which
    should be updated to use a Threadpooler executer.
    """
    totalTime = 15 # in seconds
    transitionTime = 1 # in seconds
    loop=True
    maxHue = 65535
    hueIncrement = maxHue / totalTime
    
    def on_lights():
        """Sets all lights to max brightness, so that any future cycling can easily be seen.
        """
        govee.turn(0,'on')
        lifx.set_power_all_lights("on")
        for light in philips:
            light.transitiontime = transitionTime * 10
            light.brightness = 254
            light.saturation = 254
            light.on = True # uncomment to turn all lights on
    
    def cycle():
        """Cycles the lights
        """
        #how long each cycle should last

        #loop through
        hue = 0
        if brightness_delta_toggle:
            brightnessdelta = uniform(0.0,0.3)
        else:
            brightnessdelta=0
        while True:
            brightnessdelta = uniform(0.0,0.3) if brightness_delta_toggle else 0.0
            if not(loop):
                break
            for light in philips:
                light.hue = hue
                light.brightness = int(254 * (1-brightnessdelta))
            lifx.set_color_all_lights(color=[hue,65535,int(65535*(1-brightnessdelta)),3500], duration=transitionTime*1000, rapid=True)
            #can't update govee as it would go over the 100 api calls per minute right now.
            govee.update_hue(0,hue)
            hue = (hue + hueIncrement) % maxHue
            sleep(transitionTime)
    
    on_lights()
    cycle()
    
    
govee,lifx,philips = initialize_lights()
def main():
    """
    Initialize the GUI which controls the code.
    """
    root = Tk()
    my_gui = LightGUI(root)
    root.mainloop()
    
if __name__=="__main__":
    main()
        
