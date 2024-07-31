from queue import Queue

q = Queue(maxsize=5)


for i in range(5):
    q.put(i*10)


qq = list(q.queue)
print(qq)

q.get()
q.put(1000)
qq = list(q.queue)
print(qq)