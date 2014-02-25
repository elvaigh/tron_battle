"""
Base class for class-based AIs.
"""


class AIBase(object):
    """Configure from the config object and provide basic __call__."""

    def __init__(self, config):
        for key in vars(config):
            setattr(self, key, getattr(config, key))

    @property
    def my_pos(self):
        """Return the position as an index in the grid."""
        return self.grid.coords2index(self.my_x, self.my_y)

    def go(self):
        """Override to return the direction."""
        return 'LEFT'

    def __call__(self, players_count, my_number, players, grid):
        """Store the basic values."""
        self.players_count = players_count
        self.my_number = my_number
        self.players = players
        self.grid = grid
        self.my_x, self.my_y = players[my_number].head
        return self.go()
