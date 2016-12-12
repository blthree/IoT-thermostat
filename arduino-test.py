import serial
from pyduino import *

ser = serial.Serial('COM4', 9600)
while True:
    message = ser.readline().strip().decode()
    print(message)