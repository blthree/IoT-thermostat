### Provides a minimal simulated pyduino-style object that can be used for testing
### when an arduino is not connected

class simulatedArduino():
    # the IO mode and any values of pins are stored in a dict object
    # each pin number entry contains a dict with 2 keys: mode and value
    def __init__(self):
        # create the pin dictionary
        self.pins = {}

    def setpinmode(self, pin_number, mode):
        # add an entry for the pin we want to use
        # set the mode passed by the method call
        # and set value to zero
        self.pins[pin_number] = {'mode': mode, 'value': 0}

    def digital_read(self, pin_number):
        # check to make sure pin is actually set up as an output
        # then return 0 as the value
        assert self.pins[pin_number]['mode'] == 'O'
        return 0

    def digital_write(self, pin_number, value):
        # check to make sure pin is actually set up as an input
        # assign pin value passed by method
        # print a message as a reminder
        assert self.pins[pin_number]['mode'] == 'I'
        self.pins[pin_number]['value'] = value
        print('Assigned value of ' + str(value) + ' to pin ' + str(pin_number))
        return


# method tests
a = simulatedArduino()
a.setpinmode(2, 'O')
print(a.pins)
a.setpinmode(5, 'I')
a.digital_read(2)
a.digital_write(5, 1)
