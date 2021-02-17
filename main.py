import os
import time
import random
from src.LightStrips.FixedLightStrip import FixedLightStrip
from src.LightStrips.ZenShiftLightStrip import ZenShiftLightStrip
from src.LightStrips.PulseLightStrip import PulseLightStrip
from src.LightStrips.XmasLightStrip import XmasLightStrip

if __name__ == '__main__':
    mode = os.environ.get('MODE', 'Zen')
    
    if mode == 'Pulse':
        light_strip = PulseLightStrip()
    elif mode == 'Fixed':
        light_strip = FixedLightStrip()
    elif mode == 'Xmas':
        light_strip = XmasLightStrip()
    else:
        light_strip = ZenShiftLightStrip()


    while True:
        light_strip.get_next_state()
        light_strip.update()
        time.sleep(0.1)
