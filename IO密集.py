"""
IO密集即端口的读取和切换才是程序重点
"""
import threading
import time

def think():
    print("begin to think {}".format(time.ctime()))
    time.sleep(5)
    print("end to think {}".format(time.ctime()))

def rest():
    print("begin to rest {}".format(time.ctime()))
    time.sleep(7)
    print("end to rest {}".format(time.ctime()))


if __name__ == '__main__':
    t1 = threading.Thread(target=think)
    t2 = threading.Thread(target=rest)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("end")