import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

GPIO.setmode(GPIO.BCM)

TERMS = '#freshpot'  ##Search terms for Twitter stream

## Twitter auth. data
APP_KEY = 'v8X4vmhdxP4ZYN4Ez58twGwtX'
APP_SECRET = 'BF9qqaxXjppxVZBQOMsimPKQeftTgvjlLTemLrPUutWXMSJDbH'
ACCESS_TOKEN = '735129221844979712-0FY6PRW9G4a4JY3ETHjgbCjUGAfnCsd'
ACCESS_TOKEN_SECRET = 'bOeIf4a5AxeSrejiBEScagE3mKNnAoZE8dYBP7uiLuEOW'

power_pin = 18 ## SSR Input pin

GPIO.setup(power_pin, GPIO.OUT) ## Sets it up as an output
GPIO.output(power_pin, False) ## Initially turned off


## Setup callbacks from Twython Streamer
class FreshPotStreamer(TwythonStreamer):
  def on_success(self, data):    
    
    print "POWER ON"
    GPIO.output(power_pin, True) ## Turns on
    time.sleep(360) ## Makes the coffee for 6 minutes, may need adjusting
    print "POWER OFF, FRESH POT!!"
    GPIO.output(power_pin, False) ## Turns coffee maker off
    time.sleep(300) ## Prevents it from being ran again for 5 minutes
  

## Create Streamer
try:
  stream = FreshPotStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
  GPIO.cleanup()

