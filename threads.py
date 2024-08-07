from threading import Thread
from time import sleep, perf_counter
import keyboard_emu as kbe


def func(idx, status: callable = None):
    while status is None or status() < 300:
        if status is not None:
            value = status()
        else:
            value = None
        print(f"from {'child' if idx >= 0 else 'main'} thread {idx}: {value}")
        sleep(1)

    print(f'thread {idx} finished')


global_status = 211


def my_status():
    global global_status
    return global_status


ths = []
for idx in range(5):
    th = Thread(target=func, args=(idx, my_status))
    th.start()
    ths.append(th)

t0 = perf_counter()
kbe.key_down(kbe.SC_DOWN)

for st in range(10):
    t1 = perf_counter()
    if t1 - t0 > 3.0:
        kbe.key_up(kbe.SC_DOWN)
    sleep(0.5)
    global_status += 10


for th in ths:
    th.join()
