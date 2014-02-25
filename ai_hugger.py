"""
Tron Battle AI. Finds an obstacle and hugs it.
"""

from client import run_ai  # @include(client.py)
from ai_base import AIBase  # @include(ai_base.py)


class AIHugger(AIBase):
    """Tron Battle AI: Hugger.

    Finds an obstacle and hugs it (or does the opposite is -u is specified).
    """

    # Configuration
    depth_limit = 30
    unhug = False
    threshold = 90

    def __init__(self):
        super(AIHugger, self).__init__()
        self.add_param('depth_limit', 'l', help='Depth of the BFS search.')
        self.add_param('unhug', 'u', type=bool, help='To hug or not to hug?')
        self.add_param('threshold', 't', help='Pocket volume threshold.')

    def go_hug(self):
        """See if there's an obstacle nearby and stay next to it."""
        directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']
        start_dir_no = None

        for i, d in enumerate(directions):
            if self.grid[self.my_pos + self.grid.DIRECTIONS[d]] != 0:
                start_dir_no = i + 1 + (1 if self.unhug else 0)

        if start_dir_no is None:
            return 'LEFT'  # whatever

        full_bfs = self.grid.bfs_probe(self.my_pos, limit=self.depth_limit)

        options = {}
        for i in xrange(start_dir_no, start_dir_no + 4):
            direction = directions[i % 4]
            offset = self.grid.DIRECTIONS[direction]
            new_pos = self.my_pos + offset
            if self.grid[new_pos] != 0: continue
            pr = self.grid.bfs_probe(new_pos, limit=self.depth_limit)
            if pr.empty_count >= full_bfs.empty_count * self.threshold / 100.0:
                return direction
            else:
                options[pr.empty_count] = direction

        if options:
            return options[max(options)]
        else:
            return '!'

    go = go_hug


if __name__ == '__main__':
    run_ai(AIHugger)
