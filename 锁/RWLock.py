import threading

"""
下面为读优先，算法很简单，读锁的获取给第一个要锁的，其他要锁的不会添加进等待队列，只在读锁分配数量
上自增1
而写锁直接进等待队列，而且显然只能有一个线程运行获取锁的程序
"""
class RWlock1():
    def __init__(self):
        self._lock = threading.Lock()
        self._extra = threading.Lock()
        self.read_num = 0

    def read_acquire(self):
        with self._extra:
            self.read_num += 1
            if self.read_num == 1:
                self._lock.acquire()

    def read_release(self):
        with self._extra:
            self.read_num -= 1
            if self.read_num == 0:
                self._lock.release()

    def write_acquire(self):
        self._lock.acquire()

    def write_release(self):
        self._lock.release()


"""
该方案为读写锁中写优先，使用condition，将获取锁的过程分为了，判断能否获取和获取两部分编写。
然后再判断上进行调整完成读写优先级的限制，读锁只有在写锁没有线程获取，和本身就在等待队列时才能申请
该方法存在的问题在于对于waiter即等待的线程数量上没有锁保护，多个线程运行时可能出现结果错误
"""
class RWlock2():
    def __init__(self):
        self.lock = threading.Lock()
        self.rcond = threading.Condition(self.lock)
        self.wcond = threading.Condition(self.lock)
        self.read_waiter = 0
        self.write_waiter = 0
        self.state = 0
        self.owners = []
        self.write_first = True

    def write_acquire(self, blocking=True):
        me = threading.get_ident()
        with self.lock:
            while not self._write_acquire(me):
                if not blocking:
                    return False
                self.write_waiter += 1
                self.wcond.wait()
                self.write_waiter -= 1
        return True

    def _write_acquire(self, me):
        if self.state == 0 or (self.state < 0 and me in self.owners):
            self.state -= 1
            self.owners.append(me)
            return True
        if self.state > 0 and me in self.owners:
            raise RuntimeError('cannot recursiverly wrlock a rdlocked lock')

    def read_acquire(self, blocking=True):
        me = threading.get_ident()
        with self.lock:
            while not self._read_acquire(me):
                if not blocking:
                    return False
                self.read_waiter += 1
                self.rcond.wait()
                self.read_waiter -= 1
        return True

    def _read_acquire(self, me):
        if self.state < 0:
            return False
        if not self.write_waiter:
            ok = True
        else:
            ok = me in self.owners
        if ok or not self.write_first:
            self.state += 1
            self.owners.append(me)
            return True
        return False

    def unlock(self):
        me = threading.get_ident()
        with self.lock:
            try:
                self.owners.remove(me)
            except ValueError:
                raise RuntimeError('threading was not acquire lock')

            if self.state > 0:
                self.state -= 1
            elif self.state < 0:
                self.state += 1

            if not self.state:
                if self.write_waiter and self.write_first:
                    self.wcond.notify()
                elif self.read_waiter:
                    self.rcond.notify_all()
                elif self.write_waiter:
                    self.wcond.notify()
