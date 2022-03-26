from time import sleep
from phue import Bridge
from lifxlan import LifxLAN
import requests
from math import fabs, fmod,floor

class GoveeLights:
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
    def status_check(self,raw):
        message=raw.json()
        if message['code'] != 200:
            raise Exception(message['code']+": "+message['message'])
        else:
            pass
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
        
def main():
    govee = GoveeLights(APIKEY)
    #setup phillips hue and initialize the bridge
    b = Bridge(ip=IPKEY,username=USERNAME)
    lights = b.lights
    
    #setup Lifx bulbs
    lifx = LifxLAN(9)
    lifx.set_power_all_lights("on") 
       
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
        govee.update_hue(0,hue)
        hue = (hue + hueIncrement) % maxHue
        sleep(transitionTime)
                   
if __name__=="__main__":
    main()
    
