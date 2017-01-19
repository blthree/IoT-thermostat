# Import library and create instance of REST client.

from Adafruit_IO import Client
from tinydb import TinyDB

from arduinohandler import *

db = TinyDB('db.json')

# function to check feeds and add to db
# list of feeds to check
tempfeeds = ['BedroomTemp']


def checkFeeds(feedlist):
    for fd in feedlist:
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
# function to turn on thermostat, pass the serial cxn and state
'''def updateRelayState(ard, cs):
    if
    a.digital_write(relayPin, 1)'''

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

a = connect_to_arduino('COM3')

statusPin = 12
relayPin = 4

# allow time to catch up

# flash LED to show startup
acknowledge(a, statusPin)
acknowledge(a, relayPin)

######################################
thermostate = 'OFF'
for x in range(0, 300):
    # check every 5 seconds
    if x % 5 == 0:
        latestTemp = checkFeeds(tempfeeds)
        # print(latestTemp)
        # print(thermologic(80, latestTemp, 60, thermostate))
        thermostate = thermologic(70, latestTemp, 60, thermostate)
        print(thermostate)
        if thermostate == 'ON':
            digital_write_handler(a, relayPin, 1)
        elif thermostate == 'OFF':
            digital_write_handler(a, relayPin, 0)
        else:
            digital_write_handler(a, relayPin, 0)
    time.sleep(1)

