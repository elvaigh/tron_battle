"""
Tron Battle AI. Doesn't go into obstacles if it can.
"""

import argparse

from client import TronClient  # @include(client.py)
from ai_base import AIBase  # @include(ai_base.py)


class AIWanderer(AIBase):
    """Tron Battle AI: Wanderer.

    Uses result of the ``bfs_probe`` and weight coefficients to determine
    the most interesting direction.
    """

    def go_wander(self):
        """Find the direction with least interference."""
        options = {}
        for dir, offset in self.grid.DIRECTIONS.items():
            new_pos = self.my_pos + offset
            if self.grid[new_pos] != 0: continue
            pr = self.grid.bfs_probe(new_pos, limit=self.depth_limit)
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

    go = go_wander


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
