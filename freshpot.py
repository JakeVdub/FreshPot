import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython
import time
import Adafruit_CharLCD as LCD
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime



## Raspberry Pi pin configuration:
lcd_rs        = 27 
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 13
lcd_backlight = 4

## Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

## Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

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
    
## IP Address
class getIPAddress():
  def get_ip_addr(self)
    cmd = "ip addr show scope global wlan0 | grep inet | cut -d' ' -f6 | cut -d/ -f1"
    output = ""
    ## This loop keeps attempting to find the IP, if after one minute it does not work
    ## then it returns an error output so the screen can display the error message
    while (retry < 30) and (output == ""):
      p = Popen(cmd, shell=True, stdout=PIPE)
      output = p.communicate()[0] 
      if output == "":  
        time.sleep(3)
        retry = retry + 1
    if retry > 30:
      output == "error"
    return output
    msg = output
    
    if msg == "error"
      msg == "DISCONNECTED"
    
    lcd.message(msg)
  
  
ipaddr = getIPAddress()
ipaddr.get_ip_addr()

## Create Streamer
try:
  stream = FreshPotStreamer(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  stream.statuses.filter(track=TERMS)
  

  
  
  
except KeyboardInterrupt:
  GPIO.cleanup()

