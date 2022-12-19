
import time

#=== MY CLASS ===#
class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    def __init__(self, task):
        self._start_time = None
        self.text = task+": {:0.4f} seconds"

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(self.text.format(elapsed_time))
    
# Usage
# from timer import Timer
# t = Timer()
# t.start()

# t.stop()  # A few seconds later
# > Elapsed time: 3.8191 seconds
#================#
