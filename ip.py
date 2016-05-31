#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi 

import time
import Adafruit_CharLCD as LCD
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

class App():

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
  ## Setup retry for counting system
  retry = 0
  
  self.run()
  
  ## Main thread of program, while loop is to get it to check for connectivity again
  ## Given an error
  
  def run(self):
    while (1):
      ipaddr = self.get_ip_addr()
      msg = ipaddr
    
      if msg == "error":
        msg = "DISCONNECTED"
        retry = 0
    
      self.lcd.clear()  
      self.lcd.message(msg)
      time.sleep(15)
      
    
  ## Thread to actually get IP address of wifi network, returns "output"
  def get_ip_addr(self):
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
  
  
