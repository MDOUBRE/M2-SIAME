# #############################################################################
#
# Import zone
#
import errno
import os
import signal
import syslog
import sys

import time

import threading
import json

import random

import logging

# MQTT related imports
import paho.mqtt.client as mqtt

from smbus2 import SMBus

import Adafruit_MCP9808.MCP9808 as MCP9808

import RPi.GPIO as GPIO

'''
# To extend python librayrt search path
_path2add='./libutils'
if (os.path.exists(_path2add) and not os.path.abspath(_path2add) in sys.path):
    sys.path.append(os.path.abspath(_path2add))
# Raspberry Pi related imports
from rpi_utils import *
'''
from libutils.rpi_utils import getCPUtemperature,getmac



# #############################################################################
#
# Global Variables
#
MQTT_SERVER="192.168.0.215"
MQTT_PORT=1883

MQTT_PUB_TEMP = "1R1/014/temperature"
MQTT_PUB_LUM = "1R1/014/luminosity"

MQTT_SUB_TEMP = "1R1/014/temperature/command"
MQTT_SUB_LUM = "1R1/014/luminosity/command"

MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""

bus = SMBus(1)
liste_device = []
inter_lum = 20
inter_temp = 60

val_lum = 0
val_temp = 0

bool_interupt = False

client      = None
timer_lum   = None
timer_temp  = None
log         = None
__shutdown  = False



# #############################################################################
#
# Functions
#

def scan(force=False):
    devices = []
    for addr in range(0x03, 0x77 + 1):
        read = SMBus.read_byte, (addr,), {'force':force}
        write = SMBus.write_byte, (addr, 0), {'force':force}

        for func, args, kwargs in (read, write):
            try:
                with SMBus(1) as bus:
                    data = func(bus, *args, **kwargs)
                    devices.append(addr)
                    break
            except OSError as expt:
                if expt.errno == 16:
                    pass

    return devices

def get_temp(addr):
    sensor = MCP9808.MCP9808(addr, busnum=1)
    sensor.begin()
    temp = sensor.readTempC()
    return str(temp)

def get_lum(addr):
    bus.write_byte_data(addr, 0x08, 0x03)
    time.sleep(0.05)
    val = bus.read_word_data(addr, 0xAC)
    bus.write_byte_data(0x39,0xC0,0x03)
    bus.write_byte_data(0x39,0x86,0x11) 
    return val

#
# Function ctrlc_handler
def ctrlc_handler(signum, frame):
    global __shutdown
    log.info("<CTRL + C> action detected ...");
    __shutdown = True
    # Stop monitoring
    stopMonitoring()


#
# Function stoping the monitoring
def stopMonitoring():
    global client
    global timer_lum
    global timer_temp
    log.info("[Shutdown] stop timer and MQTT operations ...");
    timer_lum.cancel()
    timer_lum.join()
    del timer_lum
    timer_temp.cancel()
    timer_temp.join()
    del timer_temp
    client.unsubscribe(MQTT_SUB_TEMP)
    client.unsubscribe(MQTT_SUB_LUM)
    client.disconnect()
    client.loop_stop()
    del client

#
# threading.timer helper function
def do_every_lum (worker_func, iterations = 0):
    global timer_lum
    global inter_lum
    global bool_interupt
    # launch new timer
    if ( iterations != 1):
        timer_lum = threading.Timer (
                        inter_lum,
                        do_every_lum, [worker_func, 0 if iterations == 0 else iterations-1])
        timer_lum.start()
    # launch worker function
    if(bool_interupt==False):
        worker_func()
    

def do_every_temp (worker_func, iterations = 0):
    global timer_temp
    global inter_temp
    # launch new timer
    if ( iterations != 1):
        timer_temp = threading.Timer (
                        inter_temp,
                        do_every_temp, [worker_func, 0 if iterations == 0 else iterations-1])
        timer_temp.start()
    # launch worker function
    worker_func()


# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code : %d" % rc)
    if( rc == 0 ):
        client.subscribe(MQTT_SUB_LUM);
        log.info("subscribing to topic: %s" % MQTT_SUB_LUM)
        client.subscribe(MQTT_SUB_TEMP);
        log.info("subscribing to topic: %s" % MQTT_SUB_TEMP)



