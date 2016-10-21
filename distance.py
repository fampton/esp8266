import time
from machine import Pin, time_pulse_us

trig = Pin(4, Pin.OUT)
echo = Pin(5, Pin.IN, Pin.PULL_UP)

def ping():
  while True:
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    pulse = time_pulse_us(echo, 1)
    print((pulse / 2) / 29)
    time.sleep_ms(800)
