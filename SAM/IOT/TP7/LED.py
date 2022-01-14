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

import RPi.GPIO as GPIO

from libutils.rpi_utils import getmac

# #############################################################################
#
# Global Variables
#
MQTT_SERVER="192.168.0.215"
MQTT_PORT=1883

MQTT_SUB_LED = "1R1/014/LED"

MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""

client      = None
timer_lum   = None
timer_temp  = None
log         = None
__shutdown  = False

led_lum = 13


# #############################################################################
#
# Functions
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
    log.info("[Shutdown] stop timer and MQTT operations ...")
    client.unsubscribe(MQTT_SUB_LED)
    client.disconnect()
    client.loop_stop()
    del client


# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code : %d" % rc)
    if( rc == 0 ):
        client.subscribe(MQTT_SUB_LED)
        log.info("subscribing to topic: %s" % MQTT_SUB_LED)


# The callback for a received message from the server.
def on_message(client, userdata, msg):

    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    #print("Le topic est : ", msg.topic)
    if(msg.topic=="1R1/014/LED"):
        if(payload['status']== "on"):
            GPIO.output(led_lum, GPIO.HIGH)

    if(msg.topic=="1R1/014/LED"):
        if(payload['status']== "off"):
            GPIO.output(led_lum, GPIO.LOW)

    
  



# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    if(mid%100==0):
        log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)

    
def main():

    # Global variables
    global client, timer_lum, timer_temp, log, inter_lum, inter_temp, liste_device, seuil

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_lum, GPIO.OUT)
    
    #
    log.info("\n----------------------------------------\n")
    log.info("Ambient application to manage luminosity")
    log.info("\n----------------------------------------\n")

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
    
  

    while(1):
        pass


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