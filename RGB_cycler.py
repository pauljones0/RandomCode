import sys
from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
import requests
from math import fabs, fmod,floor


def grovee_setup():
    #Find and setup Grovee
    # response = requests.get('https://developer-api.govee.com/v1/devices', headers={'Govee-API-KEY':'19d6dbe9-1265-4300-8420-1a96a3e53077'})
    # jresponse = response.json()
    # print(jresponse)
    #set the brightness and values to the max
    requests.put(url='https://developer-api.govee.com/v1/devices/control', headers={'Govee-API-KEY':<API KEY HERE>},json={'cmd':{'name': 'turn', 'value': 'on'},'device': <MAC ADDRESS HERE>, 'model': <MODEL HERE>})
    requests.put(url='https://developer-api.govee.com/v1/devices/control', headers={'Govee-API-KEY':<API KEY HERE>},json={'cmd':{'name': 'brightness', 'value': 100},'device': <MAC ADDRESS HERE>, 'model': <MODEL HERE>})
def hue_setup():
    #setup phillips hue and initialize the bridge
    b = Bridge(ip=<YOUR IP ADDRESS>,username=<YOUR USERNAME>)
    return b.lights
def lifx_setup():
    #setup Lifx bulbs
    lifx = LifxLAN(<NUMBER OF LIGHTS CAN BE DISCOVERED>)
    lifx.set_power_all_lights("on")
    return lifx
def calc(hue):
        '''
        This converts the normal 16bit HSV values to RGB ones and returns them.
        '''
        X= 1-fabs(fmod(hue/10922.6667,2)-1)
        X= 255 if X==1.0 else floor(X*256)
        Y=floor(fmod(hue/10922.6667,6))
        rgbval=[(255,X,0),(X,255,0),(0,255,X),(0,X,255),(X,0,255),(255,0,X)]
        return rgbval[Y]
    
def hue_grovee(new_hue):
    '''
    Makes the calls to update the RGB values
    '''
    rgb=calc(new_hue)
    red=rgb[0]
    green=rgb[1]
    blue=rgb[2]
    requests.put(url='https://developer-api.govee.com/v1/devices/control', headers={'Govee-API-KEY':<API KEY HERE>},json={'cmd':{'name': 'color', 'value': {"r":red,"g":green,"b":blue}},'device': <MAC ADDRESS HERE>, 'model': <MODEL HERE>})

    
def main():
     def Loop():
        #how long each cycle should last
        totalTime = 15 # in seconds
        transitionTime = 1 # in seconds

        maxHue = 65535
        hueIncrement = maxHue / totalTime

        #set phillips bulbs to max
        for light in lights:
            light.transitiontime = transitionTime * 10
            light.brightness = 254
            light.saturation = 254
            light.on = True # uncomment to turn all lights on

        #loop through
        hue = 0
        while True:
            for light in lights:
                light.hue = hue
            lifx.set_color_all_lights(color=[hue,65535,65535,3500], duration=transitionTime*1000, rapid=True)
            hue_grovee(hue)
            hue = (hue + hueIncrement) % maxHue
            sleep(transitionTime)
    lights=hue_setup()
    lifx = lifx_setup()
    grovee_setup()
    Loop()
                   
if __name__=="__main__":
    main()
