import time
import machine

button = machine.Pin(0, machine.Pin.IN)


def measure_pulse():
  pulse = machine.time_pulse_us(button, 0, 3000000)
  print(pulse)


