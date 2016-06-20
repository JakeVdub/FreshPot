## import
import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
import LCD


GPIO.setmode(GPIO.BCM) ##Set numbering mode
GPIO.setwarnings(False)

TERMS = '#freshpot'  ##Search terms for Twitter stream

## Twitter auth. data
APP_KEY = 'v8X4vmhdxP4ZYN4Ez58twGwtX'
APP_SECRET = 'BF9qqaxXjppxVZBQOMsimPKQeftTgvjlLTemLrPUutWXMSJDbH'
ACCESS_TOKEN = '735129221844979712-0FY6PRW9G4a4JY3ETHjgbCjUGAfnCsd'
ACCESS_TOKEN_SECRET = 'bOeIf4a5AxeSrejiBEScagE3mKNnAoZE8dYBP7uiLuEOW'

power_pin = 18 ## SSR Input pin

##shutdown_light = 19 ##Pin for blue light ring
shutdown_pin = 26 ##Pin for shutdown button

##refresh_light = 5 ##Pin for green light ring (refresh connection button)
refresh_pin = 6 ##Pin for connection-refresh button

##blink_rate = 250 ##Controls speed the light rings flash

GPIO.setup(power_pin, GPIO.OUT) ## Sets SSR's pin up as an output
GPIO.output(power_pin, False) ## SSR initially turned off

##GPIO.setup(shutdown_light, GPIO.OUT) ##Sets up blue light ring pin as an output (provides 3v3 power to light)
##GPIO.output(shutdown_light, True) ##Shutdown light ring is on

##GPIO.setup(refresh_light, GPIO.OUT) ##Sets up green light ring pin as an output (Provides 3v3 power to light)
##GPIO.output(refresh_light, True) ##Refresh light ring is on

GPIO.setup(shutdown_pin, GPIO.IN) ##Sets up shutdown_pin to accept input
GPIO.setup(refresh_pin, GPIO.IN) ##Sets up refresh button pin to accept input


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
    time.sleep(300) ## Prevents it from being ran again for 5 minutes
    



## Create Streamer, calls class FreshPotStreamer, also calls LCD.main()
try:
  LCD.main() ##Print IP on LCD
  stream = FreshPotStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET) ## Sets up Twitter Monitor
  stream.statuses.filter(track=TERMS) ## Tells it what keywords to search for
  
  
##When refresh button (green) is pressed, call LCD.main() to refresh LCD and flash light ring
if GPIO.input(refresh_pin): 
  LCD.main()
  
  
##When shutdown button is pushed for 5 seconds Print a message on LCD and then shutdown
if GPIO.input(shutdown_pin):
  pressed_time = time.monotonic()
  while GPIO.input(shutdown_pin):
    ##Placeholder, waiting for button to be released
    pass
  pressed_time = time.monotonic()-pressed_time
  
  if (pressed_time < 5):
    lcd_string("PRESS LONGER")
  
  elif (pressed_time >= 5):
    lcd_string("See Ya!", LCD_LINE_1)
    time.sleep(3000)
    os.system("sudo poweroff")
  
  
except KeyboardInterrupt:
  GPIO.cleanup()

