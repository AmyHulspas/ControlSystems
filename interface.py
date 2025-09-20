#Plot: has at least a time domain plot with accurate measurements 
# and a setpoint that can be changed.

#Data: The Rise time, Settling time and Overshoot based are 
# calculated automatically based on real-time measurements with no 
# mistakes and made visual in the plot.

import sys
import random
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class Interface:
    def __init__(self):
        self.measurements = []
        self.timeValues = []
        self.currentTime = 0
        self.plotReading = None
        self.plotWindow = None

        self.runInterface()

    def update(self):
        value = self.readMeasurement()
        self.plotMeasurements(value, self.currentTime)
        self.currentTime += 1

    def readMeasurement(self):
        #For now we just randomize a number,
        #this will get replaced with the PID measurements
        return random.uniform(-1.0, 1.0)

    def plotMeasurements(self, _value, _time):

        self.measurements.append(_value)
        self.timeValues.append(_time)

        if len(self.measurements) > 100:
            self.measurements.pop(0)
            self.timeValues.pop(0)

        # Update the plot
        if self.plotReading is not None:
            self.plotReading.setData(self.timeValues, self.measurements)

    def runInterface(self):
        #sys.arg is a required argument for QApplication,
        #it allows sys.argv to read arguments from the command line 
        pidInterfaceApp = QtWidgets.QApplication(sys.argv) #Create the application
        plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements") #Create the window
        #plotWindow.show() #Show the window to the user

        plot = plotWindow.addPlot(title="Real time measurements")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Mesaurements")
        plot.setLabel("left", "Time")

        self.plotReading = plot.plot()

        #Call the update function
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)

        #This function essentially behaves like two seperate functions
        #First 'pidInterfaceApp.exec_()' runs the application and all it's logic
        #When the application window is closed, 
        #'sys.exit' makes sure the application exits cleanly.
        sys.exit(pidInterfaceApp.exec_())