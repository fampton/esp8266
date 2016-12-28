#!/usr/bin/env python

from machine import Pin, I2C

def main():
  i2c = I2C(scl=Pin(5), sda=Pin(4))
  import ssd1306
  oled = ssd1306.SSD1306_I2C(128, 64, i2c)
  oled.text('Crampton',0,0)
  oled.show()

if __name__ == '__main__':
  main()
