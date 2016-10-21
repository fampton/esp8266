import machine
import time
import ubinascii
from machine import Pin
from umqtt.simple import MQTTClient

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
stb = Pin(0, Pin.OUT)

mydata = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
myworld = [0, 62, 0, 62, 0, 92, 0, 80, 0, 56, 0, 94, 0, 0, 0, 0,]
myhello = [0, 116, 0, 121, 0, 56, 0, 56, 0, 92, 0, 0, 0, 0, 0, 0,]

SERVER = "192.168.1.104"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
FONT = {'C': 57, 'P': 115, 'p': 115, 's': 109, 'y': 110, 'U': 62, 'r': 80, 'u': 62, 'a': 119, 'c': 88, 'b': 124, 'e': 121, 'd': 94, 'g': 95, 'f': 113, 'i': 16, 'h': 116, 'j': 14, 'l': 56, 'o': 92, 'n': 84, '1': 6, '0': 63, '3': 79, '2': 91, '5': 109, '4': 102, '7': 7, '6': 125, '9': 111, '8': 127, 't': 120}
#myword = 'hello'
#mylist = [FONT[x] for x in myword]

def sub_cb(topic, msg):
  say_hello()

def shiftout(value):
  bits = [value >> i & 1 for i in range(7,-1,-1)]
  for i in range(7,-1,-1):
    dio.value(bits[i])
    clk.value(1)
    clk.value(0)

def send_data(data):
  stb.value(0)
  for i in data:
    shiftout(i)
  stb.value(1)

def setup():
  stb.value(0)
  shiftout(0x8f)
  stb.value(1)

def reset():
  stb.value(0)
  shiftout(0x40)
  stb.value(1)
  stb.value(0)
  shiftout(0xc0)
  stb.value(1)

def say_hello():
  setup()
  reset()
  send_data(myhello)
  time.sleep(1)
  reset()
  send_data(myworld)

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
