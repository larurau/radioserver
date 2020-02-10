#!/usr/bin/python3
import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")
import logging
logging.basicConfig(level=logging.WARNING)

import signal
import time
import mpd
import numpy
import usb.core
import usb.util
import datetime
from mouseDevice import mouseDevice 

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

def changeVolume(client, volume):
    client.send_setvol(volume)
    client.fetch_setvol(volume)
    """while True:
        try:
            
            break
                    
        except Exception:
            print("Connection lost while reading line, retry ...")
            time.sleep(1)"""
    
client1 = mpd.MPDClient()           # create client object, music
client2 = mpd.MPDClient()           # create client object, noise

# Connect to music server
while True:
    try:
        status = client1.status()
        client1.send_setvol(50)     #
        client1.fetch_setvol(50)    #
        client1.send_clear()        #
        client1.fetch_clear()       #
        client1.send_add("/")       #
        client1.fetch_add("/")      #
        client1.send_play()
        client1.fetch_play()
        #client2.send_repeat(1)      #
        #client2.fetch_repeat(1)     #
        print("Initial connect music server")
        break
       
    except Exception:
        client1.connect("localhost", 6600)
        logging.info("Initial connect music server failed ...")
        time.sleep(1)

# Connect to noise server
while True:
    try:
        status = client2.status()
        client2.send_setvol(50)
        client2.fetch_setvol(50)
        client2.send_clear()
        client2.fetch_clear()
        client2.send_add("/")
        client2.fetch_add("/")
        client2.send_play()
        client2.fetch_play()
        client2.send_repeat(1)
        client2.fetch_repeat(1)
        print("Initial connect noise server")
        break
                
    except Exception:
        client2.connect("localhost", 6601)
        logging.info("Initial connect noise server failed ...")
        time.sleep(1)

# Signal handling
mouseDetached = False
def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    client1.close()
    client2.close()
    client1.disconnect()
    client2.disconnect()
    if mouseDetached:
        # release the device
        usb.util.release_interface(dev, interface)
        # reattach the device to the OS kernel
        dev.attach_kernel_driver(interface)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Variables for loop
mouse = mouseDevice(1133, 49256)
range = 2000
position = 1000
lastsecond = datetime.datetime.now().second

print("Starting loop ...")
while True: 

    velocity = mouse.readLeftRightMovement()/3

    position = newPosition(velocity, position, range)

    volume = calculateVolume(position, range)

    changeVolume(client1, volume)
    changeVolume(client2, 100-volume)

    if(lastsecond != datetime.datetime.now().second):
        print("position: " + str(position))
        print("volume:   " + str(volume))
        lastsecond = datetime.datetime.now().second

client1.close()
client2.close()
client1.disconnect()
client2.disconnect()