"""
Tron Battle player info.
"""


class PlayerInfo(object):

    alive = True

    def __init__(self, number, x0, y0, x1, y1):
        self.number = number
        self.move(x0, y0, x1, y1)

    def move(self, x0, y0, x1, y1):
        if x0 == -1:
            self.alive = False
        else:
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1

    @property
    def head(self):
        return self.x1, self.y1
