#include <stdio.h>
#include <math.h>

int rgb_convert(float *red, float *green, float *blue){
    *red = fmax(0.0, fmin(1.0, *red));
    *green =fmax(0.0, fmin(1.0, *green));
    *blue =fmax(0.0, fmin(1.0, *blue));
    int red_256 = floor(*red == 1.0 ? 255 : *red * 256.0);
    int green_256 = floor(*green == 1.0 ? 255 : *green * 256.0);
    int blue_256 = floor(*blue == 1.0 ? 255 : *blue * 256.0);
    //prints out 256 bit equivalents
    printf("[%d,%d,%d],", red_256, green_256, blue_256);
    return 0;    
}

int calc(float *H){
    //saturation = 1.0
    float s = 100/100;
    //value or brightness = 1.0
    float v = 100/100;
    float C = s*v;
    float X = C*(1-fabs(fmod(*H/60.0, 2)-1));
    float m = v-C;
    float r,g,b;
    if(*H >= 0 && *H < 60){
        r = C, g = X, b = 0;
    }
    else if(*H >= 60 && *H < 120){
        r = X, g = C, b = 0;
    }
    else if(*H >= 120 && *H < 180){
        r = 0, g = C, b = X;
    }
    else if(*H >= 180 && *H < 240){
        r = 0, g = X, b = C;
    }
    else if(*H >= 240 && *H < 300){
        r = X, g = 0, b = C;
    }
    else{
        r = C, g = 0, b = X;
    }
    float R = r+m;
    float G = g+m;
    float B = b+m;
    
    rgb_convert(&R, &G, &B);
    
    //prints out the floats
    //printf("[%f, %f, %f],\n", R, G, B);
    return 0;
}

int main()
{
    float num_values_needed = 30;
    //this code works in degrees, so hue must go from 0-360
    float incr = 360 / num_values_needed;
    for(float i = 0; i<360 ;i=i+incr) 
        {
        calc(&i);
        }
    return 0;
}

