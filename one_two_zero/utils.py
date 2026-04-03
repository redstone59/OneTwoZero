from datetime import datetime

def current_time_str(format = "%H:%M:%S") -> str:
    return datetime.strftime(datetime.now(), format)

def otz_log(msg: str):
    print(f"[{current_time_str()}] {msg}")