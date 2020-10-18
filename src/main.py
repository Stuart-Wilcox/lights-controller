import time
import random
from FixedLightStrip import FixedLightStrip
from ZenShiftLightStrip import ZenShiftLightStrip


if __name__ == '__main__':
    light_strip = ZenShiftLightStrip()
    
    while True:
        light_strip.get_next_state()
        light_strip.update()
        time.sleep(0.1)
