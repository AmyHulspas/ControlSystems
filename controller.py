import random
import serial

class Controller:
    def __init__(self):
        self.currentTime: int = 0
        self.measurements: list = []
        self.timeStamps: list = []

        self.serial = serial.Serial(port="COM4", baudrate=115200, timeout=1)
        self.currentDistance: float = 0
        self.currentSetpoint: int = 0

    def readMeasurement(self) -> float:
        #For now we just randomize a number,
        #this will get replaced with the PID measurements
        return self.currentDistance
    
    def incremementTime(self) -> None:
        self.currentTime += 1

    def readSerial(self) -> None:
        line = self.serial.readline()
        decodedLine = line.decode().strip()
        values = decodedLine.split(",")

        self.currentDistance = float(values[0])
        self.currentSetpoint = int(values[1])

        print(f"Distance = {self.currentDistance}, setpoint = {self.currentSetpoint}")
