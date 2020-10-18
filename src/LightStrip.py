import atexit
import board
import neopixel

from constants import LED_COUNT


class LightStrip:
    """
    Interface which wraps the underlying led light strip.
    Is a singleton
    """
    pixels = neopixel.NeoPixel(board.D18, 0, auto_write=False)
    __instance = None

    def __new__(cls, led_count=LED_COUNT):
        if LightStrip.__instance is None:
            LightStrip.__instance = object.__new__(cls)
        LightStrip.__instance.led_count = led_count
        LightStrip.pixels = neopixel.NeoPixel(board.D18, led_count, auto_write=False)
        return LightStrip.__instance

    def __init__(self, led_count=LED_COUNT):
        self.led_count = led_count
        self.state = {}
        self.__clear_state__() # clear state on init
        atexit.register(self.__clear_state__) # register turning lights off at exit

    def __clear_state__(self):
        for i in range(0, self.led_count):
            self.state[i] = (0, 0, 0)
        self.update()

    def update(self):
        for i in range(0, self.led_count):
            LightStrip.pixels[i] = self.state.get(i,  (0, 0, 0))

        LightStrip.pixels.show()

