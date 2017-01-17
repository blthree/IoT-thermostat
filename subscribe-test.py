# Import standard python modules.
import sys
import time

from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY = '14737421b335461c9a194995f9b537af'
ADAFRUIT_IO_USERNAME = 'blthree'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for BedroomTemp changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('BedroomTemp')


def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)


def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()

for x in range(0, 100):
    time.sleep(1)
