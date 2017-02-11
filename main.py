# Import library and create instance of REST client.

import datetime
from time import sleep

import Adafruit_IO
from dateutil import tz
from tinydb import TinyDB

from pyduino import *

# arduino pin numbers
statusPin = 12
relayPin = 4
# list of feeds to check
tempfeeds = ['BedroomTemp']


class arduinoExtra(Arduino):
    def acknowledge(self, pin):
        # flash LED 3 times to acknowledge something
        # mostly for debugging
        try:
            for j in range(0, 6):
                if j % 2 == 0:
                    self.digital_write(pin, 1)
                else:
                    self.digital_write(pin, 0)
                sleep(.25)
        except AttributeError:
            print("Acknowledgement Failed!")


class simulatedArduino():
    # the IO mode and any values of pins are stored in a dict object
    # each pin number entry contains a dict with 2 keys: mode and value
    def __init__(self):
        # create the pin dictionary
        self.pins = {}

    def set_pin_mode(self, pin_number, mode):
        # add an entry for the pin we want to use
        # set the mode passed by the method call
        # and set value to zero
        self.pins[pin_number] = {'mode': mode, 'value': 0}

    def digital_read(self, pin_number):
        # check to make sure pin is actually set up as an output
        # then return 0 as the value
        assert self.pins[pin_number]['mode'] == 'I'
        return 0

    def digital_write(self, pin_number, value):
        # check to make sure pin is actually set up as an input
        # assign pin value passed by method
        # print a message as a reminder
        assert self.pins[pin_number]['mode'] == 'O'
        self.pins[pin_number]['value'] = value
        print('Assigned value of ' + str(value) + ' to pin ' + str(pin_number))
        return

    def acknowledge(self, pin):
        # flash LED 3 times to acknowledge something
        # mostly for debugging
        try:
            for j in range(0, 6):
                if j % 2 == 0:
                    self.digital_write(pin, 1)
                else:
                    self.digital_write(pin, 0)
                sleep(.25)
        except AttributeError:
            print("Acknowledgement Failed!")

'''call this on startup, starts database, adafruit IO REST client, and connects to arduino'''
def initialize():
    # start adafruit IO client
    db = TinyDB('db.json')
    aio = Adafruit_IO.Client('14737421b335461c9a194995f9b537af')
    try:
        a = arduinoExtra('COM6')
    except serial.serialutil.SerialException:
        print("Arduino connection failed!")
        print("Simulating Arduino Connection Instead!")
        a = simulatedArduino()

    a.set_pin_mode(relayPin, 'O')
    a.set_pin_mode(statusPin, 'O')
    # flash LED to show startup
    a.acknowledge(statusPin)
    return db, aio, a


'''take in date and time as strings and spit out a localized datetime string'''


def make_date_object(d, t):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = '%Y-%m-%d %H:%M'
    recdt = d + ' ' + t
    dt = datetime.datetime.strptime(recdt, fmt)
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    return dt.strftime(fmt)


# TODO: make this generic for checking and parsing the settemp feed as well
def check_feeds(feedlist):
    for fd in feedlist:
        recordTemp = aio.receive(fd)
        recordDate = recordTemp.created_at.split('T')[:-1][0]
        recordTime = recordTemp.created_at.split('T')[1].split('.')[0][:-3]
        feedRecord = {str(make_date_object(recordDate, recordTime)): {'Location': fd, 'Temperature': recordTemp.value}}
        db.insert(feedRecord)
        # print('Received value: {0}'.format(recordTemp.value))

        if fd == 'BedroomTemp':
            bedroomTemp = recordTemp.value
            print(bedroomTemp)
    return int(bedroomTemp)


'''pass this function on or off and it will change the state
apparently relay is on when pulled low'''


# TODO: rewire relay with pullup
def flipstate(cs):
    if cs == 'OFF':
        a.digital_write(relayPin, 1)
    elif cs == 'ON':
        a.digital_write(relayPin, 0)
    else:
        a.digital_write(relayPin, 1)
    return cs


# function to decide if thermostat should be on/off
# currently uses a simple 6-degree window around the set temp
# returns a state, either on or off
def thermologic(target, bt, cs):
    assert target >= 60
    assert target <= 90
    if bt >= target + 2:
        return 'OFF'
    elif bt <= target - 2:
        return 'ON'
    else:
        return cs


# TODO: roll function into checkfeeds()
def getSetTemp():
    try:
        setpoint = int(aio.receive('SetTemp').value)
    except Adafruit_IO.RequestError:
        print('Request Error!')

    if setpoint not in range(60, 90):
        print('SetTemp is out of range: ' + str(setpoint) + ' allowable range is 60-90F')
        print('Resetting at 70F!')
        setpoint = 70
        aio.send('SetTemp', setpoint)
    print("temp is set at: " + str(setpoint))
    return setpoint


'''main program loop'''
db, aio, a = initialize()
thermostate = 'OFF'
SetTemp = getSetTemp()
while True:
    for x in range(0, 60):
        # check every 10 seconds
        if x % 10 == 0:
            latestTemp = check_feeds(tempfeeds)
            thermostate = thermologic(getSetTemp(), latestTemp, thermostate)
            print(thermostate)
            flipstate(thermostate)
            aio.send('onoff', thermostate)
        sleep(1)