import serial

class Controller:
    def __init__(self):
        self.measurements: list = []
        self.timeStamps: list = []
        self.setPoints: list = []

        self.__serial = serial.Serial(port="COM4", baudrate=115200, timeout=1)
        self.__currentDistance: float = 0
        self.__currentSetpoint: int = 0
        self.__currentTime: int = 0
        self.__maxBeamDistance: float = 50

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

    def readSerial(self) -> None:
        line = self.__serial.readline()
        decodedLine = line.decode().strip()
        values = decodedLine.split(",")

        self.__currentDistance = float(values[0])
        self.__currentSetpoint = int(values[1])
        self.__currentSetpoint = self.convertRawToSetpoint(self.__currentSetpoint)

        print(f"Distance = {self.__currentDistance}, setpoint = {self.__currentSetpoint}")
