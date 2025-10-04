import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

class Interface:
    def __init__(self):
        self.__plotDistance = None
        self.__plotSetpoint = None
        self.__plotError = None
        self.__plotWindow = None
        self.__pidInterfaceApp = None
        self.__timer = None

    def plotMeasurements(self, _controller) -> None:
        distance = _controller.getCurrentDistance()
        setpoint = _controller.getCurrentSetpoint()
        currentTime = _controller.getCurrentTime()

        _controller.measurements.append(distance)
        _controller.timeStamps.append(currentTime)
        _controller.setPoints.append(setpoint)

        error = abs(distance - setpoint) #Calculate the error
        _controller.errors.append(error)

        #Plot the distance measurement and setpoint in realtime
        if self.__plotDistance is not None:
            self.__plotDistance.setData(_controller.timeStamps, _controller.measurements)
        if self.__plotSetpoint is not None:
            self.__plotSetpoint.setData(_controller.timeStamps, _controller.setPoints)

        #Plot the overshoot in realtime
        if self.__plotError is not None:
            self.__plotError.setData(_controller.timeStamps, _controller.errors)

    def runInterface(self, _function, _distance: float) -> None:
        self.__pidInterfaceApp = QtWidgets.QApplication(sys.argv)
        self.__plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements")

        self.showMeasuredPlot(_distance)
        self.showAnalysisPlot(_distance)

        self.runUpdateFunction(_function)

    def showMeasuredPlot(self, _distance: float) -> None:
        plot = self.__plotWindow.addPlot(title="Real time measurements")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Time")
        plot.setLabel("left", "Measurements")
        plot.setYRange(0, _distance)

        self.__plotDistance = plot.plot(pen=pg.mkPen(color="blue"))
        self.__plotSetpoint = plot.plot(pen=pg.mkPen(color="green", style=Qt.DashLine, dash=[25, 30]))

        self.__plotWindow.nextRow()

    def showAnalysisPlot(self, _distance: float) -> None:
        plot = self.__plotWindow.addPlot(title="Analysis")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Time")
        plot.setLabel("left", "Error (cm)")
        plot.setYRange(0, _distance)

        self.__plotError = plot.plot(pen=pg.mkPen(color="red"))

    def runUpdateFunction(self, _function) -> None:
        if _function is None: 
            return
        
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(_function)
        self.__timer.start(30)

    def exitInterface(self) -> None:
        sys.exit(self.__pidInterfaceApp.exec_())
