import RPi.GPIO as gpio
import time

led_volet_up = 29
led_volet_down = 31
led_lum = 33
bouton = 36 

bool_allum = 0

gpio.setmode(gpio.BOARD)
#gpio.setmode(gpio.BCM)
gpio.setup(led_volet_up, gpio.OUT)
gpio.setup(led_volet_down, gpio.OUT)
gpio.setup(led_lum, gpio.OUT)
gpio.setup(bouton, gpio.IN, pull_up_down = gpio.PUD_DOWN)

gpio.output(led_volet_up, gpio.HIGH)
time.sleep(1)
gpio.output(led_volet_down, gpio.HIGH)
time.sleep(1)
gpio.output(led_lum, gpio.HIGH)
time.sleep(2)
gpio.output(led_lum, gpio.LOW)
time.sleep(1)
gpio.output(led_volet_down, gpio.LOW)
time.sleep(1)
gpio.output(led_volet_up, gpio.LOW)
time.sleep(1)

appui = 0
while(1):
    if(gpio.input(bouton)):
        appui = 1
    elif(appui==1):
        appui = 0
        if(bool_allum==0):
            gpio.output(led_lum, gpio.HIGH)
            print("1")
            bool_allum = 1
        else:
            gpio.output(led_lum, gpio.LOW)
            print("2")
            bool_allum = 0

