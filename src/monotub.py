#!/usr/bin/env python3

import serial
import sys
import os

port = sys.argv[1] if len(sys.argv) > 1 else '/dev/serial/by-id/usb-Arduino_LLC__www.arduino.cc__Genuino_Uno_9543231383735151E130-if00' # monotub.py /dev/ttyACMX para especificar el puerto

if not os.path.exists(port):
    raise Exception(f"Puerto no encontrado: {port}")

ser = serial.Serial(port, 9600)

while True:
    line = ser.readline().decode().strip()
    print(line)