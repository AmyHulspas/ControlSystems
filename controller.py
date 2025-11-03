import serial
from collections import deque

class Controller:
    def __init__(self):
        self.measurements: deque[float] = deque(maxlen=100)
        self.setPoints: deque[float] = deque(maxlen=100)
        self.timeStamps: deque[float] = deque(maxlen=100)
        self.errors: deque[float] = deque(maxlen=100)

        self.__serial = serial.Serial(port="COM4", baudrate=115200, timeout=1)
        self.__currentDistance: float = 0
        self.__currentSetpoint: int = 0
        self.__currentTime: int = 0
        self.__maxBeamDistance: float = 50

        self.__tolerancePercentage: float = 0.05
        self.__isSettled: bool = False
        self.__settlingTime: float = None
        self.__withinToleranceCounter: int = 0
        self.__requiredSettledSteps: int = 10

    def readSerial(self) -> None:
        line = self.__serial.readline()
        decodedLine = line.decode().strip()
        values = decodedLine.split(",")

        self.__currentDistance = float(values[0])
        self.__currentSetpoint = int(values[1])
        self.__currentSetpoint = self.convertRawToSetpoint(self.__currentSetpoint)

    def getCurrentDistance(self) -> float:
        return self.__currentDistance
    
    def getCurrentSetpoint(self) -> int:
        return self.__currentSetpoint
    
    def getMaxDistance(self) -> float:
        return self.__maxBeamDistance
    
    def getCurrentTime(self) -> float:
        return self.__currentTime
    
    def incremementTime(self) -> None:
        self.__currentTime += 1

    def convertRawToSetpoint(self, _value: int):
        return (_value/4095.0) * self.__maxBeamDistance

    def updateSettlingTime(self) -> None:
        if self.__isSettled:
            return

        currentValue = self.__currentDistance
        setpoint = self.__currentSetpoint
        tolerance = abs(setpoint * self.__tolerancePercentage)
        lowerBound = setpoint - tolerance
        upperBound = setpoint + tolerance

        if lowerBound <= currentValue <= upperBound:
            self.__withinToleranceCounter += 1
            if self.__withinToleranceCounter >= self.__requiredSettledSteps:
                self.__isSettled = True
                self.__settlingTime = self.__currentTime - self.__requiredSettledSteps
        else:
            self.__withinToleranceCounter = 0

    def getSettlingTime(self) -> float:
        return self.__settlingTime
    
    def getToleranceBounds(self) -> tuple:
        setpoint = self.__currentSetpoint
        tolerance = abs(setpoint * self.__tolerancePercentage)
        return (setpoint - tolerance, setpoint + tolerance)
