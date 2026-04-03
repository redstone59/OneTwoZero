from one_two_zero.core import OneTwoZero
from one_two_zero.events import OTZEvent
from typing import Callable

def otz_event_seconds(otz: OneTwoZero, condition: Callable[[float], bool]):
    def decorator(func):
        event = OTZEvent(condition, func)
        otz.subscribe_to_event(event)
        
        return func
    
    return decorator

def otz_event_repeating(otz: OneTwoZero, seconds: float):
    def decorator(func):
        event = OTZEvent(lambda uptime: False, func)
        event.initialise_timer_event(seconds)
        otz.subscribe_to_event(event)
        
        return func
    
    return decorator