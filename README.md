# Industrial Process Simulator (Water Treatment Plant HMI)

## About the Project

This project is a desktop-based Human Machine Interface (HMI) developed in Python to simulate a basic industrial water treatment process. It demonstrates how process parameters can be monitored and controlled in real time, similar to a simple SCADA system used in industrial automation.

The application provides live monitoring of temperature, pressure, and tank level while allowing the operator to control the pump and valve. It also includes alarm handling, event logging, and live trend graphs to visualize process data.

---

## Features

- Real-time monitoring of:
  - Temperature
  - Pressure
  - Tank Level

- Pump and Valve control

- Live trend graphs using PyQtGraph

- Event log with timestamps

- Alarm system for:
  - High Tank Level
  - Tank Full
  - High Temperature
  - High Pressure

- Automatic pump shutdown when the tank reaches full capacity

- Real-time date and time display

- Simple industrial-style HMI interface designed using Qt Designer

---

## Technologies Used

- Python
- PySide6
- Qt Designer
- PyQtGraph

---

## Project Structure

```
Industrial-Process-Simulator/
│
├── assets/
├── screenshots/
├── main.py
├── industrial_hmi.ui
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Industrial-Process-Simulator.git
```

### Navigate to the project folder

```bash
cd Industrial-Process-Simulator
```

### Install the required libraries

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python main.py
```

---

## Screenshots

### Dashboard

*Add a screenshot of the main dashboard here.*

### Live Trend Graphs

*Add a screenshot of the trend graphs here.*

### Event Log

*Add a screenshot of the event log here.*

---

## Future Improvements

Some features that can be added in future versions:

- User Login System
- Manual / Auto Mode
- Emergency Stop Button
- CSV Data Logging
- PLC Communication (Modbus)
- OPC UA Connectivity
- Report Generation

---

## Author

**Shivam Borane**

Electronics & Telecommunication Engineering
