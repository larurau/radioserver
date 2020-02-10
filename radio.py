#!/usr/bin/python3
import sys
if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")
import signal
import time
import mpd
import numpy
import usb.core
import usb.util
import datetime
import logging
from mouseDevice import mouseDevice 

logging.basicConfig(level=logging.WARNING)

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
       
    except:
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
        logging.info("Initial connect noise server")
        break
                
    except:
        client2.connect("localhost", 6601)
        print("Initial connect noise server failed ...")
        time.sleep(1)

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


last_station_pos=0;             # Position of last station 
noise_track_skip=True;          # Change noise track
station_dist=700;               # Distance between stations
station_width=100;              # with of 100% volume area around stations
vol_slope=0.004                 # Outside of station_with volume decreases with slope
vol_fac=1.0                     # Volume factor - this is what we change when we operate the station dial
vol_filter=numpy.arange(1,5);   # Volume filter array
master_volume=30                # Initial master volume
select_travel=0;                # How far deep is the start/stop button press
select_pressed=0;               # start/stop button pressed?

# Playlist names
playlist_name=["web-radio-local", "web-radio-int", "web-radio-news","volatile"];

print("Start mouse setup ...")

mouse = mouseDevice(1133, 49256)

range = 2000
momentaryPosition = 1000
loudness = 50

lastsecond = datetime.datetime.now().second

print("Finished mouse setup ...")

while True: 

    velocity = mouse.readLeftRightMovement()
    velocity = velocity/3

    momentaryPosition += velocity
    if (momentaryPosition>range):
        momentaryPosition -= range
    elif (momentaryPosition<0):
        momentaryPosition = range + momentaryPosition

    loudness = round(momentaryPosition/range*100)
    if(loudness<0):
        loudness=0
    elif(loudness>100):
        loudness=100

    client1.send_setvol(loudness)
    client1.fetch_setvol(loudness)
    client2.send_setvol(100-loudness)
    client2.fetch_setvol(100-loudness)

    if(lastsecond != datetime.datetime.now().second):
        print("position: " + str(momentaryPosition))
        print("volume:   " + str(loudness))
        lastsecond = datetime.datetime.now().second

client1.close()
client2.close()
client1.disconnect()
client2.disconnect()