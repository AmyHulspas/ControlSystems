#Plot: has at least a time domain plot with accurate measurements 
# and a setpoint that can be changed.

#Data: The Rise time, Settling time and Overshoot based are 
# calculated automatically based on real-time measurements with no 
# mistakes and made visual in the plot.

import sys
import random
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

def readMeasurement():
    #For now we just randomize a number,
    #this will get replaced with the PID measurements
    return random.uniform(-1.0, 1.0)

def plotMeasurements(_window):
    plot = _window.addPlot(title="measurements")
    plot.setLabel("bottom", "Time")
    plot.setLabel("left", "Measurements")

    plotTime = list(range(1, 50))
    #Pythonic way of iterating over plotTime and calling the function
    plotValues = [readMeasurement() for t in plotTime] 

    myPlot = plot.plot(plotTime, plotValues)

    return _window

def runInterface():
    #sys.arg is a required argument for QApplication,
    #it allows sys.argv to read arguments from the command line 
    pidInterfaceApp = QtWidgets.QApplication(sys.argv) #Create the application
    window = pg.GraphicsLayoutWidget(show=True, title="PID measurements") #Create the window
    window.show() #Show the window to the user

    window = plotMeasurements(window)

    #This function essentially behaves like two seperate functions
    #First 'pidInterfaceApp.exec_()' runs the application and all it's logic
    #When the application window is closed, 
    #'sys.exit' makes sure the application exits cleanly.
    sys.exit(pidInterfaceApp.exec_())


runInterface()