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

    def run_speed(self):

        while (angle := self.speed_q.get()) is not None:
            if self.can_drive():
                gas = 0.20
                brake = 0.22

                # gas = 0.15
                # brake = 0.1

                if angle < 15:
                    kbe.key_press(kbe.SC_UP, gas)
                elif np.absolute(angle - self.angle_prev) > 10:

                    kbe.key_press(kbe.SC_DOWN, brake)
                else:
                    kbe.key_press(kbe.SC_UP, gas)

                self.angle_prev = angle

    def get_multiplexors(self, get_multiplexors=None) -> dict:
        if get_multiplexors is not None:
            self.get_multiplexors = get_multiplexors
        return {'linear': 1, 'integral': 0.003, 'diff': 0.5}

    def run_wheel(self):
        max_ = 85

        def convert(old, _max_=max_):
            old_min, old_max = 0, _max_
            new_min, new_max = 0.05, 0.2

            old_range = old_max - old_min
            new_range = new_max - new_min
            converted = ((old - old_min) * new_range / old_range) + new_min

            return converted

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

                abs_interval = abs(interval)
                print(interval)
                if abs_interval > max_:
                    max_ = abs_interval
                    print(f'new abs_interval: {angle} -> {interval}', )

                kbe.key_press(kbe.SC_LEFT if interval > 0 else kbe.SC_RIGHT, convert(abs_interval, _max_=max_))
