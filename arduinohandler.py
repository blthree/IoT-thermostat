import time

from pyduino import *


# this module will handle all the arduino IO
# Hopefully this will make it easier to handle
# exceptions when the arduino fails to connect
# or other problems

# pass the address of the serial port for the arduino
# returns an arduino object if successful


def connect_to_arduino(comport):
    try:
        a = Arduino(serial_port=comport)
        time.sleep(3)
        # sleep to ensure ample time for computer to make serial connection
    except serial.serialutil.SerialException:
        print("Arduino connection failed!")
        print("Continuing anyway")
        return

    else:
        print("successfully connected to arduino on port " + comport)
        return a


def acknowledge(a, pin):
    # flash LED 3 times to acknowledge something
    # mostly for debugging
    try:
        for j in range(0, 6):
            if j % 2 == 0:
                a.digital_write(pin, 1)
            else:
                a.digital_write(pin, 0)
            time.sleep(.25)
    except AttributeError:
        print("Acknowledgement Failed!")


def start_output_pin(a, pin):
    try:
        a.set_pin_mode(pin, 'O')
        time.sleep(1)
    except AttributeError:
        print("Failed to set pin" + pin + "as an output pin")
    else:
        print("Successfully set pin" + pin + "as an output pin")


def digital_write_handler(a, pin, value):
    try:
        a.digital_write(pin, value)
    except AttributeError:
        print("digital write failed!")

        # def set_thermostat_state(a, ):
