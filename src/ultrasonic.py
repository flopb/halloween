# !/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time

class UltraSonic():

    trigPin = 16
    echoPin = 18
    MAX_DISTANCE = 220  # define the maximum measured distance
    timeOut = MAX_DISTANCE * 60  # calculate timeout according to the maximum measured distance

    def __init__(self):
        self.setup()

    def pulseIn(self, pin, level, timeOut):  # function pulseIn: obtain pulse time of a pin
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

    def getSonar(self):  # get the measurement results of ultrasonic module,with unit: cm
        distance = []
        probe_counts = 1
        counter = 0
        previous_distance = None
        while counter < probe_counts:
            counter = counter + 1
            GPIO.output(self.trigPin, GPIO.HIGH)  # make trigPin send 10us high level
            time.sleep(0.00001)  # 10us
            GPIO.output(self.trigPin, GPIO.LOW)
            pingTime = self.pulseIn(self.echoPin, GPIO.HIGH, self.timeOut)  # read plus time of echoPin
            current_distance = pingTime * 340.0 / 2.0 / 10000.0
            if previous_distance is None:
                previous_distance = current_distance

            if (abs(previous_distance - current_distance) > 2):
                counter = counter - 1
                continue

            distance.append(current_distance)  # the sound speed is 340m/s, and calculate distance
        distance = int(sum(distance) / len(distance))
        return distance

    def setup(self):
        print('Activating ultrasonic sensor...')
        GPIO.setmode(GPIO.BOARD)  # numbers GPIOs by physical location
        GPIO.setup(self.trigPin, GPIO.OUT)  #
        GPIO.setup(self.echoPin, GPIO.IN)  #

    def shutdown(self):
        GPIO.cleanup()
        print('Ultrasonic sensor shut down')

