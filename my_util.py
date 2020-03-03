import time

class Timer:
    def __init__(self, period_in_minutes):
        self.period= period_in_minutes

    def start(self):
        self.start_time = time.time()

    def out_of_time(self):
        time_since_start = time.time() - self.start_time
        if time_since_start > self.period*60:
            return True
        return False

    def reset(self):
        self.start_time = None 