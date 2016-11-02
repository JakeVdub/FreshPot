## import
import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
import LCD
import os



GPIO.setmode(GPIO.BCM) ##Set numbering mode
GPIO.setwarnings(False)

TERMS = '#freshpot'  ##Search terms for Twitter stream

## Twitter auth. data
APP_KEY = 'v8X4vmhdxP4ZYN4Ez58twGwtX'
APP_SECRET = 'BF9qqaxXjppxVZBQOMsimPKQeftTgvjlLTemLrPUutWXMSJDbH'
ACCESS_TOKEN = '735129221844979712-0FY6PRW9G4a4JY3ETHjgbCjUGAfnCsd'
ACCESS_TOKEN_SECRET = 'bOeIf4a5AxeSrejiBEScagE3mKNnAoZE8dYBP7uiLuEOW'

power_pin = 18 ## SSR Input pin

GPIO.setup(power_pin, GPIO.OUT) ## Sets SSR's pin up as an output
GPIO.output(power_pin, False) ## SSR initially turned off

## Sets up Twython for tweeting
app = Twython(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 

## Text for tweet
tweet_text = "Fresh Pot is Ready!"

## Setup callbacks from Twython Streamer
class FreshPotStreamer(TwythonStreamer):
  def on_success(self, data):    
    
    print "POWER ON"
    GPIO.output(power_pin, True) ## Turns on
    time.sleep(360) ## Makes the coffee for 6 minutes, may need adjusting
    print "POWER OFF, FRESH POT!!"
    GPIO.output(power_pin, False) ## Turns coffee maker off
    app.update_status(status = tweet_text) ##sets text for tweet
    print "Tweeted Back At Ya!"
    time.sleep(60) ## Prevents it from being ran again for a minute
    os.system("sudo shutdown -h now") ## Shuts down the pi



## Create Streamer, calls class FreshPotStreamer, also calls LCD.main()
try:
  LCD.main() ##Print IP on LCD
  stream = FreshPotStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) ## Sets up Twitter Monitor
  stream.statuses.filter(track=TERMS) ## Tells it what keywords to search for

  
except KeyboardInterrupt:
  GPIO.cleanup()

