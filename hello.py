import time
from machine import Pin

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
stb = Pin(0, Pin.OUT)

myworld = [0, 62, 0, 62, 0, 92, 0, 80, 0, 56, 0, 94, 0,0,0,0]
myhello = [0, 116, 0, 121, 0, 56, 0, 56, 0, 92, 0, 0, 0, 0, 0, 0,]

FONT = {'C': 57, 'P': 115, 'p': 115, 's': 109, 'y': 110, 'U': 62, 'r': 80, 'u': 62, 'a': 119, 'c': 88, 'b': 124, 'e': 121, 'd': 94, 'g': 95, 'f': 113, 'i': 16, 'h': 116, 'j': 14, 'l': 56, 'o': 92, 'n': 84, '1': 6, '0': 63, '3': 79, '2': 91, '5': 109, '4': 102, '7': 7, '6': 125, '9': 111, '8': 127, 't': 120}
#myword = 'hello'
#mylist = [FONT[x] for x in myword]

def shiftout(value):
    bits = [value >> i & 1 for i in range(7,-1,-1)]
    for i in range(7,-1,-1):
        dio.value(bits[i])
        clk.value(1)
        clk.value(0)

def send_command(cmd, data):
  stb.value(0)
  shiftout(cmd)
  for i in data:
    shiftout(i)
  stb.value(1)

def say_hello():
    send_command(0x8f, mydata)
    send_command(0x8f, myhello)
    time.sleep(1)
    send_command(0x8f, mydata)
    send_command(0x8f, myworld)

