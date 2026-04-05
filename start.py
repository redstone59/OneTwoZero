from python_obs.clients import OBS
from one_two_zero.core import OneTwoZero
from one_two_zero.decorators import *

KILL_TIME = 70
otz = OneTwoZero(KILL_TIME)
otz.buffer_time = 5
otz.debug_mode = True

@otz_event_on_start(otz)
def on_startup(obs: OBS):
    obs.set_scene("120 Wait")

@otz_event_seconds(otz, lambda uptime: uptime >= 3 * 60)
def and_we_are_live(obs: OBS):
    obs.set_scene("120 Desktop")

@otz_event_seconds(otz, lambda uptime: uptime >= KILL_TIME - 60)
def one_minute_left(obs: OBS):
    obs.call_macro("120 1 minute left")

@otz_event_seconds(otz, lambda uptime: uptime >= KILL_TIME - 10 * 60)
def ten_minutes_left(obs: OBS):
    obs.call_macro("120 10 minutes left")

@otz_event_seconds(otz, lambda uptime: uptime >= KILL_TIME - 30 * 60)
def thirty_minutes_left(obs: OBS):
    obs.call_macro("120 30 minutes left")

@otz_event_repeating(otz, 1)
def test_repeating(obs: OBS):
    source = obs.scene("120 Desktop").source("warning tex")
    source.toggle_visiblity()

if __name__ == "__main__":
    otz.start_stream()