import sys
from time import sleep
from udmx import uDMX
from soundmanager import SoundManager
from ultrasonic import UltraSonic
from controller import Controller

#initialize all submodules
dx = uDMX()
print("uDMX loaded")
sm = SoundManager()
print("SoundManager loaded")
us = UltraSonic()
print("UltraSonic rangefinder loaded")
ctrl = Controller(dx, sm, us)
print("Scare-controller loaded")

# Waiting fir victims...
try:
    while True:
        ctrl.handle_fear()
        ctrl.kill_non_current_us_stage_threads()
        sys.stdout.flush()
        sleep(0.5)
except KeyboardInterrupt:  # when 'Ctrl+C' is pressed, the program will exit
    pass
