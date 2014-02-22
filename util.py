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

    DIRECTIONS = {
            'UP': -64,
            'DOWN': 64,
            'LEFT': -1,
            'RIGHT': 1
    }

    def __init__(self):
        self.grid = array('h', ([0] * 30 + [-1] * 34) * 20 + [-1] * 128)

    def __str__(self):
        return '\n'.join(
                ('{: >-4d} ' * 30).format(*self.grid[start:start + 30])
                for start in range(0, 64 * 20, 64)
        )

    def __getitem__(self, idx):
        return self.grid[idx]

    def __setitem__(self, idx, value):
        self.grid[idx] = value

    @staticmethod
    def coords2index(x, y):
        return x + (y << 6)

    @staticmethod
    def index2coords(idx):
        return idx & 63, idx >> 6

    def replace(self, src, dst):
        for i, value in enumerate(self.grid):
            if value == src:
                self.grid[i] = dst

    def bfs_fill(self, value, origins, empty=0):
        directions = self.DIRECTIONS.values()
        grid = self.grid

        while origins:
            new_origins = []
            for origin in origins:
                for d in directions:
                    idx = origin + d
                    if grid[idx] == empty:
                        grid[idx] = value
                        new_origins.append(idx)
            origins = new_origins

        # print self
        # print new_origins
        # raw_input()


