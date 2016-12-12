from pyduino import *
import time
import dweepy

mykey ='6SLFOIyn71mSLWlr6JuEZM'
setpointHi = 75
setpointLo = 70
mode = 'heat' # could also be cool
hiReads = 0
lowReads = 0

if __name__ == '__main__':

    a = Arduino()
    # if your arduino was running on a serial port other than '/dev/ttyACM0/'
    # declare: a = Arduino(serial_port='/dev/ttyXXXX')

    time.sleep(3)
    # sleep to ensure ample time for computer to make serial connection

    statusPin = 9
    a.set_pin_mode(statusPin, 'O')
    time.sleep(.5)  # need to let the arduino catch up
    # initialize the digital pins as IO

    time.sleep(1)
    # allow time to make connection

    # flash LED to show startup
    for j in range(0, 6):
        if j % 2 == 0:
            a.digital_write(statusPin, 1)
        else:
            a.digital_write(statusPin, 0)
        time.sleep(.25)


    #  run for 1000 seconds

    for i in range(0, 600):
        temp = float(a.variable_read(99))
        #print(temp)
        time.sleep(4)
        adweet = dweepy.dweet_for('helpless-joke', {'TEMP': str(temp)}, mykey)
        #print(adweet)
        time.sleep(1)
        # thermostat logic
        # require 5 or more reads outside of range before starting

        if temp <= setpointLo:  # and the temperature is low
            lowReads += 1
        elif temp >= setpointHi:  # and the temperature is high
            hiReads += 1

        if mode == 'heat':
            if lowReads >= 5:
                heater = 1
                a.digital_write(statusPin, 1)
                lowReads = 0
                hiReads = 0
                dweepy.dweet_for('helpless-joke', {'HEATSTATUS': heater}, mykey)
            elif hiReads >= 5:
                heater = 0
                a.digital_write(statusPin, 0)
                lowReads = 0
                hiReads = 0
                dweepy.dweet_for('helpless-joke', {'HEATSTATUS': heater}, mykey)
        elif mode == 'cool':
            if lowReads >= 5:
                cooler = 0
                a.digital_write(statusPin, 0)
                lowReads = 0
                hiReads = 0
                dweepy.dweet_for('helpless-joke', {'COOLSTATUS': cooler}, mykey)
            elif hiReads >= 5:
                cooler = 1
                a.digital_write(statusPin, 1)
                lowReads = 0
                hiReads = 0
                dweepy.dweet_for('helpless-joke', {'COOLSTATUS': cooler}, mykey)
        else:
            debugdweet = dweepy.dweet_for('helpless-joke', {'DEBUG': 'Mode is set incorrectly'}, mykey)


