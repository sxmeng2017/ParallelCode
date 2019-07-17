import threading
import time
import random


class ThreadCreate(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        t = random.randint(1, 10)
        time.sleep(t)
        print("现在运行{0},等待时间为{1}".format(self.getName(), t))


if __name__ == '__main__':
    task = []
    for i in range(10):
        thread = ThreadCreate()
        thread.start()
        task.append(thread)
    for tt in task:
        tt.join()
    print("over")