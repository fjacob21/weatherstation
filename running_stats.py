import math


class RunningStats(object):

    def __init__(self):
        self._count = 0
        self._min = 0
        self._max = 0
        self._oldM = 0
        self._newM = 0
        self._oldS = 0
        self._newS = 0

    def add(self, data):
        self._count += 1

        if self._count == 1:
            self._min = data
            self._max = data
            self._oldM = self._newM = data
            self._oldS = 0.0
        else:
            if data < self._min:
                self._min = data
            if data > self._max:
                self._max = data
            self._newM = self._oldM + (data - self._oldM)/self._count
            self._newS = self._oldS + (data - self._oldM)*(data - self._newM)

            self._oldM = self._newM
            self._oldS = self._newS

    @property
    def count(self):
        return self._count

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def mean(self):
        if self._count > 0:
            return self._newM
        return 0.0

    @property
    def variance(self):
        if self._count > 1:
            return self._newS/(self._count - 1)
        return 0.0

    @property
    def standard_deviation(self):
        return math.sqrt(self.Variance)
