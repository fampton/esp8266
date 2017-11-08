import disp_word
import gc
import mixpanel
import network
import utime

from ntptime import settime

def main():
  wlan = network.WLAN(network.STA_IF) # create station interface
  wlan.active(True)       # activate the interface
  if not wlan.isconnected():      # check if the station is connected to an AP
      wlan.connect(<ssid>, <wifi-pw>) # connect to an AP
      for _ in range (10):
          if wlan.isconnected():      # check if the station is connected to an AP
              break
          print('.', end='')
          utime.sleep(1)
  settime()
  utc = utime.time()
  pacific = utc - 28800
  year, month, day, _, _, _, _, _ = utime.localtime(pacific)
  datestring = '%d-%d-%02d' %(year,month,day)
  while True:
    today = mixpanel.main(datestring)
    disp_word.say_something('%s' %today)
    utime.sleep(300)
    gc.collect()

if __name__ == '__main__':
  main()
