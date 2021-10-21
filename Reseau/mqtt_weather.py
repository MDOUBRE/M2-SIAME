# Import pour le mqtt
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


#################################################################################
#                                                                               #
#                                                                               #
#                             VARIABLES GLOBALES                                #
#                                                                               #
#                                                                               #
#################################################################################

MQTT_SERVER="192.168.0.215"
MQTT_PORT=1883
# Full MQTT_topic = MQTT_BASE + MQTT_TYPE
MQTT_BASE_TOPIC = "1R1/014"
MQTT_TYPE_TOPIC1 = "meteo"
MQTT_TYPE_TOPIC2 = "temperature"
MQTT_TYPE_TOPIC3 = "humidity"
MQTT_TYPE_TOPIC4 = "luminosity"
MQTT_TYPE_TOPIC5 = "pressure"
MQTT_TYPE_TOPIC6 = "command"


MQTT_PUB_METEO = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC1])
MQTT_PUB_TEMP = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC2])
MQTT_PUB_HUM = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC3])
MQTT_PUB_LUM = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC4])
MQTT_PUB_PRESS = "/".join([MQTT_BASE_TOPIC, MQTT_TYPE_TOPIC5])

# First subscription to same topic (for tests)

MQTT_SUB = MQTT_PUB_METEO
MQTT_SUB1 = MQTT_PUB_TEMP
MQTT_SUB2 = MQTT_PUB_HUM
MQTT_SUB3 = MQTT_PUB_LUM
MQTT_SUB4 = MQTT_PUB_PRESS

#lumCommand
MQTT_SUB5 = "/".join([MQTT_SUB,MQTT_TYPE_TOPIC6])
MQTT_SUB6 = "/".join([MQTT_SUB1,MQTT_TYPE_TOPIC6])
MQTT_SUB7 = "/".join([MQTT_SUB2,MQTT_TYPE_TOPIC6])
MQTT_SUB8 = "/".join([MQTT_SUB3,MQTT_TYPE_TOPIC6])
MQTT_SUB9 = "/".join([MQTT_SUB4,MQTT_TYPE_TOPIC6])
# ... then subscribe to <topic>/command to receive orders
#MQTT_SUB = "/".join([MQTT_PUB, "command"])

MQTT_QOS=0 # (default) no ACK from server
#MQTT_QOS=1 # server will ack every message

MQTT_USER=""
MQTT_PASSWD=""

# Measurement related
# seconds between each measure.
measure_interleave = 5

client      = None
timer       = None
log         = None
__shutdown  = False


#################################################################################
#                                                                               #
#                                                                               #
#                             FUNCTIONS POUR MQTT                               #
#                                                                               #
#                                                                               #
#################################################################################

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
    global timer
    log.info("[Shutdown] stop timer and MQTT operations ...");
    timer.cancel()
    timer.join()
    del timer
    client.unsubscribe(MQTT_SUB)
    client.disconnect()
    client.loop_stop()
    del client

#
# threading.timer helper function
def do_every (interval, worker_func, iterations = 0):
    global timer
    # launch new timer
    if ( iterations != 1):
        timer = threading.Timer (
                        interval,
                        do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1])
        timer.start();
    # launch worker function
    worker_func();

# --- MQTT related functions --------------------------------------------------
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info("Connected with result code : %d" % rc)

    if( rc == 0 ):
        log.info("subscribing to topic: %s" % MQTT_SUB)
        client.subscribe(MQTT_SUB);
        log.info("subscribing to topic: %s" % MQTT_SUB1)
        client.subscribe(MQTT_SUB1);
        log.info("subscribing to topic: %s" % MQTT_SUB2)
        client.subscribe(MQTT_SUB2);
        log.info("subscribing to topic: %s" % MQTT_SUB3)
        client.subscribe(MQTT_SUB3);
        log.info("subscribing to topic: %s" % MQTT_SUB4)
        client.subscribe(MQTT_SUB4);
        log.info("subscribing to topic: %s" % MQTT_SUB5)
        client.subscribe(MQTT_SUB5);
        log.info("subscribing to topic: %s" % MQTT_SUB6)
        client.subscribe(MQTT_SUB6);
        log.info("subscribing to topic: %s" % MQTT_SUB7)
        client.subscribe(MQTT_SUB7);
        log.info("subscribing to topic: %s" % MQTT_SUB8)
        client.subscribe(MQTT_SUB8);
        log.info("subscribing to topic: %s" % MQTT_SUB9)
        client.subscribe(MQTT_SUB9);

