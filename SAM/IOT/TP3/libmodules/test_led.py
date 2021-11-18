import RPi.GPIO as gpio
import time

ledA = 11
ledB = 12

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(ledA, gpio.OUT)
gpio.setup(ledB, gpio.OUT)

gpio.output(ledA, True)

time.sleep(3)

gpio.output(ledA, False)

gpio.output(ledB, gpio.HIGH)

time.sleep(3)

gpio.output(ledB, gpio.LOW)