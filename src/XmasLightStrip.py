from constants import MAX_INTENSITY
from LightStrip import LightStrip

class XmasLightStrip(LightStrip):
    def __init__(self, led_count=None):
        if led_count:
            super().__init__(led_count=led_count)
        else:
            super().__init__()
        self.count = 0

    def set_odd(self, value):
        for i in range(1, self.led_count, 2):
            self.state[i] = value

    def set_even(self, value):
        for i in range(0, self.led_count, 2):
            self.state[i] = value

    def get_next_state(self):
        if self.count % 2:
            # state 1
            self.set_odd((0, MAX_INTENSITY, 0))
            self.set_even((MAX_INTENSITY, 0, 0))
        else:
            # state 2
            self.set_odd((MAX_INTENSITY, 0, 0))
            self.set_even((0, MAX_INTENSITY, 0))

        self.count = self.count + 1
