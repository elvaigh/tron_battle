"""
Tron Battle AI. Very simple code that just doesn't go into obstacles if it can.
"""

import argparse

from client import TronClient  # @include(client.py)


class AIWanderer(object):
    """Tron Battle AI: Wanderer.

    Uses result of the ``bfs_probe`` and weight coefficients to determine
    the most interesting direction.
    """

    def __init__(self, config):
        self.depth_limit = config.depth_limit
        self.distance_love = config.distance_love
        self.obstacle_fear = config.obstacle_fear
        self.space_love = config.space_love

    def __call__(self, players_count, my_number, players, grid):
        """Go randomly where there's path."""
        x, y = players[my_number].head
        pos = grid.coords2index(x, y)

        options = {}
        for dir, offset in grid.DIRECTIONS.items():
            new_pos = pos + offset
            if grid[new_pos] != 0: continue
            pr = grid.bfs_probe(new_pos, limit=self.depth_limit)
            weight = pr.max_distance * self.distance_love
            if weight > 0:
                weight += self.space_love * pr.empty_count
                if pr.closest_obstacle_d is not None:
                    weight += self.obstacle_fear * pr.closest_obstacle_d
                options[weight] = dir

        if options:
            return options[max(options)]
        else:
            return '!'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=AIWanderer.__doc__)
    parser.add_argument('--depth-limit', '-l', type=int, default=20,
            metavar='N', help='Depth of the search.')
    parser.add_argument('--distance-love', '-d', type=int, default=100,
            metavar='N', help='Relative weight of maximal distance.')
    parser.add_argument('--obstacle-fear', '-o', type=int, default=100,
            metavar='N',
            help='Relative weight of distance to closest obstacle.')
    parser.add_argument('--space-love', '-s', type=int, default=100,
            metavar='N', help='Relative weight of amount of space.')
    config = parser.parse_args()

    tc = TronClient(AIWanderer(config))
    tc.run()
