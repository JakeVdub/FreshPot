#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi 

import time
import Adafruit_CharLCD as LCD
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime


# Raspberry Pi pin configuration:
lcd_rs        = 27  # Note this might need to be changed to 21 for older revision Pi's.
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

# Print a two line message
lcd.message('Hello\nworld!')

# Wait 5 seconds
time.sleep(5.0)

######## Got this from an example ##################

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

while 1:
        lcd.clear()
        ipaddr = run_cmd(cmd)
        lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
        lcd.message('IP %s' % ( ipaddr ) )
        sleep(2)

