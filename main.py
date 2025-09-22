import controller as pid
import interface
import sys
from PyQt5 import QtWidgets, QtCore

controller = pid.Controller()
myInterface = interface.Interface()

def update():
    value = controller.readMeasurement()

    myInterface.plotMeasurements(value, myInterface.currentTime)
    myInterface.currentTime += 1

if __name__ == "__main__":
    myInterface.runInterface(update)
    myInterface.exitInterface()