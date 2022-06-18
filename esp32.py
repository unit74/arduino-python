import urllib.request
import cv2
import numpy as np
from stack import *

class esp32:
    def __init__(self, url):
        self.url = url
        self.x = 0
        self.y = 0
        self.direction = 0 # 북
        self.log = Stack()
    def go(self):
        urllib.request.urlopen(self.url + "go")
    def left(self):
        urllib.request.urlopen(self.url + "left")
    def right(self):
        urllib.request.urlopen(self.url + "right")
    def back(self):
        urllib.request.urlopen(self.url + "back")
    def goOne(self):
        urllib.request.urlopen(self.url + "goone")
    def leftOne(self):
        urllib.request.urlopen(self.url + "leftone")
        urllib.request.urlopen(self.url + "left")
        urllib.request.urlopen(self.url + "left")
    def rightOne(self):
        urllib.request.urlopen(self.url + "rightone")
        urllib.request.urlopen(self.url + "right")
        urllib.request.urlopen(self.url + "right")
    def backOne(self):
        urllib.request.urlopen(self.url + "backone")
    def north(self):
        if self.direction == 0: # 북
            return (self.x - 1, self.y)
        elif self.direction == 1: # 동
            return (self.x, self.y + 1)
        elif self.direction == 2: # 남
            return (self.x + 1, self.y)
        elif self.direction == 3: # 서
            return (self.x, self.y - 1)
    def east(self):
        if self.direction == 0: # 북
            return (self.x, self.y + 1)
        elif self.direction == 1: # 동
            return (self.x + 1, self.y)
        elif self.direction == 2: # 남
            return (self.x, self.y - 1)
        elif self.direction == 3: # 서
            return (self.x - 1, self.y )
    def south(self):
        if self.direction == 0: # 북
            return (self.x + 1, self.y)
        elif self.direction == 1: # 동
            return (self.x, self.y - 1)
        elif self.direction == 2: # 남
            return (self.x - 1, self.y)
        elif self.direction == 3: # 서
            return (self.x, self.y + 1)
    def west(self):
        if self.direction == 0: # 북
            return (self.x, self.y - 1)
        elif self.direction == 1: # 동
            return (self.x - 1, self.y)
        elif self.direction == 2: # 남
            return (self.x, self.y + 1)
        elif self.direction == 3: # 서
            return (self.x + 1, self.y)
    def westDirection(self):
        if self.direction - 1 == -1:
            return 3
        return self.direction - 1;
    def eastDirection(self):
        if self.direction + 1 == 4:
            return 0
        return self.direction + 1
    def getJPG(self):
        srcRes = urllib.request.urlopen(self.url + "cam-hi.jpg")
        srcnp = np.array(bytearray(srcRes.read()), dtype=np.uint8)
        src = cv2.imdecode(srcnp, -1)
        return src