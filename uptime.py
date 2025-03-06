from datetime import datetime

start_time = ""

def start():
    global start_time
    start_time = datetime.now()

def get_uptime():
    uptime = datetime.now() - start_time
    return str(uptime).split('.')[0]