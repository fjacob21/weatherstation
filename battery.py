import time
import board
from simpleio import map_range


class Battery(object):

    def __init__(self, magtag, max_level=3.3):
        self._magtag = magtag
        self._max_level = max_level

    @property
    def max_level(self):
        return self._max_level

    @property
    def level(self):
        return self._magtag.peripherals.battery

    @property
    def pourcentage(self):
        map_range(self.level, 2.4, 3.7, 0, 100)
        return int(map_range(self.level, 2.4, 3.7, 0, 100))
