#!/usr/bin/python3
import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")
import logging
logging.basicConfig(level=logging.WARNING)

import signal
import numpy
import datetime
from mouseDevice import mouseDevice 
from radioServer import radioServerClient 

def newPosition(change, position, range):
    newposition = position + change
    if (newposition>range):
        newposition -= range
    elif (newposition<0):
        newposition = range + position
    return newposition

def calculateVolume(value, range):
    volume = round(value/range*100)
    if(volume<0):
        volume=0
    elif(volume>100):
        volume=100
    return volume

client1 = radioServerClient("localhost", 6600)
client2 = radioServerClient("localhost", 6601)

# Signal handling
mouseDetached = False
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!\n')
    client1.shutdown()
    client2.shutdown()
    if mouseDetached:
        mouse.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# mouse setup
mouse = mouseDevice(1133, 49256)
mouseDetached = True

# Variables for loop
range = 2000
position = 1000
lastsecond = datetime.datetime.now().second

print("Starting loop ...")
while True: 

    velocity = mouse.readLeftRightMovement()/3

    position = newPosition(velocity, position, range)

    volume = calculateVolume(position, range)

    client1.setVolume(volume)
    client2.setVolume(100-volume)

    if(lastsecond != datetime.datetime.now().second):
        print("position: " + str(position))
        print("volume:   " + str(volume))
        lastsecond = datetime.datetime.now().second

client1.shutdown()
client2.shutdown()