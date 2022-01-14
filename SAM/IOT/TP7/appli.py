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

MQTT_PUB_TEMP = "1R1/014/temperature/command"
MQTT_PUB_LUM = "1R1/014/luminosity/command"
MQTT_PUB_SHUT = "1R1/014/shutter/command"

MQTT_SUB_TEMP = "1R1/014/temperature"
MQTT_SUB_LUM = "1R1/014/luminosity"
MQTT_SUB_SHUT = "1R1/014/shutter"
MQTT_SUB_PRES = "1R1/014/presence"

MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""

client      = None
timer_lum   = None
timer_temp  = None
log         = None
__shutdown  = False

shut_id = 0
shut_status = 0
shut_order = 0
temperature = 0
luminosity = 0

seuil = 0

bool_action_volet = False
bool_lum_allume = False
bool_presence = False

led_lum = 13


# #############################################################################
#
# Functions
#
def manage():
    global shut_id, shut_status, shut_order, temperature, luminosity, seuil
    global bool_action_volet, bool_lum_allume

    if(luminosity < seuil):
        if(shut_order=="idle"):
            bool_action_volet = False
            if(shut_status!="open"):
                publish_cmd_up()
                bool_action_volet = True
            else:
                GPIO.output(led_lum, GPIO.HIGH)
                bool_lum_allume = True
        
    elif(luminosity>seuil+1000):
        if(shut_order=="idle"):
            bool_action_volet = False
            if(bool_lum_allume == True):
                GPIO.output(led_lum, GPIO.LOW)
                bool_lum_allume = False
            else:
                bool_action_volet = True
                publish_cmd_down()


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
    client.unsubscribe(MQTT_SUB_TEMP)
    client.unsubscribe(MQTT_SUB_LUM)
    client.unsubscribe(MQTT_SUB_SHUT)
    client.unsubscribe(MQTT_SUB_PRES)
    client.disconnect()
    client.loop_stop()
    del client


# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code : %d" % rc)
    if( rc == 0 ):
        client.subscribe(MQTT_SUB_LUM)
        log.info("subscribing to topic: %s" % MQTT_SUB_LUM)
        client.subscribe(MQTT_SUB_TEMP)
        log.info("subscribing to topic: %s" % MQTT_SUB_TEMP)
        client.subscribe(MQTT_SUB_SHUT)
        log.info("subscribing to topic: %s" % MQTT_SUB_SHUT)
        client.subscribe(MQTT_SUB_PRES)
        log.info("subscribing to topic: %s" % MQTT_SUB_PRES)


# The callback for a received message from the server.
def on_message(client, userdata, msg):
    global shut_id, shut_status, shut_order, temperature, luminosity
    global bool_action_volet, bool_lum_allume, bool_presence
    global MQTT_SUB_PRES

    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.debug("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    #print("Le topic est : ", msg.topic)
    if(msg.topic=="1R1/014/temperature"):
        if(payload['unitID']==getmac()):
            temperature = payload['value']
            print(temperature)

    
    if(msg.topic=="1R1/014/luminosity"):
        if(payload['unitID']==getmac()):
            luminosity = int(payload['value'])
            print("luminosité = ", luminosity, " lux")

    if(msg.topic=="1R1/014/shutter"):
        shut_id = str(payload['unitID'])
        shut_status = str(payload['status'])
        shut_order = str(payload['order'])

    if(msg.topic==MQTT_SUB_PRES):
        if(payload['unitID']==getmac()):
            if(payload['value']=="Change" and bool_presence==False):
                print("presence = True")
                bool_presence = True
            elif(payload['value']=="Change" and bool_presence==True):
                bool_presence = False
                GPIO.output(led_lum, GPIO.LOW)

  
    print(luminosity)
    #print(seuil)
    #print(bool_presence)
    if((luminosity<seuil or luminosity>seuil+1000) and bool_presence==True):

        #print("on est la")
        manage()
        if(bool_action_volet == False  and bool_lum_allume==False):
            publish_cmd_capt_lum()



# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    if(mid%100==0):
        log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)


# --- neOCampus related functions ---------------------------------------------
def publish_cmd_up():  
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['dest'] = "all"
    jsonFrame['order'] = "up"
    # ... and publish it!
    client.publish(MQTT_PUB_SHUT, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)

def publish_cmd_down():  
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['dest'] = "all"
    jsonFrame['order'] = "down"
    # ... and publish it!
    client.publish(MQTT_PUB_SHUT, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)


def publish_cmd_status():  
    jsonFrame = { }
    jsonFrame['unitID'] = str(getmac())
    jsonFrame['dest'] = "all"
    jsonFrame['order'] = "status"
    # ... and publish it!
    client.publish(MQTT_PUB_SHUT, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)

def publish_cmd_capt_lum():  
    addr = 0x39    
    jsonFrame = { }
    jsonFrame['dest'] = str(getmac())
    jsonFrame['order'] = "capture"
    # ... and publish it!
    client.publish(MQTT_PUB_LUM, json.dumps(jsonFrame), MQTT_QOS)
    print("on publie : ", jsonFrame)

    
def main():

    # Global variables
    global client, timer_lum, timer_temp, log, inter_lum, inter_temp, liste_device, seuil

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_lum, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(led_lum, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)

    seuil = int(sys.argv[1])
    
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
    
    publish_cmd_status()
    publish_cmd_capt_lum()

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