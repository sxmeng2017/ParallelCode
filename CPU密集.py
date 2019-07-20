"""
CPU密集即程序运行过程中主要消耗CPU的计算资源
"""
import threading
import time


def add():
    sum = 0
    for i in range(10000):
        sum += i
    print("sum", sum)


def mul():
    sum2 = 1
    for i in range(1,1000):
        sum2 *= i
    print("sum2", sum2)

start = time.time()

t1 = threading.Thread(target=add)
t2 = threading.Thread(target=mul)
l = []
l.append(t1)
l.append(t2)
print(time.ctime())
for t in l:
    t.start()
for t in l:
    t.join()
print("cost time %s" % (time.ctime()))
