import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin


# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)

# Default MQTT server to connect to
SERVER = "192.168.1.104"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"button"


def main(server=SERVER):
    counter = 0
    c = MQTTClient(CLIENT_ID, server)
    c.connect()
    print("Connected to %s, waiting for button presses" % server)
    while True:
      if button.value() != 0:
        continue
      counter += 1
      print("Button pressed {} times".format(counter))
      c.publish(TOPIC, b"{}".format(counter), qos=1)
      time.sleep_ms(200)

    c.disconnect()
