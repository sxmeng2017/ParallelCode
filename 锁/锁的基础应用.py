import time
import threading

global num
num = 100
thread_list = []

def n():
    global num
    temp = num
    time.sleep(0.001)
    num = temp - 1
for i in range(100):
    t = threading.Thread(target=n)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()
print('final: {}'.format(num))