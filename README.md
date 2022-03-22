# RandomCode
Bits and pieces of random code that I make from time-to-time.

Brightness.ps1 - Powershell script, runs in the background in task scheduler and constantly updates the brightness of the screen.

Volume.ps1 - I used this to mute my system randomly, as CodeRadio would keep playing and it got overwhelming to have it do so all the time. This uses nircmd.exe to run so make sure you have that installed first. You can choose how many seconds of noise you want and how many second of silence.

Midterm-V3.py -A dictionary lookup program I used for a midterm to find approximations of a medical sentence quickly and efficiently. It didn't involve the whole course and a ton of data cleaning was required, but it works reasonably well.

Handin.py - 7 Shifts coding challenge

Smallprogram1.py - This is me trying to code again. Make small simple things that I know how to make, consistently. I've been crushed by the harder assignments in the later years in my Uni degree and didn't feel like I knew how to code the stuff that I was expected of me, instead scrolling reddit endlessly. This is the first (and hopefully not the last) program that doesn't do much, but allows me to feel accomplished and knowledgable and that I can make things.

imageviewer.pynb - Allows you to view images from a url, and view all associated metadata.

RGBcycler.py - Razer Chroma works with Lifx and Hue, but the implementations aren't very well done, with obvious banding between transitions. This code allows you to do a synchronous RGB cycle with Lifx AND hue bulbs. TODO add Twinkly AND grovee API too

color_convert.c -Converts from 360 degree HSV to RGB 8bit, outputting a python-like list. This is used to help make RGBcycler.py work with Grovee API lights, as Grovee only accepts RGB values. May plan to write this in python in the future

16bitHSV_to_RGB.py - Converts 16bit HSV value to RGB, assuming that one is doing a RGB cycle (max saturation and brightness) and outputs list.
