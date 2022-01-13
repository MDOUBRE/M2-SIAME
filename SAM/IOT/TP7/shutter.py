#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Shutter module
#
# Thiebolt  aug.19  updated
# Francois  apr.16  initial release
#



# #############################################################################
#
# Import zone
#
import time
import json
import threading
import paho.mqtt.client as mqtt_client
import os
import sys
import logging
import RPi.GPIO as gpio




# #############################################################################
#
# Functions
#



# #############################################################################
#
# Classes
#
class Shutter(object):

    # class attributes
    SHUTTER_POS_CLOSED  = 0
    SHUTTER_POS_OPEN    = 1
    SHUTTER_POS_UNKNOWN = 2

    SHUTTER_ACTION_CLOSE    = 0
    SHUTTER_ACTION_OPEN     = 1
    SHUTTER_ACTION_STOP     = 2
    SHUTTER_ACTION_IDLE     = 3
    SHUTTER_ACTION_UNKNOWN  = 4
    

    SHUTTER_TYPE_WIRED = 0
    SHUTTER_TYPE_WIRELESS = 1

    MQTT_TYPE_TOPIC = "shutter"

    # Min. and max. values for shutter course time
    MIN_COURSE_TIME         = 5
    MAX_COURSE_TIME         = 60

    # attributes
    _status = "between"
    shutterType = SHUTTER_TYPE_WIRED
    courseTime  = 30;       # (seconds) max. time for shutter to get fully open / close

    _backend    = None      # current backends
    _upOutput   = None
    _downOutput = None
    _stopOutput = None

    _curCmd     = "idle"
    _condition  = None      # threading condition
    _thread     = None      # thread to handle shutter's course



    shutter_ID = None

    # on a enlevé mqtt_conf des arguments
    def __init__(self, unitID, ledUp=-1, ledDown=-1, hutterType="wired", courseTime=30, io_backend=None, upOutput=None, downOutput=None, stopOutput=None, shutdown_event=None, *args, **kwargs):
        ''' Initialize object '''
        
        self.courseTime=courseTime
        self._backend=io_backend
        self._upOutput=upOutput
        self._downOutput=downOutput
        self._stopOutput=stopOutput
        self.shutter_ID=unitID
        self.ledUp=ledUp
        self.ledDown=ledDown

        gpio.setmode(gpio.BCM)
        if(self.ledUp != -1):
            gpio.setup(self.ledUp, gpio.OUT)
        if(self.ledDown != -1):
            gpio.setup(self.ledDown, gpio.OUT)

    def getCmdEnCours(self):
        return self._curCmd

    def getStatut(self):
        return self._status

    def getID(self):
        return self.shutter_ID

    def timeout(self,connect):
        init = self._curCmd
        cooldown = self.courseTime
        while ((cooldown > 0) & (self._curCmd == init)):
            cooldown = cooldown - 1
            time.sleep(1)
        if(cooldown == 0):
            if(self._curCmd=='up'):
                self._status='open'
                self._curCmd='idle'
                if(self.ledUp != -1):
                    gpio.output(self.ledUp, gpio.LOW)
            if(self._curCmd=='down'):
                self._status='close'
                self._curCmd='idle'
                if(self.ledDown != -1):
                    gpio.output(self.ledDown, gpio.LOW)
            connect.pubStatus(self)

    def fctUp(self,connect):
        if(self.getStatut()!='open'):
            if(self._curCmd=='down'):
                self._curCmd='idle'
                self._status='between'
                if(self.ledDown != -1):
                    gpio.output(self.ledDown, gpio.LOW)
                connect.pubStatus(self)
            elif(self._curCmd=='idle'):
                self._curCmd='up'
                if(self.ledUp != -1):
                    gpio.output(self.ledUp, gpio.HIGH)
                connect.pubStatus(self)
                myThread = threading.Thread(target=self.timeout, args=[connect])
                myThread.start()
    
    def fctDown(self,connect):
        if(self.getStatut()!='close'):
            if(self._curCmd=='up'):
                self._curCmd='idle'
                self._status='between'
                if(self.ledUp != -1):
                    gpio.output(self.ledUp, gpio.LOW)
                connect.pubStatus(self)
            elif(self._curCmd=='idle'):
                self._curCmd='down'
                if(self.ledDown != -1):
                    gpio.output(self.ledDown, gpio.HIGH)
                connect.pubStatus(self)
                myThread = threading.Thread(target=self.timeout, args=[connect])
                myThread.start()

    def fctStop(self,connect):
        if(self.getStatut()!='stop'):
            if(self._curCmd=='down'):
                self.fctUp(connect)
            elif(self._curCmd=='up'):
                self.fctDown(connect)

    


# #############################################################################
#
# MAIN
#

def main():

    #TODO: implement simple tests of your module
    _______________
    _______________
    _______________
    _______________
    _______________




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

