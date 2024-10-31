from collections import deque
import numpy as np
from collections import deque

class MedianFilter:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def add_value(self, value):
        self.values.append(value)
        return np.median(self.values)

# Example usage
mf = MedianFilter(window_size=5)
for distance in [10, 12, 11, 14, 13, 15, 16]:
    print(mf.add_value(distance))

class MovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def add_value(self, value):
        self.values.append(value)
        return sum(self.values) / len(self.values)

class ExponentialMovingAverage:
    def __init__(self, alpha):
        self.alpha = alpha
        self.current_average = None

    def add_value(self, value):
        if self.current_average is None:
            self.current_average = value
        else:
            self.current_average = (self.alpha * value) + ((1 - self.alpha) * self.current_average)
        return self.current_average

