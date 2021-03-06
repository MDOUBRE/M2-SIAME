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

import RPi.GPIO as gpio

from libutils.rpi_utils import getmac

bouton1 = 16 
bouton2 = 20

bool_pres = False
bool_interupt = False

MQTT_SERVER="192.168.0.215"
MQTT_PORT=1883
MQTT_PUB = "1R1/014/presence"
MQTT_PUB2 = "1R1/014/luminosity/command"
MQTT_QOS=0
MQTT_USER=""
MQTT_PASSWD=""

client      = None
timer_lum   = None
timer_temp  = None
log         = None
__shutdown  = False


gpio.setmode(gpio.BCM)
gpio.setup(bouton1, gpio.IN, pull_up_down = gpio.PUD_DOWN)
gpio.setup(bouton2, gpio.IN, pull_up_down = gpio.PUD_DOWN)


# Function ctrlc_handler
def ctrlc_handler(signum, frame):
    global __shutdown
    log.info("<CTRL + C> action detected ...");
    __shutdown = True
    # Stop monitoring
    stopMonitoring()

def stopMonitoring():
    global client
    client.disconnect()
    client.loop_stop()
    del client

# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code : %d" % rc)

# The callback for a received message from the server.
def on_message(client, userdata, msg):

    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    if(mid%10==0):
        log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)

def publishVal(string):
    # generate json payload
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['value'] = str(string)
    # ... and publish it!
    client.publish(MQTT_PUB, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)

def publishFreq(int):
    # generate json payload
    jsonFrame = { }
    jsonFrame['dest'] = str(getmac())
    jsonFrame["order"] = "frequency"
    jsonFrame['value'] = int
    # ... and publish it!
    client.publish(MQTT_PUB2, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)


def main():

    # Global variables
    global client, bool_pres, bool_interupt
    #
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

    appui_B1 = 0
    appui_B2 = 0
    while(1):
        if(gpio.input(bouton1)):
            appui_B1 = 1
        elif(appui_B1==1):
            appui_B1 = 0
            if(bool_pres == False):
                bool_pres = True
                print("Presence detect??e")
            else:
                bool_pres = False    
                print("Plus de pr??sence")
            publishVal("Change")

        if(gpio.input(bouton2)):
            appui_B2 = 1
        elif(appui_B2==1):
            appui_B2 = 0
            if(bool_interupt==False):
                bool_interupt = True
                publishFreq(-10)
                print("Passage en mode interupt")
            else:
                bool_interupt = False
                publishFreq(10)
                print("passage en mode fr??quence avec fr??quence de 10")    


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