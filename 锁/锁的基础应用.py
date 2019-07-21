import time
import threading

"""
#不加锁
start = time.time()
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
print('final: {},{}'.format(num, str(time.time() - start)))

"""
"""
#加锁
start = time.time()
R = threading.Lock()
global num
num = 100
thread_list = []

def n():
    global num
    R.acquire()
    temp = num
    time.sleep(0.001)
    num = temp - 1
    R.release()
for i in range(100):
    t = threading.Thread(target=n)
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()
print('final: {},{}'.format(num, str(time.time() - start)))

"""

"""
#事件触发
def worker(event):

    print('woking is horrrrrible~~~~~~~~')
    time.sleep(1)

    event.wait()
    print('play!!!!!~~~~~~~~')

def boss(event):
    print('woking is on~~~~~~~~')
    print(event.isSet())
    time.sleep(6)
    event.set()
    print('woking is over~~~~~~~~')
    print(event.isSet())

def main():
    e = threading.Event()
    t1 = threading.Thread(target=boss, args=(e,))
    t1.start()

    for i in range(5):
        t = threading.Thread(target=worker, args=(e,))
        t.start()
main()

"""

