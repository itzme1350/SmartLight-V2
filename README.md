# 💡 SmartLight V2

### MPU-6050 Gesture-Controlled Lighting System with Real-Time Python Dashboard

SmartLight V2 is an Arduino-based gesture-controlled lighting system that uses an MPU-6050 six-axis motion sensor to control LED brightness, lighting patterns, and power states through physical movements.

The project combines embedded C++, I²C communication, motion sensing, gesture detection, and Python-based visualization to create an interactive hardware-software system.

## Features

* **Gesture-Controlled Brightness:** Tilt forward or backward to adjust LED brightness.
* **Individual LED Activation:** Tilt left or right to change the number of active LEDs.
* **Shake Detection:** Toggle the lighting system ON/OFF.
* **Twist Recognition:** Switch between NORMAL and BREATHING lighting modes.
* **PWM Brightness Control:** Independently control four LEDs using PWM-capable pins.
* **Real-Time Dashboard:** Monitor motion sensor readings through a Python graphical interface.
* **3D Motion Visualization:** Display pitch and roll using an animated 3D wireframe.
* **Live Motion Graph:** Visualize pitch and roll changes in real time.
* **High-Speed Serial Communication:** Stream sensor readings at 115200 baud.

## Hardware Requirements

| Component                        | Quantity  |
| -------------------------------- | --------- |
| ELEGOO Mega 2560                 | 1         |
| MPU-6050 Gyroscope/Accelerometer | 1         |
| LEDs                             | 4         |
| 220Ω or 330Ω Resistors           | 4         |
| Breadboard                       | 1         |
| Jumper Wires                     | As needed |
| USB Cable                        | 1         |

## Wiring Connections

### MPU-6050 to Arduino Mega 2560

| MPU-6050 | Arduino Mega |
| -------- | ------------ |
| VCC      | 3.3V         |
| GND      | GND          |
| SDA      | Pin 20       |
| SCL      | Pin 21       |

### LED Connections

| LED   | Arduino Pin |
| ----- | ----------- |
| LED 1 | 9           |
| LED 2 | 10          |
| LED 3 | 11          |
| LED 4 | 5           |

Each LED connects through its own current-limiting resistor, with its cathode connected to GND.

## Gesture Controls

| Gesture                     | Function                |
| --------------------------- | ----------------------- |
| Tilt forward                | Increase brightness     |
| Tilt backward               | Decrease brightness     |
| Tilt right                  | Activate another LED    |
| Tilt left                   | Deactivate one LED      |
| Shake                       | Toggle lights ON/OFF    |
| Quick twist in +Z direction | Activate BREATHING mode |
| Quick twist in −Z direction | Return to NORMAL mode   |

Gesture directions depend on sensor orientation.

## Lighting Modes

### NORMAL

The active LEDs maintain a constant brightness determined by the user's tilt gestures.

### BREATHING

The active LEDs gradually increase and decrease in brightness using a sinusoidal waveform.

## Software Requirements

**Arduino**

* Arduino IDE
* Arduino Wire library

**Python**

* Python 3
* Pygame Community Edition (`pygame-ce`)
* PySerial (`pyserial`)

Install Python dependencies:

```bash
python -m pip install pygame-ce pyserial
```

## Running the Project

### Arduino Setup

1. Connect the MPU-6050 and LEDs according to the wiring tables.
2. Open `arduino/SmartLight_V2/SmartLight_V2.ino` in Arduino IDE.
3. Select Arduino Mega 2560.
4. Select the appropriate serial port.
5. Upload the firmware.

### Python Dashboard

1. Open `python/dashboard.py`.
2. Locate the serial configuration:

```python
PORT = "COM3"
BAUD = 115200
```

3. Change `COM3` to the Arduino's assigned serial port.
4. Save the file.
5. Close Arduino IDE Serial Monitor.
6. Launch the dashboard:

```bash
python python/dashboard.py
```

The graphical interface displays live sensor data and lighting status.

## How It Works

The MPU-6050 contains a three-axis accelerometer and three-axis gyroscope.

The accelerometer measures acceleration, including gravity, allowing the microcontroller to estimate pitch and roll.

The gyroscope measures angular velocity, which is used to recognize rapid rotational gestures.

The Arduino processes the measurements and determines which lighting actions should be performed.

PWM output controls LED brightness, while sinusoidal modulation creates the breathing effect.

The Arduino transmits sensor readings and system information to the computer using USB serial communication.

A Python application receives this information through PySerial and visualizes the measurements using Pygame.

## Dashboard Features

The Python interface includes:

* Animated 3D orientation visualization
* Real-time pitch and roll values
* Gyroscope angular velocity
* Four virtual LED indicators
* Brightness percentage meter
* Lighting mode status
* Gesture notifications
* Live scrolling motion graph

The dashboard runs at a target of 60 frames per second.

## Technologies Used

**Hardware:** Arduino Mega 2560, MPU-6050, LEDs

**Programming:** C++, Python

**Communication:** I²C, USB Serial

**Libraries:** Wire, Pygame, PySerial

**Concepts:** Embedded systems, motion sensing, PWM, real-time visualization, gesture recognition, sensor data processing

## Future Improvements

* Sensor fusion for more stable 3D orientation tracking
* Additional lighting modes and effects
* Custom gesture recognition
* Wireless communication using Bluetooth
* RGB LED strip integration
* Bidirectional control between the dashboard and Arduino
* Gesture calibration and sensitivity settings

## Project Status

**Functional Prototype — Completed**

The current prototype supports four-LED gesture control, two lighting modes, motion sensing, and live Python visualization.
