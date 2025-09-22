import random

class Controller:
    def __init__(self):
        self.time = 0
        self.measurements = []
        self.timeStamps = []

        print("CREATED CONTROLLER")

    def readMeasurement(self):
        #For now we just randomize a number,
        #this will get replaced with the PID measurements
        return random.uniform(-1.0, 1.0)
