from pyduino import *
import time
import dweepy

mykey ='6SLFOIyn71mSLWlr6JuEZM'
setpointHi = 75
setpointLo = 70
mode = 'heat' # could also be cool

if __name__ == '__main__':

    a = Arduino()
    # if your arduino was running on a serial port other than '/dev/ttyACM0/'
    # declare: a = Arduino(serial_port='/dev/ttyXXXX')

    time.sleep(3)
    # sleep to ensure ample time for computer to make serial connection

    statusPin = 9
    relayPin = 4
    a.set_pin_mode(statusPin, 'O')
    time.sleep(.5)  # need to let the arduino catch up
    a.set_pin_mode(relayPin, 'O')
    # initialize the digital pins as IO

    time.sleep(1)
    # allow time to make connection

    # read state of valuePin, which stores the current state of the button
    buttonState = a.variable_read(98)
    # flash LED to show startup
    for j in range(0, 6):
        if j % 2 == 0:
            a.digital_write(relayPin, 1)
            a.digital_write(statusPin, 1)
        else:
            a.digital_write(relayPin, 0)
            a.digital_write(statusPin, 0)
        time.sleep(.5)


    #  run for 1000 seconds

    for i in range(0, 600):
        #buttonState = a.variable_read(98)  # check valuePin

        #  MOVED THIS TO ARDUINO LEVEL FOR SPEED!!!!!!!!!
        '''if buttonState == '1.00':
            a.digital_write(relayPin, 1)  # turn LED on if valuePin is 1
        else:
            a.digital_write(relayPin, 0)  # turn LED off otherwise '''
        if buttonState == '1.00':
            print("System is ON")  # turn LED on if valuePin is 1
        else:
            print("System is OFF")  # turn LED off otherwise
        temp = float(a.variable_read(99))
        #print(temp)
        time.sleep(5)
        adweet = dweepy.dweet_for('helpless-joke', {'TEMP': str(temp)}, mykey)
        #print(adweet)

        # thermostat logic
        if mode == "heat":  #if we are in heating mode
            if temp <= setpointLo:  # and the temperature is low
                # then turn on the heater
                a.digital_write(statusPin, 1)
            elif temp >= setpointHi:  # and the temperature is high
                # then turn off the heater
                a.digital_write(statusPin, 0)
        elif mode == "cool":
            if temp <= setpointLo:  # and the temperature is high
                # then turn on the A/C
                a.digital_write(statusPin, 1)
            elif temp >= setpointHi:  # and the temperature is low
                # then turn off the A/C
                a.digital_write(statusPin, 0)
        else:
            debugdweet = dweepy.dweet_for('helpless-joke', {'DEBUG': 'Mode is set incorrectly'}, mykey)
