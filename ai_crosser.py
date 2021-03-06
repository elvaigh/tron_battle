"""
Tron Battle AI. Tries to cross the field while it can, then wanders.
"""

from client import run_ai  # @include(client.py)
from ai_wanderer import AIWanderer  # @include(ai_wanderer.py)


class AICrosser(AIWanderer):
    """Tron Battle AI: Crosser.

    if in the pocket:
        if others there:
            go straight as far as possible
        else:
            fill (uses wanderer AI)
    else:
        go straight as far as possible
    """

    # Wanderer config overrides
    depth_limit = 30
    obstacle_fear = -3
    space_love = 30

    # Crosser config
    ray_width = 6
    pocket_threshold = 100
    claustrophobia = 85

    def __init__(self):
        super(AICrosser, self).__init__()
        self.add_param('claustrophobia', 'c',
                help='Minimum %% of space to keep going straight.')
        self.add_param('pocket_threshold', 't',
                help='Available space to decide that we\'re in a pocket.')
        self.add_param('ray_width', 'w', help='Width of the ray scan.')

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
        self.full_bfs = pr
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
        threshold = self.full_bfs.empty_count * self.claustrophobia / 100.0
        return pr.empty_count > threshold

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
    run_ai(AICrosser)
