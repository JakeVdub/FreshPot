import time
import os
import RPi.GPIO as GPIO
import LCD


shutdown_pin = 6 ##Pin for shutdown button

def main():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(shutdown_pin, GPIO.IN, GPIO.PUD_DOWN)
  
  button_state = GPIO.input(shutdown_pin)

  while True:
    if button_state == GPIO.HIGH:
      os.system("sudo shutdown -h now")
