"""
Tron Battle AI. Tries to cross the field while it can, then wanders.
"""

import argparse

from client import TronClient  # @include(client.py)
from ai_wanderer import AIWanderer  # @include(ai_wanderer.py)


class AICrosser(AIWanderer):
    """Tron Battle AI: Crosser.

    if in the pocket:
        if others there:
            go straight as far as possible
        else:
            wander
    else:
        go straight as far as possible
    """

    OPEN = 0
    POCKET = 1
    LONELY = 2

    def get_phase(self):
        """Return the phase of the game.

        The phases are:
            OPEN - see others and space is >= ``self.pocket_threshold``,
            POCKET - see others ans space is < ``self.pocket_threshold``,
            LONELY - don't see others.
        """
        pr = self.grid.bfs_probe(self.my_pos, limit=50)
        self.full_bfs_probe = pr
        for i in xrange(4):
            if self.grid.head_of(i) in pr.objects:
                if pr.empty_count >= self.pocket_threshold:
                    return self.OPEN
                else:
                    return self.POCKET
        return self.LONELY

    def check_direction(self):
        """Check that ``self.direction`` exists and is viable."""
        if 'direction' not in vars(self):
            return False

        new_pos = self.my_pos + self.grid.DIRECTIONS[self.direction]
        if self.grid[new_pos] != 0:
            return False

        pr = self.grid.bfs_probe(new_pos, limit=self.depth_limit)
        return pr.empty_count > self.full_bfs_probe.empty_count * 0.3

    def choose_direction(self):
        """Look for good straight directions."""
        options = {}
        for dir, offset in self.grid.DIRECTIONS.items():
            pr = self.grid.ray_probe(self.my_pos, offset, self.ray_width)
            weight = pr.max_distance
            weight += pr.closest_obstacle_d * 3
            options[weight] = dir

        self.direction = options[max(options)]

    def go_straight(self):
        """Go straight to the farthest open side."""
        if self.check_direction():
            return self.direction
        else:
            self.choose_direction()
            if self.check_direction():
                return self.direction
            else:
                return self.go_wander()

    def go(self):
        """Act depending on the phase of the game."""
        self.phase = self.get_phase()

        if self.phase in [self.OPEN, self.POCKET]:
            return self.go_straight()
        else:
            return self.go_wander()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=AICrosser.__doc__)
    parser.add_argument('--depth-limit', '-l', type=int, default=20,
            metavar='N', help='Depth of the search for wandering.')
    parser.add_argument('--distance-love', '-d', type=int, default=100,
            metavar='N', help='Relative weight of maximal distance.')
    parser.add_argument('--obstacle-fear', '-o', type=int, default=0,
            metavar='N',
            help='Relative weight of distance to closest obstacle.')
    parser.add_argument('--space-love', '-s', type=int, default=0,
            metavar='N', help='Relative weight of amount of space.')
    parser.add_argument('--ray-width', '-w', type=int, default=4,
            metavar='N', help='Width of the straightor scan.')
    parser.add_argument('--pocket-threshold', '-t', type=int, default=100,
            metavar='N', help='Pocket threshold.')
    config = parser.parse_args()

    tc = TronClient(AICrosser(config))
    tc.run()
