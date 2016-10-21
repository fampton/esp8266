import machine
import time
import ubinascii
from machine import Pin
from umqtt.simple import MQTTClient

# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
stb = Pin(0, Pin.OUT)

SERVER = "192.168.1.104"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

cmd = 0x8f
data = [0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff]

# Received messages from subscriptions will be delivered to this callback

def shiftout(value):
  bits = [value >> i & 1 for i in range(7,-1,-1)]
  for i in range(7,-1,-1):
    dio.value(bits[i])
    clk.value(1)
    clk.value(0)

def sub_cb(topic, msg):
  stb.value(0)
  shiftout(cmd)
  for i in data:
    shiftout(i)
  stb.value(1)

def main(server=SERVER):
  c = MQTTClient(CLIENT_ID, server)
  c.set_callback(sub_cb)
  c.connect()
  c.subscribe(b"x1")
  while True:
    if True:
      # Blocking wait for message
      c.wait_msg()
    else:
      # Non-blocking wait for message
      c.check_msg()
      # Then need to sleep to avoid 100% CPU usage (in a real
      # app other useful actions would be performed instead)
      time.sleep(1)

  c.disconnect()

if __name__ == "__main__":
    main()
