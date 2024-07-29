from threading import Thread
from time import sleep


def func(idx):
    for i in range(5):
        print(f"from {'child' if idx >= 0 else 'main'} thread {idx}: {i}")
        sleep(1)


th = Thread(target=func, args=(1111, ))
th.start()

ths = []
for idx in range(5):
    th = Thread(target=func, args=(idx,))
    th.start()
    ths.append(th)

func(-2)


th.join()
for th in ths:
    th.join()
