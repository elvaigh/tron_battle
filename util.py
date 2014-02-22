# Utils for the Tron Battle

from array import array


class TronGrid(object):

    # Coordinates are mapped to indices like this:
    #
    #     idx = x + (y << 6)
    #
    # Then:
    #
    #     x = idx & 63
    #     y = idx >> 6
    #
    # The size of the grid is 30 x 20 with some padding to avoid overflows with
    # reasonably small moves. Initially the grid is filled with 0s for empty
    # cells and -1s for walls.

    def __init__(self):
        self.grid = array('h', ([0] * 30 + [-1] * 34) * 20 + [-1] * 128)

    @staticmethod
    def coords2index(x, y):
        return x + (y << 6)

    @staticmethod
    def index2coords(idx):
        return idx & 63, idx >> 6

    def replace(self, src, dst):
        for i in xrange(len(self.grid)):
            if self.grid[i] == src:
                self.grid[i] = dst

