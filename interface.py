import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class Interface:
    def __init__(self):
        self.__plotReading = None
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

        if self.__plotReading is not None:
            self.__plotReading.setData(_controller.timeStamps, _controller.measurements)

        if self.__plotSetpoint is not None:
            self.__plotSetpoint.setData(_controller.timeStamps, _controller.setPoints)

    def runInterface(self, _function, _distance:float):
        self.__pidInterfaceApp = QtWidgets.QApplication(sys.argv)
        self.__plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements")

        plot = self.__plotWindow.addPlot(title="Real time measurements")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Time")
        plot.setLabel("left", "Measurements")
        plot.setYRange(0, _distance)

        self.__plotReading = plot.plot()
        self.__plotSetpoint = plot.plot(pen=pg.mkPen(color=(255, 0, 0), style=QtCore.Qt.DotLine))

        self.runUpdateFunction(_function)

    def runUpdateFunction(self, _function):
        if _function is None: 
            return
        
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(_function)
        self.__timer.start(10)

    def exitInterface(self):
        sys.exit(self.__pidInterfaceApp.exec_())
