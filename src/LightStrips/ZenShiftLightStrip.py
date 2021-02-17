import time
import random
from src.LightStrips.LightStrip import LightStrip
from src.constants import MAX_INTENSITY, ZEN_STEADY_PERIOD, ZEN_SHIFT_PERIOD
from src.utils import clamp_int, get_random_rgb


class ZenShiftLightStrip(LightStrip):
    def __init__(
        self,
        zen_steady_period=ZEN_STEADY_PERIOD,
        zen_shift_period=ZEN_SHIFT_PERIOD,
        led_count=None
    ):
        if not led_count:
            super().__init__()
        else:
            super().__init__(led_count=led_count)

        self.zen_steady_period = zen_steady_period * pow(10, 9) # put seconds into ns
        self.zen_shift_period = zen_shift_period * pow(10, 9) # put  seconds into ns

        self.transition = { 
            'complete': False,
            'target': self.get_next_target(),
            'current': (0,0,0),
            'slope': None,
            'intercept': None,
        } # keep track of transition
        self.time_of_last_state = time.time_ns()

    def get_next_state(self):
        next_state = self.state # default is to keep steady state

        if not self.transition['complete']:
            next_state = self.get_next_transition_state()

        # check if we are not in a transition state and need to start it
        elif (time.time_ns() - self.time_of_last_state) > self.zen_steady_period:
            self.transition = {
                'target': self.get_next_target(),
                'current': self.transition['current'],
                'complete': False,
                'slope': None,
                'intercept': None,
            }
            self.time_of_last_state = time.time_ns()
            next_state = self.get_next_transition_state()
        
        self.state = next_state

    def get_next_transition_state(self):
        if self.transition['complete'] or self.transition['target'] == self.transition['current']:
            self.transition['complete'] = True
            self.time_of_last_state = time.time_ns()
            return self.state
        
        # determine slope if it doesnt exist
        if not self.transition['slope']:
            (targ_red, targ_green, targ_blue) = self.transition['target']
            (curr_red, curr_green, curr_blue) = self.transition['current']
            red_slope = (targ_red - curr_red) / self.zen_shift_period
            green_slope = (targ_green - curr_green) / self.zen_shift_period
            blue_slope = (targ_blue - curr_blue) / self.zen_shift_period
            
            self.transition['slope'] = (red_slope, green_slope, blue_slope)
            self.transition['intercept'] = (curr_red, curr_green, curr_blue)

        # figure out current state by multiplying slope and time elapsed
        (red_slope, green_slope, blue_slope) = self.transition['slope']
        (red_intercept, green_intercept, blue_intercept) = self.transition['intercept']
        time_elapsed = time.time_ns() - self.time_of_last_state

        next_state_red = clamp_int((red_slope * time_elapsed) + red_intercept, low=0, high=MAX_INTENSITY) 
        next_state_green = clamp_int((green_slope * time_elapsed) + green_intercept, low=0, high=MAX_INTENSITY) 
        next_state_blue = clamp_int((blue_slope * time_elapsed) + blue_intercept, low=0, high=MAX_INTENSITY)

        self.transition['current'] = (next_state_red, next_state_green, next_state_blue)
        next_state = {}
        for i in range(0, self.led_count):
            next_state[i] = (next_state_red, next_state_green, next_state_blue)

        return next_state

    def get_next_target(self):
        return get_random_rgb()
