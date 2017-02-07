# Import library and create instance of REST client.

import datetime

import Adafruit_IO
from dateutil import tz
from tinydb import TinyDB

from arduinohandler import *

db = TinyDB('db.json')

# function to check feeds and add to db
# list of feeds to check
tempfeeds = ['BedroomTemp']

'''take in date and time as strings and spit out a localized datetime string'''


def makeDateObj(d, t):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fmt = '%Y-%m-%d %H:%M'
    recdt = d + ' ' + t
    dt = datetime.datetime.strptime(recdt, fmt)
    dt = dt.replace(tzinfo=from_zone)
    dt = dt.astimezone(to_zone)
    return dt.strftime(fmt)

def checkFeeds(feedlist):
    for fd in feedlist:
        recordTemp = aio.receive(fd)
        recordDate = recordTemp.created_at.split('T')[:-1][0]
        recordTime = recordTemp.created_at.split('T')[1].split('.')[0][:-3]
        feedRecord = {str(makeDateObj(recordDate, recordTime)): {'Location': fd, 'Temperature': recordTemp.value}}
        db.insert(feedRecord)
        # print('Received value: {0}'.format(recordTemp.value))

        if fd == 'BedroomTemp':
            bedroomTemp = recordTemp.value
            print(bedroomTemp)


    return int(bedroomTemp)


# pass this function on or off and it will change the state
def flipstate(cs):
    if cs == 'ON':
        cs = 'OFF'
    elif cs == 'OFF':
        cs = 'ON'
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

#################################################
# start adafruit IO client
aio = Adafruit_IO.Client('14737421b335461c9a194995f9b537af')

a = connect_to_arduino('/dev/ttyUSB0')

statusPin = 12
relayPin = 4
start_output_pin(a, relayPin)
start_output_pin(a, statusPin)
# allow time to catch up

# flash LED to show startup
acknowledge(a, statusPin)
acknowledge(a, relayPin)
# get starting SetTemp
SetTemp = getSetTemp()

######################################
thermostate = 'OFF'
while True:
    for x in range(0, 60):
        # check every 5 seconds
        if x % 5 == 0:
            latestTemp = checkFeeds(tempfeeds)
            thermostate = thermologic(getSetTemp(), latestTemp, thermostate)
            print(thermostate)
            # apparently relay is on when pulled low
            if thermostate == 'OFF':
                digital_write_handler(a, relayPin, 1)
            elif thermostate == 'ON':
                digital_write_handler(a, relayPin, 0)
            else:
                digital_write_handler(a, relayPin, 1)
            aio.send('onoff', thermostate)
        time.sleep(1)
