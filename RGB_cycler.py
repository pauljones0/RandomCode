import sys
from phue import Bridge
from lifxlan import LifxLAN

def main():
    
    #setup phillips hue and initialize the bridge
    b = Bridge(ip='YOUR BRIDGE IP HERE',username='YOUR USERNAME HERE')
    lights = b.lights
    
    #setup Lifx bulbs
    lifx = LifxLAN(9)
    
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
        # light.on = True # uncomment to turn all lights on
    
    #loop through
    hue = 0
    while True:
        for light in lights:
            light.hue = hue
        lifx.set_color_all_lights(color=[hue,65535,65535,3500], duration=transitionTime*1000, rapid=True)
        hue = (hue + hueIncrement) % maxHue
        sleep(transitionTime)
                   
if __name__=="__main__":
    main()