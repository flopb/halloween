import sys
from time import sleep
from udmx import uDMX
from soundmanager import SoundManager
from ultrasonic import UltraSonic
import threading


class Controller():

    def __init__(self, dx: uDMX, sm: SoundManager, us: UltraSonic):
        self.dx = dx
        self.sm = sm
        self.us = us
        self.ultrasonic_previouse_distance = 300
        self.us_current_stage = 0
        self.threads = {}

    def handle_fear(self):
        self.handle_ultrasonic()

    def handle_ultrasonic(self):
        distance = self.us.getSonar()
        print(str(distance))
        if True or distance < self.ultrasonic_previouse_distance:  # the victim gets closer
            if distance <= 200 and distance > 170:
                self.us_current_stage = 1
                self.us_thread()
            elif distance <= 170 and distance > 120:
                self.us_current_stage = 2
                self.us_thread()
            elif distance <= 120 and distance > 90:
                self.us_current_stage = 3
                self.us_thread()
            elif distance <= 90:
                self.us_current_stage = 4

    def us_thread(self):
        self.kill_non_current_us_stage_threads()
        if self.threads.get(self.us_current_stage) is None:
            self.threads[self.us_current_stage] = threading.Thread(target=self.play_random_psst, args=(), kwargs={})
            self.threads[self.us_current_stage].start()  # Will run a new thread

    def kill_non_current_us_stage_threads(self):
        lock = threading.Lock()
        lock.acquire()
        for thread in self.threads:
            if thread != self.us_current_stage and self.threads.get(thread) is not None:
                self.threads[thread].stop = True
                self.threads[thread] = None


    def play_random_psst(self):
        t = threading.currentThread()
        while not getattr(t, "stop", False):
            self.sm.playFX("fx1")
            print(self.stage, flush=True)
            sleep(5)
