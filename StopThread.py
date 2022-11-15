import time
import threading
import Colors

class RainbowThread(threading.Thread):
    def __init__(self, strip, *args, **kwargs):
        super(RainbowThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
        self._strip = strip
    
    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet()
    
    def run(self):
        self._stop = threading.Event()
        Colors.rainbow(self._strip, self)
            