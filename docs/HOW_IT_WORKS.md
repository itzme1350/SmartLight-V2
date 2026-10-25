# SmartLight V2 — How It Works

## 1. Project Overview

SmartLight V2 is a gesture-controlled lighting system built using an Arduino Mega 2560, an MPU-6050 motion sensor, and four LEDs.

The system interprets physical movements to control LED brightness, activate or deactivate individual LEDs, and switch between lighting effects.

A Python application provides real-time visualization of sensor measurements, lighting status, and detected gestures.

## 2. System Architecture

SmartLight V2 consists of three primary components:

**Motion Sensing → Embedded Processing → Lighting and Visualization**

```text
         MPU-6050
    Gyroscope + Accelerometer
              |
              | I2C
              |
      Arduino Mega 2560
              |
       Motion Processing
       Gesture Detection
              |
       +------+------+
       |             |
       v             v
    PWM Output    USB Serial
       |          115200 baud
       v             |
    Four LEDs        v
                Python Dashboard
                     |
                  PySerial
                     |
                   Pygame
                     |
              Live Visualization
```

## 3. MPU-6050 Motion Sensing

The MPU-6050 combines two sensors.

### Accelerometer

The accelerometer measures acceleration along three axes:

* X-axis
* Y-axis
* Z-axis

When the sensor is stationary, gravity provides a reference for estimating its orientation.

The Arduino calculates pitch and roll using accelerometer readings and trigonometric functions.

### Gyroscope

The gyroscope measures angular velocity around three axes.

SmartLight V2 currently uses the Z-axis gyroscope measurement to detect rapid twisting movements.

Angular velocity is measured in degrees per second.

## 4. Gesture Recognition

The Arduino processes sensor measurements and compares them against predefined thresholds.

### Pitch-Based Brightness Control

When pitch exceeds +15°, the Arduino increases brightness.

When pitch falls below −15°, the Arduino decreases brightness.

When pitch remains between these thresholds, brightness stays unchanged.

### Roll-Based LED Activation

When roll exceeds +25°, another LED is activated.

When roll falls below −25°, one LED is deactivated.

The sensor must return near its neutral position before another roll gesture is recognized.

This prevents repeated activation while the sensor remains tilted.

### Shake Detection

Shake detection uses the magnitude of the three-axis acceleration vector:

$$
a = \sqrt{a_x^2 + a_y^2 + a_z^2}
$$

When acceleration exceeds the configured threshold of 1.9g, the Arduino toggles the lighting system between ON and OFF.

A cooldown period helps prevent repeated triggering.

### Twist Detection

The Arduino monitors Z-axis angular velocity.

When the value exceeds +170°/s, BREATHING mode activates.

When it falls below −170°/s, NORMAL mode activates.

The system uses a reset threshold and cooldown to reduce repeated detections.

## 5. LED Brightness Control

The Arduino controls four LEDs through PWM-capable digital pins:

| LED   | PWM Pin |
| ----- | ------- |
| LED 1 | 9       |
| LED 2 | 10      |
| LED 3 | 11      |
| LED 4 | 5       |

PWM (Pulse Width Modulation) controls the average power delivered to each LED by varying its duty cycle.

Brightness values range from 0 to 255.

## 6. Lighting Modes

### NORMAL Mode

The Arduino outputs a constant PWM brightness value to each active LED.

The user can increase or decrease brightness using pitch gestures.

### BREATHING Mode

The system uses a cosine-based waveform to create a gradual brightness transition:

$$
B(t) = B_{\max}\frac{1-\cos(2\pi t/T)}{2}
$$

Where:

* \(B(t)\) is the instantaneous PWM brightness.
* \(B_{\max}\) is the user-selected brightness.
* \(t\) is elapsed time.
* \(T\) is the animation period.

The current animation period is approximately three seconds.

## 7. Arduino-to-Python Communication

The Arduino communicates with the computer through USB serial at **115200 baud**.

It transmits:

* Pitch angle
* Roll angle
* Z-axis angular velocity
* Acceleration magnitude
* Brightness percentage
* Number of active LEDs
* Current lighting mode

The Arduino also transmits messages when specific gestures are recognized.

The Python application uses PySerial to read these messages.

## 8. Python Dashboard

The dashboard is developed using Pygame.

It provides several real-time visualizations.

### 3D Orientation Display

A virtual rectangular object rotates according to measured pitch and roll angles.

The display uses mathematical rotations and perspective projection.

### Motion Graph

Pitch and roll measurements are stored in fixed-length buffers and displayed as scrolling line graphs.

### Virtual LED Indicators

Four graphical LED indicators represent the number of active physical LEDs.

### Brightness Meter

A horizontal progress bar shows the current brightness percentage.

### Gesture Notifications

The dashboard displays notifications when shake or twist gestures are detected.

### Lighting Mode Indicator

The interface displays either NORMAL or BREATHING mode.

## 9. Performance

| Parameter                   | Configuration       |
| --------------------------- | ------------------- |
| Microcontroller             | Arduino Mega 2560   |
| Motion Sensor               | MPU-6050            |
| I²C Address                 | 0x68                |
| Serial Baud Rate            | 115200              |
| Sensor Reporting Interval   | Approximately 20 ms |
| Dashboard Target Frame Rate | 60 FPS              |
| Lighting Channels           | 4                   |
| Brightness Range            | 0–255               |
| Lighting Modes              | 2                   |

The Python interface renders independently of the sensor reporting interval.

## 10. Limitations

The current prototype uses accelerometer-derived pitch and roll without full sensor fusion.

Consequently, the orientation visualization may be affected by linear acceleration and vibration.

The dashboard does not currently display an independently estimated yaw angle.

Shake recognition is threshold-based rather than a trained gesture-classification system.

Additionally, dashboard LED indicators are based on reported lighting status and do not perfectly reproduce the physical LEDs' breathing animation.

## 11. Future Development

Potential improvements include:

* Complementary filtering or Kalman filtering for improved orientation estimation
* Three-axis orientation visualization
* Gesture calibration
* Additional lighting animations
* Wireless communication
* RGB lighting integration
* Bidirectional dashboard controls
* More advanced gesture classification

## 12. Conclusion

SmartLight V2 demonstrates the integration of embedded hardware and desktop software into a real-time interactive system.

The project combines I²C communication, accelerometer and gyroscope measurements, gesture recognition, PWM lighting control, serial communication, and graphical visualization.

It provides a foundation for further development in embedded systems, human-computer interaction, and motion-controlled devices.
