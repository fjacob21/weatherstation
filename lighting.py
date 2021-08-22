import time


class Lighting(object):
    RED = 0x880000
    GREEN = 0x008800
    BLUE = 0x000088
    YELLOW = 0x884400
    CYAN = 0x0088BB
    MAGENTA = 0x9900BB
    WHITE = 0x888888


    def __init__(self, magtag):
        self._magtag = magtag
        self._blink_start = 0.0
        self._blink_duration = 0.0

    @property
    def is_blink_started(self):
        return self._blink_start != 0.0 and self._blink_duration != 0.0

    def blink(self, color, duration):
        self._magtag.peripherals.neopixel_disable = False
        self._magtag.peripherals.neopixels.fill(color)
        self._blink_start = time.monotonic()
        self._blink_duration = duration

    def update(self):
        if  self.is_blink_started:
            if time.monotonic() - self._blink_start >= self._blink_duration:
                self._magtag.peripherals.neopixel_disable = True
                self._blink_start = 0.0
                self._blink_duration = 0.0
