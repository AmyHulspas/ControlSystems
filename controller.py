import random

class Controller:
    def __init__(self):
        self.currentTime = 0
        self.measurements = []
        self.timeStamps = []

    def readMeasurement(self):
        #For now we just randomize a number,
        #this will get replaced with the PID measurements
        return random.uniform(-1.0, 1.0)
    
    def incremementTime(self):
        self.currentTime += 1
