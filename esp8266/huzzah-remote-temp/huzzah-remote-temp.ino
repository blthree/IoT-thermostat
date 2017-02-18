/***************************************************
  Adafruit IO code is from:
  Adafruit MQTT Library ESP8266 Example

  Written by Tony DiCola for Adafruit Industries.
  MIT license, all text above must be included in any redistribution


 ****************************************************/
  #include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into port 5 on the esp
#define ONE_WIRE_BUS 5

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

/************************* WiFi Access Point *********************************/

#define WLAN_SSID       "YOUR WIFI SSID"
#define WLAN_PASS       "YOUR WIFI PASSWORD"

/************************* Adafruit.io Setup *********************************/

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    "PUT USERNAME HERE"
#define AIO_KEY         "PUT AIO KEY HERE"

/*************************LED SETUP*******************************************/
//currently not used, although it is hooked up
#define LEDpin  13
int currentTemp;
/************ Global State (you don't need to change this!) ******************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// or... use WiFiFlientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

/****************************** Feeds ***************************************/

Adafruit_MQTT_Publish bedroomtemp = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/BedroomTemp");
// Setup a feed called 'onoff' for subscribing to changes.
Adafruit_MQTT_Subscribe onoffbutton = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "/feeds/onoff");

/*************************** Sketch Code ************************************/

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();

void setup() {
  sensors.begin();
  
  Serial.begin(115200);
  delay(10);

  Serial.println(F("Adafruit MQTT demo"));
  pinMode(LEDpin, OUTPUT);


  digitalWrite(LEDpin, LOW);
  delay(500);
  digitalWrite(LEDpin, HIGH);
  delay(500);
  digitalWrite(LEDpin, LOW);
  delay(500);
  digitalWrite(LEDpin, HIGH);
  delay(500);
 digitalWrite(LEDpin, LOW);
  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);
  WiFi.begin("Check your knot", "7thheaven");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  // Setup MQTT subscription for onoff feed.
  mqtt.subscribe(&onoffbutton);
}

uint32_t x=0;

void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();

  // this is our 'wait for incoming subscription packets' busy subloop
  // try to spend your time here

  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &onoffbutton) {
      Serial.print(F("Got: "));
      Serial.println((char *)onoffbutton.lastread);
      if (strcmp((char *)onoffbutton.lastread, "ON") == 0) {
        digitalWrite(LEDpin, HIGH); 
        Serial.println(F("its on"));
      }
      if (strcmp((char *)onoffbutton.lastread, "OFF") == 0) {
        digitalWrite(LEDpin, LOW); 
        Serial.println(F("its off"));
      }
    }
  }
  sensors.requestTemperatures();

  currentTemp=sensors.getTempFByIndex(0);
    //Serial.println(currentTemp);
  // Now we can publish stuff!

    Serial.print(F("\nSending bedroomTemp val "));
  Serial.print(currentTemp);
  Serial.print("...");
  if (! bedroomtemp.publish(currentTemp)) {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }

  // ping the server to keep the mqtt connection alive
  // NOT required if you are publishing once every KEEPALIVE seconds
  /*
  if(! mqtt.ping()) {
    mqtt.disconnect();
  }
  */
}

// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}

