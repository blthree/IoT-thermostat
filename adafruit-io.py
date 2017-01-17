# Import library and create instance of REST client.
import time

from Adafruit_IO import Client
from tinydb import TinyDB

from pyduino import *

db = TinyDB('db.json')

# function to check feeds and add to db
# list of feeds to check
tempfeeds = ['BedroomTemp', 'LivingroomTemp']

def checkFeeds():
    for fd in tempfeeds:
        recordTemp = aio.receive(fd)
        recordDate = recordTemp.created_at.split('T')[:-1][0]
        recordTime = recordTemp.created_at.split('T')[1].split('.')[0][:-3]
        feedRecord = {'Location': fd, 'Temperature': recordTemp.value, 'Date': recordDate,
                      'Time': recordTime}
        db.insert(feedRecord)
        # print('Received value: {0}'.format(recordTemp.value))

        if fd == 'BedroomTemp':
            bedroomTemp = recordTemp.value
            print(bedroomTemp)

    # SetTemp = aio.receive('SetTemp')

    # print(db.all())
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
def thermologic(target, bt, lt, cs):
    assert target > 60
    assert target < 90
    if bt >= target + 3:
        return 'OFF'
    elif bt <= target - 3:
        return 'ON'
    else:
        return cs


#################################################
# start adafruit IO client
aio = Client('14737421b335461c9a194995f9b537af')

a = Arduino()
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')

time.sleep(3)
# sleep to ensure ample time for computer to make serial connection

statusPin = 12
relayPin = 4
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
for j in range(0, 6):
    if j % 2 == 0:
        a.digital_write(relayPin, 1)
    else:
        a.digital_write(relayPin, 0)
    time.sleep(.25)
######################################
thermostate = 'OFF'
for x in range(0, 300):
    # check every 5 seconds
    if x % 5 == 0:
        latestTemp = checkFeeds()
        # print(latestTemp)
        # print(thermologic(80, latestTemp, 60, thermostate))
        thermostate = thermologic(70, latestTemp, 60, thermostate)
        print(thermostate)
    time.sleep(1)

