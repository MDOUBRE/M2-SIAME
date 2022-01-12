from smbus2 import SMBus
import RPi.GPIO as GPIO

bus = SMBus(1)

def interruptionTSL(self):
    global bus    
    print("Interrupt")
    bus.write_byte_data(0x39,0xC0,0x03)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4, GPIO.FALLING, callback = interruptionTSL)

bus.write_byte_data(0x39,0x80,0x03)
bus.write_byte_data(0x39,0x86,0x11)    
# Threshold Low
bus.write_byte_data(0x39,0xA2,0x00)
bus.write_byte_data(0x39,0xA3,0x00)
# Threshold High
bus.write_byte_data(0x39,0xA4,0xE8)
bus.write_byte_data(0x39,0xA5,0x03)

while(1):
    pass