import sys
import time
import threading
import os

# Stores various common constants
class Constants:
    MIN_CLICK_SLEEP_MS = 20 / 1000.
    MAX_CLICK_SLEEP_MS = 35 / 1000.
    THRESHOLD_CONFIDENCE = 0.55

# Utility for backgrounding a function
def background(f, args=[]):
    threading.Thread(target=f, args=args).start()


def console_delay(seconds):
    for i in range(seconds * 2):
        print('.', end='')
        sys.stdout.flush()
        time.sleep(0.5)

# Data type used to describe a rectangle
class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return f"[({self.x},{self.y}) {self.w} | {self.h}]"


def uuid():
    import uuid
    return uuid.uuid1()


def now():
    import time
    return int(round(time.time() * 1000))