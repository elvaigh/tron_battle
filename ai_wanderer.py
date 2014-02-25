"""
Tron Battle AI. Doesn't go into obstacles if it can.
"""

from client import run_ai  # @include(client.py)
from ai_base import AIBase  # @include(ai_base.py)


class AIWanderer(AIBase):
    """Tron Battle AI: Wanderer.

    Uses result of the ``bfs_probe`` and weight coefficients to determine
    the most interesting direction.
    """

    # Configuration
    depth_limit = 20
    distance_love = 100
    obstacle_fear = 100
    space_love = 100

    def __init__(self):
        super(AIWanderer, self).__init__()
        self.add_param('depth_limit', 'l',
                help='Depth of the search.')
        self.add_param('distance_love', 'd',
                help='Relative weight of maximal distance.')
        self.add_param('obstacle_fear', 'o',
                help='Relative weight of distance to closest obstacle.')
        self.add_param('space_love', 's',
                help='Relative weight of amount of space.')

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
    run_ai(AIWanderer)
