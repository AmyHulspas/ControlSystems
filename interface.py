import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

class Interface:
    def __init__(self):
        self.__plotDistance = None
        self.__plotSetpoint = None
        self.__plotWindow = None
        self.__pidInterfaceApp = None
        self.__timer = None

    def plotMeasurements(self, _controller):

        _controller.measurements.append(_controller.getCurrentDistance())
        _controller.timeStamps.append(_controller.getCurrentTime())
        _controller.setPoints.append(_controller.getCurrentSetpoint())

        if len(_controller.measurements) > 100:
            _controller.measurements.pop(0)
            _controller.timeStamps.pop(0)
            _controller.setPoints.pop(0)

        if self.__plotDistance is not None:
            self.__plotDistance.setData(_controller.timeStamps, _controller.measurements)

        if self.__plotSetpoint is not None:
            self.__plotSetpoint.setData(_controller.timeStamps, _controller.setPoints)

    def runInterface(self, _function, _distance:float):
        self.__pidInterfaceApp = QtWidgets.QApplication(sys.argv)
        self.__plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements")

        self.showPlot(_distance)

        self.runUpdateFunction(_function)

    def showPlot(self, _distance: float):
        plot = self.__plotWindow.addPlot(title="Real time measurements")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Time")
        plot.setLabel("left", "Measurements")
        plot.setYRange(0, _distance)

        self.__plotDistance = plot.plot(pen=pg.mkPen(color="blue"))
        self.__plotSetpoint = plot.plot(pen=pg.mkPen(color="green", style=Qt.DashLine, dash=[25, 30]))

        self.__plotWindow.nextCol()
    
    def runUpdateFunction(self, _function):
        if _function is None: 
            return
        
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(_function)
        self.__timer.start(10)

    def exitInterface(self):
        sys.exit(self.__pidInterfaceApp.exec_())
