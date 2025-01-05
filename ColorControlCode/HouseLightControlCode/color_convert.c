#include <stdio.h>
#include <math.h>

// Convert float RGB values (0-1) to 8-bit integers (0-255)
int rgb_convert(float *red, float *green, float *blue) {
    // Clamp values between 0-1
    *red = fmax(0.0, fmin(1.0, *red));
    *green = fmax(0.0, fmin(1.0, *green));
    *blue = fmax(0.0, fmin(1.0, *blue));

    // Convert to 8-bit integers
    int red_256 = (int)(*red * 255.0 + 0.5); // Rounding instead of floor
    int green_256 = (int)(*green * 255.0 + 0.5);
    int blue_256 = (int)(*blue * 255.0 + 0.5);

    printf("[%d,%d,%d],", red_256, green_256, blue_256);
    return 0;
}

// Convert HSV to RGB, with H in degrees (0-360), S=1, V=1
int hsv_to_rgb(float *hue) {
    const float s = 1.0; // Full saturation
    const float v = 1.0; // Full value/brightness
    
    // Pre-calculate common values
    float C = s * v; // Chroma
    float h_prime = *hue / 60.0f;
    float X = C * (1 - fabs(fmod(h_prime, 2) - 1));
    float m = v - C;

    float r, g, b;
    
    // Color selection using integer division
    int segment = (int)(h_prime);
    switch(segment) {
        case 0: r = C; g = X; b = 0; break;
        case 1: r = X; g = C; b = 0; break;
        case 2: r = 0; g = C; b = X; break;
        case 3: r = 0; g = X; b = C; break;
        case 4: r = X; g = 0; b = C; break;
        default: r = C; g = 0; b = X; // Case 5
    }

    // Add value-saturation adjustment
    float R = r + m;
    float G = g + m;
    float B = b + m;
    
    return rgb_convert(&R, &G, &B);
}

int main() {
    const int NUM_VALUES = 30;
    const float INCREMENT = 360.0f / NUM_VALUES;
    
    // Pre-calculate all values
    for(float hue = 0; hue < 360.0f; hue += INCREMENT) {
        hsv_to_rgb(&hue);
    }
    
    return 0;
}
