from math import fabs, fmod,floor

def calc(hue):
    X= 1-fabs(fmod(hue/10922.6667,2)-1)
    X= 255 if X==1.0 else floor(X*256)
    Y=floor(fmod(hue/10922.6667,6))
    rgbval=[(255,X,0),(X,255,0),(0,255,X),(0,X,255),(X,0,255),(255,0,X)]
    big_list.append(rgbval[Y])

num_vals_needed=30
increment = 65536/num_vals_needed
big_list=[]
i=0
while i<(65536-1):
    calc(i)
    i+=increment
print(big_list)
