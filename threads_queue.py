from threading import Thread
from time import sleep, perf_counter
import keyboard_emu as kbe
from queue import Queue

q = Queue()


def func():
    while True:
        position = q.get()
        print(f'get position: {position}')


th = Thread(target=func)
th.start()

for st in range(10):
    sleep(0.5)
    q.put(st)

