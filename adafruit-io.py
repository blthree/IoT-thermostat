# Import library and create instance of REST client.
from Adafruit_IO import Client
from apscheduler.schedulers.background import BackgroundScheduler
from tinydb import TinyDB, Query
import time
# create scheduler and tinydb instances
sched = BackgroundScheduler()
db = TinyDB('db.json')
lastGoodRecord = {}
# function to check feeds and add to db
# inputs and outputs the last received record
def checkFeeds():
    BedroomTemp = aio.receive('BedroomTemp')
    recordDate = BedroomTemp.created_at.split('T')[:-1][0]
    recordTime = BedroomTemp.created_at.split('T')[1].split('.')[0][:-3]
    BedroomRecord = {'Location': 'Bedroom', 'Temperature': BedroomTemp.value, 'Date': recordDate, 'Time': recordTime}
    db.insert(BedroomRecord)
    print('Received value: {0}'.format(BedroomTemp.value))

    LivingRoomTemp = aio.receive('LivingroomTemp')
    recordDate = LivingRoomTemp.created_at.split('T')[:-1][0]
    recordTime = LivingRoomTemp.created_at.split('T')[1].split('.')[0][:-3]
    LivingRoomRecord = {'Location': 'Living Room', 'Temperature': LivingRoomTemp.value, 'Date': recordDate, 'Time': recordTime}
    # to be replaced with something to check for a duplicate record
    db.insert(LivingRoomRecord)
    print('Received value: {0}'.format(LivingRoomTemp.value))
    #currently broken
    #if BedroomRecord != lastGoodRecord:
     #   db.insert(BedroomRecord)
      #  print('Received value: {0}'.format(BedroomTemp.value))
       # lastGoodRecord = BedroomRecord
    print(db.all())
    return


# start adafruit IO client
aio = Client('14737421b335461c9a194995f9b537af')

# setup scheduler to check every 10 seconds then start it up
sched.add_job(checkFeeds, 'interval', seconds=10)
sched.start()


for x in range(0,100):
    print('x=',x)
    time.sleep(1)

