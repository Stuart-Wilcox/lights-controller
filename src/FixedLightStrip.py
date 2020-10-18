import random
from constants import MAX_INTENSITY, SCALE_FACTOR
from LightStrip import LightStrip


class FixedLightStrip(LightStrip):
    def __init__(self, led_count=None):
        if not led_count:
            super().__init__()
        else:
            super().__init__(led_count=led_count)

        self.low = self.led_count // 4
        self.mid = self.led_count // 5
        self.high = self.led_count // 10

    def get_next_state(self, intensity=None):
        if not intensity:
            intensity = (random.random(), random.random(), random.random())

        next_state = {}

        low_value = self.__calc_low__(intensity[0])
        mid_value = self.__calc_mid__(intensity[1])
        high_value = self.__calc_high__(intensity[2])

        index = 0

        for i in range(index, index + self.low):
            next_state[i] = low_value
        index = index + self.low

        for i in range(index, index + self.mid):
            next_state[i] = mid_value
        index = index + self.mid
        
        for i in range(index, index + self.high):
            next_state[i] = high_value
        index = index + self.high

        for i in range(index, index + self.mid):
            next_state[i] = mid_value
        index = index + self.mid
        
        for i in range(index, index + self.low):
            next_state[i] = low_value

        self.state = next_state

    def __calc_low__(self, intensity):
        # scale down other two colours
        primary_intensity = int(intensity * MAX_INTENSITY)
        secondary_intensity = int(primary_intensity / SCALE_FACTOR)
        return (primary_intensity, secondary_intensity, secondary_intensity)

    def __calc_mid__(self, intensity):
        primary_intensity = int(intensity * MAX_INTENSITY)
        secondary_intensity = int(primary_intensity / SCALE_FACTOR)
        return (secondary_intensity, primary_intensity, secondary_intensity)

    def __calc_high__(self, intensity):
        primary_intensity = int(intensity * MAX_INTENSITY)
        secondary_intensity = int(primary_intensity / SCALE_FACTOR)
        return (secondary_intensity, secondary_intensity, primary_intensity)

