import threading
import time

CM_BITS = 16
MAX_COUNTERMAX = ((1 << CM_BITS) - 1)

class MergeCCM():
    def __init__(self, c=0, cm=0):
        self.num = int((c << CM_BITS) | cm)
    def split(self, num):
        c = (num >> CM_BITS) & MAX_COUNTERMAX
        cm = num & MAX_COUNTERMAX

class SignalTheft(threading.Thread):

