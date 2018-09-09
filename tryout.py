# coding: utf-8

# In[1]:


import usb  # This is pyusb
import time
from time import sleep

vid = 0x16c0
pid = 0x05dc

# Find the uDMX interface by vendor and product ID
dev = usb.core.find(idVendor=vid, idProduct=pid)
# This would find the uDMX by bus number and address (aka port)
# dev = usb.core.find(bus=1, address=4)
#
# You could find the uDMX by using the SYMLINK that the udev rule sets up.
# links = glob.glob("/dev/uDMXusb*")
# os.path.realpath(links[0]) # returns something like /dev/bus/usb/001/004
# You can use a regex to pull out the bus (001) and address (004).

if dev is None:
    print("uDMX device was not found")
    exit(0)

#
# It looks like the only way to determine what methods and
# properties are available on a given pyusb object requires looking
# at the source code on github: https://github.com/walac/pyusb/tree/master/usb
#

print("**********uDMX Device")
print("type:", type(dev))
print(dev)

print("**********MANUFACTURER")
print(dev.manufacturer)
if dev.manufacturer != "www.anyma.ch":
    print("Error - expected www.anyma.ch, actual " + dev.manufacturer)

print("**********PRODUCT")
print(dev.product)

dev.set_configuration()
cfg = dev.get_active_configuration()
print("**********CONFIGURATION")
print("type:", type(cfg))
print(cfg)

intf = cfg[0, 0]
print("**********INTERFACE")
print("type:", type(intf))
print(intf)

ep = usb.util.find_descriptor(intf,
                              # match the first OUT endpoint
                              custom_match= \
                                  lambda e: \
                                      usb.util.endpoint_direction(e.bEndpointAddress) == \
                                      usb.util.ENDPOINT_OUT)
print("**********ENDPOINT")
if ep:
    print(ep)
else:
    print("This device.configuration.interface does not have an OUT endpoint")

status = usb.control.get_status(dev)
print("**********STATUS")
print("Status:", status)

cmd_SetSingleChannel = 1
"""
usb request for cmd_SetSingleChannel:
	bmRequestType:	ignored by device, should be USB_TYPE_VENDOR | USB_RECIP_DEVICE | USB_ENDPOINT_OUT
	bRequest:		cmd_SetSingleChannel
	wValue:			value of channel to set [0 .. 255]
	wIndex:			channel index to set [0 .. 511]
	wLength:		ignored
"""
cmd_SetChannelRange = 2
"""
usb request for cmd_SetChannelRange:
	bmRequestType:	ignored by device, should be USB_TYPE_VENDOR | USB_RECIP_DEVICE | USB_ENDPOINT_OUT
	bRequest:		cmd_SetChannelRange
	wValue:			number of channels to set [1 .. 512-wIndex]
	wIndex:			index of first channel to set [0 .. 511]
	wLength:		length of data, must be >= wValue
"""

# From pyusb (usb.core)
# class Device
#    def ctrl_transfer(self, bmRequestType, bRequest, wValue=0, wIndex=0,
#            data_or_wLength = None, timeout = None):
"""
		Do a control transfer on the endpoint 0.
        This method is used to issue a control transfer over the endpoint 0
        (endpoint 0 is required to always be a control endpoint).
        The parameters bmRequestType, bRequest, wValue and wIndex are the same
        of the USB Standard Control Request format.
        Control requests may or may not have a data payload to write/read.
        In cases which it has, the direction bit of the bmRequestType
        field is used to infer the desired request direction. For
        host to device requests (OUT), data_or_wLength parameter is
        the data payload to send, and it must be a sequence type convertible
        to an array object. In this case, the return value is the number
        of bytes written in the data payload. For device to host requests
        (IN), data_or_wLength is either the wLength parameter of the control
        request specifying the number of bytes to read in data payload, and
        the return value is an array object with data read, or an array
        object which the data will be read to, and the return value is the
        number of bytes read.
"""

# All data tranfers use this request type. This is more for
# the PyUSB package than for the uDMX.
bmRequestType = usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE | usb.util.CTRL_OUT


def setDMX(channel, value):
    channel = channel - 1
    n = dev.ctrl_transfer(bmRequestType, cmd_SetSingleChannel, wValue=value, wIndex=channel, data_or_wLength=1)
    # print("Sent:", channel,"=>",value)


# In[2]:


# Mode
setDMX(1, 0)
# Color
setDMX(2, 40)
# Strobe Speed
setDMX(3, 0)
# Master Dimming
setDMX(4, 255)
# Red Dimming
setDMX(5, 255)
# Green Dimming
setDMX(6, 1)
# Blue Dimming
setDMX(7, 0)
# White Dimming
setDMX(8, 0)

import random
from time import sleep

