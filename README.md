# IoT-thermostat

As an apartment dweller, a real 'smart' thermostat is out of the question, so I decided to cobble together a home made solution using a esp8266, raspberry pi, arduino nano, and a standard 5V relay to interface with the cheapest-model-money-can-buy 'dumb' thermostat installed in my apartment. The esp8266 uses mqtt to send temperature data from a DS18b20 to the Adafruit.io system. The thermostat temperature is also set on the adafruit IO dashboard. The raspberry pi pulls in the set temperature and environment temperature from adafruit IO, if the actual temperature is outside of a 2 degree window from the set temperature, it sends a command to the arduino which flips the relay controlling the thermostat.

The pyduino sketch gets uploaded to the arduino nano which is connected via USB to a raspberry pi. The arduino sketch is not my work, it goes with the python package of the same name. Essentially allows the arduino to act as a slave device by listening for text commands over the serial port. Just hook up the relay and an optional status LED, load the sketch, and connect to a raspberry pi via usb.

The raspberry pi runs the main script, which sends and receives data from the adafruit io website, as well as issues commands to the arduino. If the raspberry pi fails to connect to the arduino, it loads a simulated arduino object instead, which allows testing of the main script without having to be near the physical thermostat setup.

The esp8266 is an adafruit huzzah, programmed with the arduino IDE as well. Very simple program that just connects to the wifi and starts sending out the temperature to adafruit io via mqtt. 

As far as interfacing with the thermostat itself, there's two wires from the relay up to the thermostat, where they are screwed into the contacts on the going to the heater.
