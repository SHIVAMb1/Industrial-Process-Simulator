import sys
import random
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QDateTime
import pyqtgraph as pg
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QLCDNumber,
    QProgressBar,
    QTableWidget,
    QWidget,
    QVBoxLayout
)
from collections import deque
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QLCDNumber,
    QProgressBar,
    QTableWidget,
    QWidget
)
tempData = deque(maxlen=50)
pressureData = deque(maxlen=50)
levelData = deque(maxlen=50)

xData = deque(maxlen=50)
counter = 0

def updateValues():
    global temperature, pressure, level

    if pumpRunning:

        # Temperature rises slowly until 40°C
        if temperature < 40:
            temperature += 0.3

        # Pressure rises until 2.5 bar
        if pressure < 2.5:
            pressure += 0.05

        # Tank fills until 100%
        if level < 100:
            level += 1

        lcdTemperature.display(round(temperature, 1))
        lcdPressure.display(round(pressure, 2))
        lcdLevel.display(level)
        progressLevel.setValue(level)
        lblStatus.setText("NORMAL")
        global counter

        counter += 1

        # Temperature Status
        if temperature < 20:
            tempn.setText("NORMAL")
        elif temperature < 25:
            tempn.setText("HIGH TEMP")
        else:
            tempn.setText("OVERHEATED")

# Pressure Status
        if pressure < 2.3:
            barn.setText("NORMAL")
        elif pressure < 2.55:
            barn.setText("HIGH PRESSURE")
        else:
            barn.setText("MAX PRESSURE")

        # Tank Status
        if level < 90:
            tankn.setText("NORMAL")
        elif level < 100:
            tankn.setText("HIGH LEVEL")
        else:
            tankn.setText("TANK FULL")

        xData.append(counter)
        tempData.append(temperature)
        pressureData.append(pressure)
        levelData.append(level)

        tempCurve.setData(list(xData), list(tempData))
        pressureCurve.setData(list(xData), list(pressureData))
        levelCurve.setData(list(xData), list(levelData))
        # Alarm logic
        if 90 <= level < 100:
            lblAlarm.setText("HIGH LEVEL WARNING")
            lblAlarmMessage.setText("Tank level has exceeded 90%. Please monitor the process.")
            lblStatus.setText("WARNING")
            addEvent("High Level Warning")

        elif level >= 100:
            lblAlarm.setText("TANK FULL")
            lblAlarmMessage.setText("Tank is full. Pump stopped to prevent overflow.")
            lblStatus.setText("TANK FULL")
            addEvent("Tank Full")
            stopPump()

        else:
            lblAlarm.setText("SYSTEM NORMAL")
            lblAlarmMessage.setText("All parameters are within normal range.")

from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer
temperature = 0
pressure = 0
level = 0
pumpRunning = False
app = QApplication(sys.argv)

loader = QUiLoader()

ui_file = QFile("industrial_hmi.ui")
ui_file.open(QFile.ReadOnly)

window = loader.load(ui_file)
ui_file.close()

# Find Widgets
# Find Widgets
btnStart = window.findChild(QPushButton, "btnStart")
btnStop = window.findChild(QPushButton, "btnStop")

lblPumpStatus = window.findChild(QLabel, "lblPumpStatus")
lblValveStatus = window.findChild(QLabel, "lblValveStatus")
lblAlarm = window.findChild(QLabel, "lblAlarm")

lcdTemperature = window.findChild(QLCDNumber, "lcdTemperature")
lcdPressure = window.findChild(QLCDNumber, "lcdPressure")
lcdLevel = window.findChild(QLCDNumber, "lcdLevel")
btnReset = window.findChild(QPushButton, "btnReset")
dateTime = window.findChild(QLabel, "dateTime")
lblStatus = window.findChild(QLabel, "lblStatus")
tempn = window.findChild(QLabel, "tempn")
barn = window.findChild(QLabel, "barn")
tankn = window.findChild(QLabel, "tankn")
progressLevel = window.findChild(QProgressBar, "progressLevel")

