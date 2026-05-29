import time

class Heartbeat:
    def __init__(self, timeout=180):
        self.last_tick = time.time()
        self.timeout = timeout

    def ping(self):
        self.last_tick = time.time()

    def check(self):
        if time.time() - self.last_tick > self.timeout:
            return False
        return True
