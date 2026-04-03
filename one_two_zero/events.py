from python_obs.clients import OBS
from typing import Callable

import time
import warnings

class OTZEvent:
    def __init__(self, condition: Callable[[float], bool], on_condition_met) -> None:
        self._condition = condition
        self.on_condition_met = on_condition_met
        self.has_run: bool = False
        
        self.is_timer_event: bool = False
        self._last_time_checked: float | None = None
        self.elapsed_time: float = 0
        self.activation_time: float | None = None

    def on_condition_met(self, obs: OBS) -> None:
        warnings.warn("Unbound `on_condition_met` called.", RuntimeWarning)

    def has_condition_met(self, value: float) -> bool:
        if self.is_timer_event:
            if self.activation_time == None:
                return False
            
            return self.elapsed_time >= self.activation_time
        else:
            return self._condition(value) and not self.has_run
    
    def initialise_timer_event(self, activation_time: float):
        self.is_timer_event = True
        self._last_time_checked = time.time()
        self.activation_time = activation_time
        self.elapsed_time = 0
    
    def update_timer(self):
        if not self.is_timer_event: return

        current_time = time.time()
        if self._last_time_checked == None:
            self._last_time_checked = current_time
        
        delta_time = current_time - self._last_time_checked
        self.elapsed_time += delta_time
        
        self._last_time_checked = current_time