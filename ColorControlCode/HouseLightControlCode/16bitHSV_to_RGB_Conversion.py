from math import fabs, fmod, floor

def hsv_to_rgb(hue):
    # Normalize hue to 0-6 range for the 6 color segments
    segment = (hue / 10922.6667) % 6  # 65536/6 ≈ 10922.6667
    
    # Calculate X value (represents the varying component in each segment)
    X = 1 - abs((segment % 2) - 1)  # Simplified from original formula
    X = 255 if X >= 0.999 else floor(X * 256)
    
    # Map segment number to RGB values
    segment_floor = floor(segment)
    return {
        0: (255, X, 0),
        1: (X, 255, 0), 
        2: (0, 255, X),
        3: (0, X, 255),
        4: (X, 0, 255),
        5: (255, 0, X)
    }[segment_floor]

# Pre-calculate all values in one list comprehension
num_vals_needed = 30
increment = 65536 / num_vals_needed
rgb_values = [hsv_to_rgb(i) for i in range(0, 65536-1, int(increment))]
print(rgb_values)
