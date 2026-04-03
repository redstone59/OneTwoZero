from one_two_zero.events import OTZEvent
from one_two_zero.utils import otz_log
from python_obs.clients import OBS

import time
import threading
import queue

class OneTwoZero:
    def __init__(self, kill_time_seconds: float, host: str = "localhost", port: int = 4455, password: str | None = None) -> None:
        self._start_time = float('inf')
        self._obs = OBS(host, port, password)
        self._event_queue = queue.Queue()
        
        self.events: list[OTZEvent] = []
        self.kill_time = kill_time_seconds
        
        self.debug_mode = False

    def check_event(self, event: OTZEvent, uptime: float):
        if event.is_timer_event:
            event.update_timer()
            
        if event.has_condition_met(uptime):
            otz_log(f"Running {"repeating" if event.is_timer_event else "one-time"} event '{event.on_condition_met.__name__}'...")
            
            if event.is_timer_event and event.activation_time != None:
                event.elapsed_time -= event.activation_time
            else:
                event.has_run = True
            
            self._event_queue.put(lambda: event.on_condition_met(self._obs))

    def check_events(self):
        uptime = self.get_uptime()
        
        for event in self.events:
            self.check_event(event, uptime)

    def event_queue_loop(self):
        otz_log("Event queue thread running!")
        while self.get_uptime() < self.kill_time:
            if self._event_queue.empty(): continue

            event_to_run = self._event_queue.get()
            event_to_run()
        otz_log("Event queue thread stopped.")

    def get_uptime(self) -> float:
        if self._start_time == float('inf'):
            return 0
        
        return time.time() - self._start_time

    def start_stream(self) -> None:
        if self.debug_mode: 
            otz_log(f"Running in debug mode...")
        
        self._obs.connect()
        otz_log(f"Started stream with kill time of {self.kill_time}s")
        self._start_time = time.time()
        if not self.debug_mode: self._obs.start_stream()
        
        otz_log("Starting event queue thread...")
        event_queue_thread = threading.Thread(
            target = self.event_queue_loop
        )
        event_queue_thread.start()
        
        while self.get_uptime() < self.kill_time:
            self.check_events()

        otz_log(f"Ended stream after {time.time() - self._start_time:.2f}s")
        if not self.debug_mode: self._obs.end_stream()
        
        event_queue_thread.join()
    
    def subscribe_to_event(self, event: OTZEvent):
        self.events.append(event)