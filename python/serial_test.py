import serial
import time

PORT = "COM3"  # Use the same COM port as dashboard.py

with serial.Serial(PORT, 9600, timeout=1) as arduino:
    time.sleep(2)

    print("Testing live MPU-6050 data...")

    while True:
        line = arduino.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        if line:
            print(line)