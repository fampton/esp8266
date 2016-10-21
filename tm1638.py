from machine import Pin

dio = Pin(5, Pin.OUT)
clk = Pin(4, Pin.OUT)
stb = Pin(0, Pin.OUT)

cmd = 0x8f
data = [0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff, 0x00, 0xff]

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