switches = 0
count = 0
while (count < 10):
    count = count + 1
    while switches < 254:
        switches = switches + 1
        # rand = random.randint(0,255)
        # setDMX(2, rand)
        setDMX(4, switches)
        # sleep(0.001)

    while switches > 0:
        switches = switches - 1
        # rand = random.randint(0,255)
        # setDMX(2, rand)
        setDMX(4, switches)
        # sleep(0.001)

# Mode OFF

setDMX(1, 0)

# In[3]:


# setDMX(1,0)
channel_values = bytearray([0, 0, 0, 255, 255, 10, 100, 0])
channel = 0

n = dev.ctrl_transfer(bmRequestType, cmd_SetChannelRange, wValue=len(channel_values),
                      wIndex=channel, data_or_wLength=channel_values)

# ####

# In[4]:


import pygame
from time import sleep

file = 'assets/sounds/pong.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)

pygame.mixer.music.play(loops=0, start=30)
sleep(10)
# pygame.mixer.music.fadeout(5000)
pygame.mixer.music.stop()

# In[5]:


pygame.mixer.music.stop()

# In[6]:


import pygame
from time import sleep

pygame.init()
pygame.mixer.init()
effect = pygame.mixer.Sound('assets/sounds/fx1.wav')
effect.play(loops=-1, maxtime=0, fade_ms=5000)
effect2 = pygame.mixer.Sound('assets/sounds/fx2.wav')
effect2.play(3)
sleep(3)
effect.stop()
effect2.stop()

# In[7]:


import pygame
import random
from time import sleep

switches = 0
count = 0
pygame.init()
pygame.mixer.init()
effect = pygame.mixer.Sound('assets/sounds/fx1.wav')
effect2 = pygame.mixer.Sound('assets/sounds/fx2.wav')
effect.play(loops=-1, maxtime=0, fade_ms=0)
effect2.play(3)
while (count < 5):
    count = count + 1

    while switches < 254:
        switches = switches + 1
        # rand = random.randint(0,255)
        # setDMX(2, rand)
        setDMX(4, switches)
        sleep(0.001)

    while switches > 0:
        switches = switches - 1
        # rand = random.randint(0,255)
        # setDMX(2, rand)
        setDMX(4, switches)
        sleep(0.00)
effect.stop()
effect2.stop()

# In[18]:


## Ultrasonic range finder
# !/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time
import threading
from IPython.display import clear_output

trigPin = 16
echoPin = 18
MAX_DISTANCE = 220  # define the maximum measured distance
timeOut = MAX_DISTANCE * 60  # calculate timeout according to the maximum measured distance


def pulseIn(pin, level, timeOut):  # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while (GPIO.input(pin) != level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    t0 = time.time()
    while (GPIO.input(pin) == level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    pulseTime = (time.time() - t0) * 1000000
    return pulseTime


def getSonar():  # get the measurement results of ultrasonic module,with unit: cm
    distance = []
    probe_counts = 1
    counter = 0
    previous_distance = None
    while counter < probe_counts:
        counter = counter + 1
        GPIO.output(trigPin, GPIO.HIGH)  # make trigPin send 10us high level
        time.sleep(0.00001)  # 10us
        GPIO.output(trigPin, GPIO.LOW)
        pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read plus time of echoPin
        current_distance = pingTime * 340.0 / 2.0 / 10000.0
        if previous_distance is None:
            previous_distance = current_distance

        if (abs(previous_distance - current_distance) > 5):
            counter = counter - 1
            continue

        distance.append(current_distance)  # the sound speed is 340m/s, and calculate distance
    distance = int(sum(distance) / len(distance))
    return distance

def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)  # numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT)  #
    GPIO.setup(echoPin, GPIO.IN)  #


def loop():
    GPIO.setup(11, GPIO.IN)
    dim_modifier = 255
    current_dim_value = 255
    # Green Dimming
    setDMX(6, 0)
    # Blue Dimming
    setDMX(7, 0)
    # time.sleep(0.1)
    while (True):
        time.sleep(0.001)
        distance = int(getSonar())
        # clear_output()
        # print ("The distance is : %.2f cm"%(distance))
        if distance > 2:
            dim_modifier = int((10 * dim_modifier + 2 * distance) / 11)
            if dim_modifier >= 255:
                dim_modifier = 255
        # if(abs(dim_modifier-current_dim_value) > 10):
        #   continue
        while dim_modifier != current_dim_value:
            if dim_modifier > current_dim_value:
                current_dim_value = current_dim_value + 1
            else:
                current_dim_value = current_dim_value - 1
        setDMX(4, (current_dim_value))


if __name__ == '__main__':  # program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # when 'Ctrl+C' is pressed, the program will exit
        GPIO.cleanup()  # release resource

import threading


def foo():
    print("bar")
    setDMX(4, 0)
    sleep(2)
    print("bar2")
    setDMX(4, 255)


thr = threading.Thread(target=foo, args=(), kwargs={})
thr.start()  # Will run "foo"
