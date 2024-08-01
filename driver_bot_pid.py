import keyboard_emu as kbe
import threading
from queue import Queue
import time
import numpy as np


class DriverBotPID():
    """Бот-водитель для NFS: Shift, версия, работающая по принципу PID-регулятора"""

    def __init__(self):
        self.do_run = True
        self.radius_prev = 0
        self.integral = 0
        self.angle_prev = 0

        self.threads = dict()

        self.wheel_q = Queue(maxsize=1)
        self.speed_q = Queue(maxsize=1)

        self.threads['wheel'] = threading.Thread(target=self.run_wheel)
        self.threads['wheel'].start()

        self.threads['speed'] = threading.Thread(target=self.run_speed)
        self.threads['speed'].start()

    def __del__(self):
        self.do_run = False
        time.sleep(0.1)
        self.threads['wheel'].join()
        self.threads['speed'].join()

    def can_drive(self, can_drive=None):
        if can_drive is not None:
            self.can_drive = can_drive
        return False

    def get_multiplexors(self, get_multiplexors=None) -> dict:
        if get_multiplexors is not None:
            self.get_multiplexors = get_multiplexors
        return {'linear': 1.0, 'integral': 0.02, 'diff': 0.5}

    def run_speed(self):

        while (radius := self.speed_q.get()) is not None:
            if self.can_drive():
                gas = 0.15
                sleep = gas
                if np.absolute(radius-self.radius_prev) > np.absolute(self.radius_prev)*0.10:
                    kbe.key_press(kbe.SC_DOWN, sleep)
                elif np.absolute(radius-self.radius_prev) > np.absolute(self.radius_prev)*0.05:
                    kbe.key_press(kbe.SC_UP, gas*1.5)
                else:
                    kbe.key_press(kbe.SC_UP, gas)

                time.sleep(sleep)
                self.radius_prev = radius

    def run_wheel(self):

        def convert(old):
            old_min, old_max = -110, 110
            new_min, new_max = 0.02, 0.2

            old_range = old_max - old_min
            new_range = new_max - new_min
            converted = ((old - old_min) * new_range / old_range) + new_min

            return converted

        min_ = 0
        max_ = 0

        while (angle := self.wheel_q.get()) is not None:

            if self.can_drive():
                base = 1
                multiplexors = self.get_multiplexors()
                koeff = {
                    'linear': base * multiplexors['linear'],
                    'integral': base * multiplexors['integral'],
                    'diff': base * multiplexors['diff']
                }

                self.integral = koeff['integral'] * angle + self.integral
                differential = koeff['diff'] * (angle - self.angle_prev)
                self.angle_prev = angle
                interval = koeff['linear'] * angle + self.integral + differential

                if interval < min_:
                    min_ = interval
                    print(angle, min_)

                if interval > max_:
                    max_ = interval
                    print(angle, max_)

                if interval > 0:
                    kbe.key_press(kbe.SC_LEFT, convert(interval))
                elif interval < 0:
                    kbe.key_press(kbe.SC_RIGHT, convert(interval))
