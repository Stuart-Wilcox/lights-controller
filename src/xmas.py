import time
import random
from XmasLightStrip import XmasLightStrip

if __name__ == '__main__':
    light_strip = XmasLightStrip()
    
    while True:
        light_strip.get_next_state()
        light_strip.update()
        time.sleep(1)
