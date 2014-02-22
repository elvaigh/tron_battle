"""
Tron Battle player info.
"""


class PlayerInfo(object):

    def __init__(self, number):
        self.number = number
        self.is_alive = True

    def move(self, x0, y0, x1, y1):
        if x0 == -1:
            self.is_alive = False
        else:
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1

    @property
    def coords(self):
        if self.is_alive:
            return self.x0, self.y0, self.x1, self.y1
        else:
            return -1, -1, -1, -1

    @property
    def head(self):
        return self.coords[2:]

    @property
    def tail(self):
        return self.coords[:2]
