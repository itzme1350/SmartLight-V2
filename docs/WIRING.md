# 🔌 SmartLight V2 — Hardware Wiring Guide

## Overview

SmartLight V2 uses an Arduino Mega 2560, an MPU-6050 motion sensor, and four LEDs to create a gesture-controlled lighting system.

## Components

| Component         | Quantity  |
| ----------------- | --------- |
| Arduino Mega 2560 | 1         |
| MPU-6050          | 1         |
| LEDs              | 4         |
| 220Ω resistors    | 4         |
| Breadboard        | 1         |
| Jumper wires      | As needed |

## MPU-6050 Connections

| MPU-6050 Pin | Arduino Mega 2560 |
| ------------ | ----------------- |
| VCC          | 3.3V              |
| GND          | GND               |
| SDA          | Digital Pin 20    |
| SCL          | Digital Pin 21    |

The MPU-6050 communicates with the Arduino through the I²C protocol.

The sensor uses I²C address `0x68` in the current configuration.

## LED Connections

| LED   | Arduino Pin | Resistor |
| ----- | ----------- | -------- |
| LED 1 | D9          | 220Ω     |
| LED 2 | D10         | 220Ω     |
| LED 3 | D11         | 220Ω     |
| LED 4 | D5          | 220Ω     |

Each LED must have its own current-limiting resistor.

### Individual LED Circuit

```text
Arduino PWM Pin
       |
       |
   220Ω Resistor
       |
       |
   LED Anode (+)
   LED Cathode (-)
       |
       |
      GND
```

## PWM Control

The Arduino Mega 2560 uses PWM to control the brightness of each LED.

The selected pins support PWM:

* D5
* D9
* D10
* D11

PWM values range from `0` to `255`, where `0` represents OFF and `255` represents maximum duty cycle.

## Power and Safety

* Disconnect USB power before modifying connections.
* Use a separate resistor for each LED.
* Verify LED polarity before powering the circuit.
* Keep all grounds connected.
* Verify the sensor breakout's supported supply voltage before using 5V.
* Do not connect LEDs directly to Arduino output pins without current-limiting resistors.

## Communication

The Arduino communicates with the MPU-6050 using I²C and sends processed sensor readings to the Python dashboard through USB serial communication at 115200 baud.

## Troubleshooting

**MPU-6050 not detected:** Check SDA, SCL, VCC, and GND connections.

**LED not illuminating:** Check LED polarity, resistor placement, and the assigned PWM pin.

**Unreadable serial output:** Ensure the Arduino and Python applications use the same baud rate.

**Dashboard not receiving data:** Check the COM port and close Arduino Serial Monitor before launching Python.
