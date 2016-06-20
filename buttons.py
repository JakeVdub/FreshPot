import time
import os
import RPi.GPIO as GPIO
import LCD

GPIO.setmode(GPIO.BCM) ##Set numbering mode
GPIO.setwarnings(False)


shutdown_pin = 26 ##Pin for shutdown button
refresh_pin = 6 ##Pin for connection-refresh button

GPIO.setup(shutdown_pin, GPIO.IN) ##Sets up shutdown_pin to accept input
GPIO.setup(refresh_pin, GPIO.IN) ##Sets up refresh button pin to accept input

def main():


  ##When refresh button (green) is pressed, call LCD.main() to refresh LCD 
  if GPIO.input(refresh_pin): 
    LCD.Get_IP()
  
  
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

