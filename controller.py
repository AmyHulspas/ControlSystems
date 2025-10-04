import serial

class Controller:
    def __init__(self):
        self.measurements: list = []
        self.timeStamps: list = []
        self.currentTime: int = 0

        self.__serial = serial.Serial(port="COM4", baudrate=115200, timeout=1)
        self.__currentDistance: float = 0
        self.__currentSetpoint: int = 0

    def readMeasurement(self) -> float:
        return self.__currentDistance
    
    def incremementTime(self) -> None:
        self.currentTime += 1

    def readSerial(self) -> None:
        line = self.__serial.readline()
        decodedLine = line.decode().strip()
        values = decodedLine.split(",")

        self.__currentDistance = float(values[0])
        self.__currentSetpoint = int(values[1])

        print(f"Distance = {self.__currentDistance}, setpoint = {self.__currentSetpoint}")
