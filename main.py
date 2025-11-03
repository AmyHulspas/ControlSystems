import controller as pid
import interface

controller = pid.Controller()
myInterface = interface.Interface()

def update():
    myInterface.plotMeasurements(controller)
    controller.incremementTime()
    controller.readSerial()
    controller.updateSettlingTime()
    myInterface.updateSettlingDisplay(controller)

if __name__ == "__main__":
    myInterface.runInterface(update, controller.getMaxDistance())
    myInterface.exitInterface()
