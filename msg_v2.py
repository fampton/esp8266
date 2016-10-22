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

TOPIC = 'x1'
SERVER = "192.168.1.253"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
FONT = {'C': 57, 'P': 115, 'p': 115, 's': 109, 'y': 110, 'U': 62, 'r': 80, 'u': 62, 'a': 119, 'c': 88, 'b': 124, 'e': 121, 'd': 94, 'g': 95, 'f': 113, 'i': 16, 'h': 116, 'j': 14, 'l': 56, 'o': 92, 'n': 84, '1': 6, '0': 63, '3': 79, '2': 91, '5': 109, '4': 102, '7': 7, '6': 125, '9': 111, '8': 127, 't': 120}

#def sub_cb(topic, msg):
#  say_something('123')

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

def convert_text(data):
  mylist = []
  for i in data.decode():
    mylist.append(0)
    mylist.append(FONT[i]) 
  return mylist

def say_something(topic, msg):
  print((topic,msg))
  mymsg = (topic,msg)[1]
  setup()
  reset()
  mylist = convert_text(msg)
  send_data(mydata)
  reset()
  send_data(mylist)

def main(server=SERVER):
  c = MQTTClient(CLIENT_ID, server)
  c.set_callback(say_something)
  c.connect()
  c.subscribe(b"x1")
  print("Connected to %s, subscribed to %s topic" % (server, TOPIC))
 
  try:
      while 1:
          #micropython.mem_info()
          c.wait_msg()
  finally:
      c.disconnect()
