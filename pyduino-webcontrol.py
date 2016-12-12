from flask import Flask, render_template, request, redirect, url_for
from pyduino import *
import time

##############BEGIN PYDUINO CONTROL CODE#######################
a = Arduino()
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')

time.sleep(3)
# sleep to ensure ample time for computer to make serial connection

valuePin = 9
relayPin = 4
a.set_pin_mode(valuePin, 'I')
time.sleep(.5)  # need to let the arduino catch up
a.set_pin_mode(relayPin, 'O')
# initialize the digital pins as IO

time.sleep(1)
# allow time to make connection
# flash LED to show startup
for j in range(0, 6):
    if j % 2 == 0:
        a.digital_write(relayPin, 1)
    else:
        a.digital_write(relayPin, 0)
    time.sleep(.5)

app = Flask(__name__)


# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/', methods=['POST', 'GET'])
def hello_world():
    # variables for template page (templates/index.html)
    author = "Benson"
    readval = 10
    button_lyfe()

    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':
        # if we press the turn on button
        if request.form['submit'] == 'Turn On':
            print('TURN ON')
            a.digital_write(relayPin, 1)

        # if we press the turn off button
        elif request.form['submit'] == 'Turn Off':
            print('TURN OFF')
            a.digital_write(relayPin, 0)
        else:
            pass

    # the default page to display will be our template with our template variables
    return render_template('index.html', author=author, value=a.digital_read(valuePin))


if __name__ == "__main__":
    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run(host='0.0.0.0')


def button_lyfe():
    # read state of valuePin, which stores the current state of the button
    buttonState = a.digital_read(valuePin)

    #  run for 1000 seconds
    buttonState = a.digital_read(valuePin) # check valuePin
    print(buttonState)
    if buttonState == 1:
        a.digital_write(relayPin, 1)  # turn LED on if valuePin is 1
    else:
        a.digital_write(relayPin, 0)  # turn LED off otherwise
    #time.sleep(1)