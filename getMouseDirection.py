#!/usr/bin/python3

import sys
import usb.core
import usb.util
import signal

def signal_handler(sig, frame):
    print("")
    print('\nYou pressed Ctrl+C!')
    # release the device
    usb.util.release_interface(dev, interface)
    # reattach the device to the OS kernel
    dev.attach_kernel_driver(interface)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# decimal vendor and product values
dev = usb.core.find(idVendor=0x046d, idProduct=0xc068)                                         # => device object

# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]

# if the OS kernel already claimed the device, which is most likely true http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
    # tell the kernel to detach
    dev.detach_kernel_driver(interface)
    # claim the device
    usb.util.claim_interface(dev, interface)

collected = 0
attempts = 20
while True: 
    try:
        data = dev.read(endpoint.bEndpointAddress,endpoint.wMaxPacketSize)
        
        if collected >= attempts:
            collected = 0
            print("")
        
        velocity = int(data[2])
        if (data[3] == 255):
            velocity = (velocity-256)
            sys.stdout.write("L(" + str(velocity).ljust(3) + ") ")
        else:
            sys.stdout.write("R(" + str(velocity).ljust(3) + ") ")
        
        collected += 1
    except usb.core.USBError as e:
        data = None
        if e.args == ('Operation timed out',):
            continue

















"""if (data[3] == 255):
    print("Moving left (Velocity: " + str(data[2]) + ")")
else:
    print("Moving right (Velocity: " + str(data[2]) + ")")
print(str(data))
print("---") """

#collected < attempts :