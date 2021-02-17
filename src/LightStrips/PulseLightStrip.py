import random
import time
from src.constants import (
    MAX_INTENSITY,
    PULSE_STEADY_PERIOD,
    PULSE_SHIFT_PERIOD,
    PULSE_SHIFT_STEP
)
from src.utils import clamp_int, get_random_rgb
from src.LightStrips.LightStrip import LightStrip

class PulseLightStrip(LightStrip):
    def __init__(
        self,
        pulse_steady_period=PULSE_STEADY_PERIOD,
        pulse_shift_period=PULSE_SHIFT_PERIOD,
        led_count=None
    ):
        if not led_count:
            super().__init__()
        else:
            super(led_count=led_count)
    
        self.middle = (self.led_count // 2) + 1
        self.values = []
        for i in range(0, self.middle):
            self.values.append((0, 0, 0))
        
        self.pulse_steady_period = pulse_steady_period * pow(10, 9) # put seconds into ns
        self.pulse_shift_period = pulse_shift_period * pow(10, 9) # put  seconds into ns

        self.transition = { 
            'complete': False,
            'target': (0, 0, 0),
            'current': (0, 0, 0),
            'slope': None,
            'intercept': None,
        } # keep track of transition

        self.transition['target'] = self.get_next_target()
        self.time_of_last_state = time.time_ns()
    
    def get_next_state(self, intensity=None):
        next_value = self.transition['current'] # default is to keep steady state

        if not self.transition['complete']:
            next_value = self.get_next_transition_value()
        # check if we are not in a transition state and need to start it
        elif (time.time_ns() - self.time_of_last_state) > self.pulse_steady_period:
            self.transition = {
                'target': self.get_next_target(),
                'current': self.transition['current'],
                'complete': False,
                'slope': None,
                'intercept': None,
            }
            self.time_of_last_state = time.time_ns()
            next_value = self.get_next_transition_value()
        
        self.add_next_value(next_value)
        self.add_next_value(next_value)

        count = 0
        next_state = {}
        # iterate from middle outwards
        for low_index in range(self.middle - 1, -1, -1):
            high_index = self.middle + (self.middle - low_index)

            value = self.values[count]
            count += 1

            next_state[low_index] = value
            next_state[high_index] = value
        next_state[self.middle] = self.transition['target']

        self.state = next_state 

    
    def add_next_value(self, value):
        # remove last element in list and add new value
        self.values.pop(0)
        self.values.append(value)
    
    def get_next_transition_value(self):
        if self.transition['complete'] or self.transition['target'] == self.transition['current']:
            self.transition['complete'] = True
            self.time_of_last_state = time.time_ns()
            return self.transition['current']
        
        # determine slope if it doesnt exist
        if not self.transition['slope']:
            (targ_red, targ_green, targ_blue) = self.transition['target']
            (curr_red, curr_green, curr_blue) = self.transition['current']
            red_slope = (targ_red - curr_red) / self.pulse_shift_period
            green_slope = (targ_green - curr_green) / self.pulse_shift_period
            blue_slope = (targ_blue - curr_blue) / self.pulse_shift_period
            
            self.transition['slope'] = (red_slope, green_slope, blue_slope)
            self.transition['intercept'] = (curr_red, curr_green, curr_blue)

        # figure out current state by multiplying slope and time elapsed
        (red_slope, green_slope, blue_slope) = self.transition['slope']
        (red_intercept, green_intercept, blue_intercept) = self.transition['intercept']
        time_elapsed = time.time_ns() - self.time_of_last_state

        next_state_red = clamp_int((red_slope * time_elapsed) + red_intercept, low=0, high=MAX_INTENSITY, step=PULSE_SHIFT_STEP) 
        next_state_green = clamp_int((green_slope * time_elapsed) + green_intercept, low=0, high=MAX_INTENSITY, step=PULSE_SHIFT_STEP) 
        next_state_blue = clamp_int((blue_slope * time_elapsed) + blue_intercept, low=0, high=MAX_INTENSITY, step=PULSE_SHIFT_STEP)

        self.transition['current'] = (next_state_red, next_state_green, next_state_blue)
        return self.transition['current']
    
    def get_next_target(self):
        next_target = get_random_rgb()
        while next_target == self.transition['target']:
            next_target = get_random_rgb()
        return next_target

