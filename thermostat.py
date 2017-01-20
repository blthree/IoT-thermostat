from arduinohandler import *


class Thermostat:
    def __init__(self, a, relaypin=12):
        print("Thermostat is on pin" + relaypin)
        acknowledge(a, relaypin)

    def
