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
        self.__toleranceLineLower = None
        self.__toleranceLineUpper = None
        self.__settlingLabel = None

    def plotMeasurements(self, _controller) -> None:
        distance = _controller.getCurrentDistance()
        setpoint = _controller.getCurrentSetpoint()
        currentTime = _controller.getCurrentTime()

        _controller.measurements.append(distance)
        _controller.timeStamps.append(currentTime)
        _controller.setPoints.append(setpoint)

        error = (distance - setpoint)
        _controller.errors.append(error)

        if self.__plotDistance is not None:
            self.__plotDistance.setData(_controller.timeStamps, _controller.measurements)
        if self.__plotSetpoint is not None:
            self.__plotSetpoint.setData(_controller.timeStamps, _controller.setPoints)

        if self.__plotError is not None:
            self.__plotError.setData(_controller.timeStamps, _controller.errors)

        if self.__toleranceLineLower is not None and self.__toleranceLineUpper is not None:
            lower, upper = _controller.getToleranceBounds()
            self.__toleranceLineLower.setValue(lower)
            self.__toleranceLineUpper.setValue(upper)

    def runInterface(self, _function, _distance: float) -> None:
        self.__pidInterfaceApp = QtWidgets.QApplication(sys.argv)
        self.__plotWindow = pg.GraphicsLayoutWidget(show=True, title="PID measurements")

        self.showMeasuredPlot(_distance)
        self.__plotWindow.nextRow()
        self.showAnalysisPlot(_distance)

        self.createSettlingLabel()

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

        self.__toleranceLineLower = pg.InfiniteLine(angle=0, pen=pg.mkPen(color="red", style=Qt.DashLine))
        self.__toleranceLineUpper = pg.InfiniteLine(angle=0, pen=pg.mkPen(color="red", style=Qt.DashLine))
        plot.addItem(self.__toleranceLineLower)
        plot.addItem(self.__toleranceLineUpper)

    def showAnalysisPlot(self, _distance: float) -> None:
        plot = self.__plotWindow.addPlot(title="Analysis")
        plot.setMouseEnabled(x=False, y=False)
        plot.showGrid(x=True, y=True)
        plot.setLabel("bottom", "Time")
        plot.setLabel("left", "Error (cm)")
        plot.setYRange(-_distance, _distance)

        self.__plotError = plot.plot(pen=pg.mkPen(color="red"))

    def createSettlingLabel(self) -> None:
        labelProxy = QtWidgets.QGraphicsProxyWidget()
        self.__settlingLabel = QtWidgets.QLabel("Settling time: calculating...")
        
        #Make the background black and the text white
        self.__settlingLabel.setStyleSheet("QLabel { background-color: black; color: white; }")
        labelProxy.setWidget(self.__settlingLabel)
        self.__plotWindow.addItem(labelProxy)

    def updateSettlingDisplay(self, _controller) -> None:
        settlingTime = _controller.getSettlingTime()
        if settlingTime is None:
            self.__settlingLabel.setText("Settling time: calculating...")
        else:
            self.__settlingLabel.setText("Settling time: " + str(settlingTime))

    def runUpdateFunction(self, _function) -> None:
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(_function)
        self.__timer.start(30)

    def exitInterface(self) -> None:
        sys.exit(self.__pidInterfaceApp.exec_())
