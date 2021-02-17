import random
from src.constants import MAX_INTENSITY

def clamp_int(value, low=0, high=0, step=1):
    value = int(value)

    half_step = int(step) / 2
    direction = 1
    if (value % step) < half_step:
        direction = -1  
    while value % step:
        value += direction

    low = int(low)
    high = int(high)
    return min(high, max(low, value))

def get_random_rgb():
    value = int(random.uniform(1, 7))
    red = value & 1
    green = value >> 1 & 1
    blue = value >> 2 & 1
    
    return (red * MAX_INTENSITY, green * MAX_INTENSITY, blue * MAX_INTENSITY)