# The callback for a received message from the server.
def on_message(client, userdata, msg):
    global inter_temp
    global inter_lum
    global timer_lum
    global timer_temp
    global bool_interupt

    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    print("Le topic est : ", msg.topic)
    if(msg.topic=="1R1/014/temperature/command"):
        if(payload["dest"]==getmac()):
            if(payload["order"]=="frequency"):
                inter_temp = int(payload["value"])
                #do_every_temp(publishTemp)
                print("L'inter_temp est maintenant de ", inter_temp)
            elif(payload["order"]=="capture"):
                #timer.cancel()
                #timer_temp = threading.Timer (inter_temp, do_every_temp(publishTemp))
                #timer.start()
                do_every_temp(publishTemp, 1)
    
    
    if(msg.topic=="1R1/014/luminosity/command"):
        if(payload["dest"]==getmac()):
            # passer par var globale addr_pub_lum pour choisir la val de quel capteur on pub
            if(payload["order"]=="frequency"):
                inter_lum = int(payload["value"])
                #do_every_lum(publishLum)
                print("L'inter_lum est maintenant de ", inter_lum)
                if(inter_lum<=0):
                    bool_interupt = True
                    #bus.write_byte_data(0x39,0xC0,0x03)
                    #bus.write_byte_data(0x39,0x86,0x11) 
                else:
                    bool_interupt = False
            elif(payload["order"]=="capture"):
                #timer.cancel()
                #timer_lum = threading.Timer (inter_lum, do_every_lum(publishLum))
                #timer.start()
                do_every_lum(publishLum, 1)

# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    if(mid%10==0):
        log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)


# --- neOCampus related functions ---------------------------------------------
# Acquire sensors and publish
def publishLum():
    global liste_device
    addr=0x39
    # passer par var globale addr_pub_lum
    lum = get_lum(addr)

    # generate json payload
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['subID'] = str(hex(addr))
    jsonFrame['value'] = str(lum)
    jsonFrame['value_units'] = 'lux'
    # ... and publish it!
    client.publish(MQTT_PUB_LUM, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)
     


def publishTemp():  
    global liste_device
    for i in range(len(liste_device)):
        addr = liste_device[i]
        if(int(addr)>=24 and int(addr)<=31):            
            temp = get_temp(addr)            
            # generate json payload
            jsonFrame = { }
            jsonFrame['unitID'] = str(getmac())
            jsonFrame['subID'] = str(hex(addr))
            jsonFrame['value'] = str(temp)
            jsonFrame['value_units'] = 'celsius'
            # ... and publish it!
            client.publish(MQTT_PUB_TEMP, json.dumps(jsonFrame), MQTT_QOS)
            print("on publie : ", jsonFrame)

def interruptionTSL(self):
    global bus, bool_interupt    
    print("Interruption")
    if(bool_interupt==True):
        publishLum()
    bus.write_byte_data(0x39,0xC0,0x03)
    bus.write_byte_data(0x39,0x86,0x11) 

# #############################################################################
#
# MAIN
#

def main():

    # Global variables
    global client, timer_lum, timer_temp, log, inter_lum, inter_temp, liste_device

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback = interruptionTSL)

    bus.write_byte_data(0x39,0xC0,0x03)
    bus.write_byte_data(0x39,0x86,0x11)    
    # Threshold Low
    bus.write_byte_data(0x39,0xA2,0x00)
    bus.write_byte_data(0x39,0xA3,0x00)
    # Threshold High
    bus.write_byte_data(0x39,0xA4,0xE8)
    bus.write_byte_data(0x39,0xA5,0x03)

    print("on est la")
    
    #
    log.info("\n###\nSample application to publish RPI's temperature to [%s] and to [%s]\non server %s:%d" % (MQTT_PUB_TEMP,MQTT_PUB_LUM, str(MQTT_SERVER),MQTT_PORT))
    log.info("(note: some randomization added to the temperature)")
    log.info("###")

    # Trap CTRL+C (kill -2)
    signal.signal(signal.SIGINT, ctrlc_handler)

    # MQTT setup
    client = mqtt.Client( clean_session=True, userdata=None )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    if len(MQTT_USER)!=0 and len(MQTT_PASSWD)!=0:
        client.username_pw_set(MQTT_USER,MQTT_PASSWD); # set username / password

    # Start MQTT operations
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.loop_start()

    # Launch Acquisition & publish sensors till shutdown
    liste_device = scan(True)
    #for i in range(len(liste_device)):
    #    liste_device[i] = '{:02X}'.format(liste_device[i])
    print("Devices connectes sur I2C : ", liste_device)

    do_every_lum(publishLum)
    do_every_temp(publishTemp)
    
    #while(1):
    #    pass

    # waiting for all threads to finish
    if( timer_lum is not None ):
        timer_lum.join()
    if( timer_temp is not None ):
        timer_temp.join()
    


# Execution or import
if __name__ == "__main__":

    # Logging setup
    logging.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    log = logging.getLogger()

    print("\n[DBG] DEBUG mode activated ... ")
    log.setLevel(logging.DEBUG)
    #log.setLevel(logging.INFO)

    # Start executing
    main()


# The END - Jim Morrison 1943 - 1971
#sys.exit(0)