# Image Labels
thermometer = window.findChild(QLabel, "thermometer")
motor = window.findChild(QLabel, "motor")
valve = window.findChild(QLabel, "valve")
scale = window.findChild(QLabel, "scale")
#scale2 = window.findChild(QLabel, "scale2")
bar = window.findChild(QLabel, "bar")
tank = window.findChild(QLabel, "tank")
lblAlarmMessage = window.findChild(QLabel, "lblAlarmMessage")
eventTable = window.findChild(QTableWidget, "eventTable")
# Load Images
thermometer.setPixmap(QPixmap("assets/thermometer.png"))
motor.setPixmap(QPixmap("assets/motor.png"))
valve.setPixmap(QPixmap("assets/valve.png"))
scale.setPixmap(QPixmap("assets/scale.png"))
#scale2.setPixmap(QPixmap("assets/scale2.png"))
bar.setPixmap(QPixmap("assets/bar.png"))
tank.setPixmap(QPixmap("assets/tank.png"))

# Fit images inside labels
for label in [thermometer, motor, valve, scale, bar, tank]:
    label.setScaledContents(True)
# Graph Widgets
graphTemperature = window.findChild(QWidget, "graphTemperature")
graphPressure = window.findChild(QWidget, "graphPressure")
graphLevel = window.findChild(QWidget, "graphLevel")

print("Temp:", graphTemperature)
print("Pressure:", graphPressure)
print("Level:", graphLevel)

# Create layouts
tempLayout = QVBoxLayout(graphTemperature)
pressureLayout = QVBoxLayout(graphPressure)
levelLayout = QVBoxLayout(graphLevel)

# Create PlotWidgets
tempPlot = pg.PlotWidget()
pressurePlot = pg.PlotWidget()
levelPlot = pg.PlotWidget()

# Create Curves
tempCurve = tempPlot.plot(pen='r')
pressureCurve = pressurePlot.plot(pen='b')
levelCurve = levelPlot.plot(pen='g')

# Add PlotWidgets to layouts
tempLayout.addWidget(tempPlot)
pressureLayout.addWidget(pressurePlot)
levelLayout.addWidget(levelPlot)

# Titles
tempPlot.setTitle("Temperature")
pressurePlot.setTitle("Pressure")
levelPlot.setTitle("Tank Level")

# Optional
tempPlot.showGrid(x=True, y=True)
pressurePlot.showGrid(x=True, y=True)
levelPlot.showGrid(x=True, y=True)

lcdTemperature.display(temperature)
lcdPressure.display(pressure)
lcdLevel.display(level)
progressLevel.setValue(level)

'''print(lcdTemperature)
print(lcdPressure)
print(lcdLevel)
print(progressLevel)'''

# Functions
def startPump():
    global pumpRunning
    pumpRunning = True
    lblPumpStatus.setText("RUNNING")
    lblValveStatus.setText("OPEN")
    lblStatus.setText("RUNNING")
    addEvent("Pump Started")
    addEvent("Valve Opened")


def stopPump():
    global pumpRunning

    print("STOP PUMP CALLED")

    pumpRunning = False
    lblPumpStatus.setText("STOPPED")
    lblValveStatus.setText("CLOSED")
    lblStatus.setText("STOPPED")
    addEvent("Pump Stopped")
    addEvent("Valve Closed")

def resetAlarm():
    if level >= 100:
        lblAlarm.setText("TANK FULL")
        lblAlarmMessage.setText("Tank is full. Pump stopped to prevent overflow.")

    elif level >= 90:
        lblAlarm.setText("HIGH LEVEL WARNING")
        lblAlarmMessage.setText("Tank level has exceeded 90%. Please monitor the process.")

    else:
        lblAlarm.setText("SYSTEM NORMAL")
        lblAlarmMessage.setText("All parameters are within normal range.")
        lblStatus.setText("NORMAL")
        addEvent("Alarm Reset")
        
from PySide6.QtCore import QTime

def addEvent(message):
    row = eventTable.rowCount()
    eventTable.insertRow(row)

    eventTable.setItem(row, 0, QTableWidgetItem(QTime.currentTime().toString("HH:mm:ss")))
    eventTable.setItem(row, 1, QTableWidgetItem(message))

    eventTable.scrollToBottom()

def updateDateTime():
    current = QDateTime.currentDateTime()
    dateTime.setText(current.toString("dd-MMM-yyyy  hh:mm:ss AP"))

from PySide6.QtWidgets import QTableWidgetItem   
# Connect Buttons
btnStart.clicked.connect(startPump)
btnStop.clicked.connect(stopPump)
btnReset.clicked.connect(resetAlarm)


timer = QTimer()
timer.timeout.connect(updateValues)
timer.start(1000)

clockTimer = QTimer()
clockTimer.timeout.connect(updateDateTime)
clockTimer.start(1000)

updateDateTime()

window.show()

sys.exit(app.exec())