# The callback for a received message from the server.
def on_message(client, userdata, msg):
    ''' process incoming message.
        WARNING: threaded environment! '''
    payload = json.loads(msg.payload.decode('utf-8'))
    log.warning("Received message '" + json.dumps(payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    
    if(msg.topic == "1R1/014/temperature/command"):
        if(payload['order']=='capture'):
            publishTemperature()
    if(msg.topic == "1R1/014/humidity/command"):
        if(payload['order']=='capture'):
            publishHumidity()
    if(msg.topic == "1R1/014/luminosity/command"):
        if(payload['order']=='capture'):
            publishLuminosity()
    if(msg.topic == "1R1/014/pressure/command"):
        if(payload['order']=='capture'):
            publishPressure()
    if(msg.topic == "1R1/014/meteo/command"):
        if(payload['order']=='capture'):
            publishMeteo()
    if(msg.topic == "1R1/014/luminosity"):
        log.warning("Luminosite is %s %s" % (payload['value'],payload['value_units']))
    if(msg.topic == "1R1/014/humidity"):
        log.warning("humidity is %s %s" % (payload['value'],payload['value_units']))
    if(msg.topic == "1R1/014/temperature"):
        log.warning("temperature is %s %s" % (payload['value'],payload['value_units']))
    if(msg.topic == "1R1/014/pressure"):
        log.warning("pressure is %s %s" % (payload['value'],payload['value_units']))
    #if(msg.topic == "1R1/014/meteo"):
    #    log.warning("Luminosite is %s %s" % (payload['value'],payload['value_units']))

    # TO BE CONTINUED
    log.warning("TODO: process incoming message!")


# The callback to tell that the message has been sent (QoS0) or has gone
# through all of the handshake (QoS1 and 2)
def on_publish(client, userdata, mid):
    log.debug("mid: " + str(mid)+ " published!")

def on_subscribe(mosq, obj, mid, granted_qos):
    log.debug("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    log.debug(string)


# --- neOCampus related functions ---------------------------------------------
# Acquire sensors and publish
def publishMeteo():
    file1 = open("illum.txt", "r")
    meteo=file1.readlines()
    file1.close()

    log.debug("RPi meteo = " + meteo)
    # generate json payload
    jsonFrame = { }
    jsonFrame['value'] = json.loads(meteo)
    jsonFrame['value_units'] = 'celsius'
    # ... and publish it!
    client.publish(MQTT_PUB_METEO, json.dumps(jsonFrame), MQTT_QOS)

def publishTemperature():
    file2 = open("temperature.txt", "r")
    temperature=file2.readline()
    file2.close()

    log.debug("RPi temperature = " + temperature)
    # generate json payload
    jsonFrame = { }
    jsonFrame['value'] = json.loads(temperature)
    jsonFrame['value_units'] = 'celsius'
    # ... and publish it!
    client.publish(MQTT_PUB_TEMP, json.dumps(jsonFrame), MQTT_QOS)

def publishHumidity():
    file3 = open("hum.txt", "r")
    humidity=file3.readline()
    file3.close()
    
    print(str(humidity) + "\n")

    log.debug("RPi humidite = " + humidity)
    # generate json payload
    jsonFrame = { }
    jsonFrame['value'] = json.loads(humidity)
    jsonFrame['value_units'] = '%'
    # ... and publish it!
    client.publish(MQTT_PUB_HUM, json.dumps(jsonFrame), MQTT_QOS)

def publishLuminosity():
    file4 = open("illum.txt", "r")
    luminosity=file4.readline()
    file4.close()

    log.warning("Luminosity = " + luminosity)
    # generate json payload
    jsonFrame = { }
    jsonFrame['value'] = json.loads(luminosity)
    jsonFrame['value_units'] = 'lx'
    # ... and publish it!
    client.publish(MQTT_PUB_LUM, json.dumps(jsonFrame), MQTT_QOS)
    log.warning("Le publish est terminé")

def publishPressure():
    file5 = open("air_press.txt", "r")
    pressure=file5.readline()
    file5.close()

    log.debug("RPi pression d'air = " + pressure)
    # generate json payload
    jsonFrame = { }
    jsonFrame['value'] = json.loads(pressure)
    jsonFrame['value_units'] = 'mb'
    # ... and publish it!
    client.publish(MQTT_PUB_PRESS, json.dumps(jsonFrame), MQTT_QOS)


#################################################################################
#                                                                               #
#                                                                               #
#                                    MAIN                                       #
#                                                                               #
#                                                                               #
#################################################################################

def main():

    # Global variables
    global client, timer, log

    #
    log.info("\n###\nSample application to publish RPI's temperature to [%s]\non server %s:%d" % (MQTT_PUB_LUM,str(MQTT_SERVER),MQTT_PORT))
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
    while True:
        client.loop(timeout=2.0, max_packets=1)


if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s][%(module)s:%(funcName)s:%(lineno)d][%(levelname)s] %(message)s", stream=sys.stdout)
    log = logging.getLogger()

    print("\n[DBG] DEBUG mode activated ... ")
    log.setLevel(logging.DEBUG)
    log.setLevel(logging.INFO)

    # Start executing
    main()