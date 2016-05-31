#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi 

import time
import Adafruit_CharLCD as LCD
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

# Raspberry Pi pin configuration:
lcd_rs        = 27 
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 13
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

retry = 0 ##Sets counter for displaying error message
output = ""
cmd = "ip addr show scope global wlan0 | grep inet | cut -d' ' -f6 | cut -d/ -f1"

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

while (retry < 30):
  lcd.clear()
  time.sleep(1)
  p = Popen(cmd, shell=True, stdout=PIPE)
  output = p.communicate()[0]
  ipaddr = output
  if output == "":  
    lcd.message("DISCONNECTED")
    retry = retry + 1
  else:
    lcd.message("CONNECTED" / 'IP %s' % ( ipaddr ) )
    sleep(15)

if (retry > 30):
  lcd.message("ERROR")
  time.sleep(15)
  retry = 0
