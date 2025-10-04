#Plot: has at least a time domain plot with accurate measurements 
# and a setpoint that can be changed.

#Data: The Rise time, Settling time and Overshoot based are 
# calculated automatically based on real-time measurements with no 
# mistakes and made visual in the plot.

import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class Interface:
    def __init__(self):
        self.__plotReading = None
        self.__plotWindow = None
        self.__pidInterfaceApp = None
        self.__timer = None

    def plotMeasurements(self, _controller):

        _controller.measurements.append(_controller.readMeasurement())
        _controller.timeStamps.append(_controller.currentTime)

        if len(_controller.measurements) > 100:
            _controller.measurements.pop(0)
            _controller.timeStamps.pop(0)

        # Update the plot
        if self.__plotReading is not None:
            self.__plotReading.setData(_controller.timeStamps, _controller.measurements)

    def runInterface(self, _function):
        #sys.arg is a required argument for QApplication,
        #it allows sys.argv to read arguments from the command line 
        self.__pidInterfaceApp = QtWidgets.QApplication(sys.argv) #Create the application
        self.__plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements") #Create the window

        plot = self.__plotWindow.addPlot(title="Real time measurements")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Mesaurements")
        plot.setLabel("left", "Time")

        self.__plotReading = plot.plot()

        self.runUpdateFunction(_function)

    def runUpdateFunction(self, _function):
        if _function is None: 
            return
        
        #Call the update function
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(_function)
        self.__timer.start(10)

    def exitInterface(self):
        #This function essentially behaves like two seperate functions
        #First 'pidInterfaceApp.exec_()' runs the application and all it's logic
        #When the application window is closed, 
        #'sys.exit' makes sure the application exits cleanly.
        sys.exit(self.__pidInterfaceApp.exec_())