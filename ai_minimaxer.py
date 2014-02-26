"""
Tron Battle AI using minimax algorithm.
"""

from client import run_ai  # @include(client.py)
from ai_wanderer import AIWanderer  # @include(ai_wanderer.py)
from minimax import MiniMax  # @include(minimax.py)


class AIMiniMaxer(AIWanderer):
    """Tron Battle AI: MiniMaxer.

    if can see others:
        use minimax
    else:
        fill (users wanderer)
    """

    # Wanderer config overrides
    depth_limit = 30
    obstacle_fear = -3
    space_love = 30

    # MiniMax config
    max_layers = 8
    max_layer_size = 10

    def __init__(self):
        super(AIMiniMaxer, self).__init__()
        self.add_param('max_layers', 'm',
                help='Number of minimax layers.')
        self.add_param('max_layer_size', 'y',
                help='Max number of states in the layer.')

    def can_see_others(self):
        """Return True if we can reach other players."""
        self.full_bfs = self.grid.bfs_probe(self.my_pos)
        for i in xrange(4):
            if self.grid.head_of(i) in self.full_bfs.objects:
                return True
        return False

    def go(self):
        """Act depending if we see others."""
        if self.can_see_others():
            mm = MiniMax(self.grid, self.players[self.my_number],
                    full_bfs=self.full_bfs)
            weight, move = mm.find_best_move(max_layers=self.max_layers,
                    max_layer_size=self.max_layer_size)
            mm.unlink_states()
            if weight > 0:
                return move
        return self.go_wander()


if __name__ == '__main__':
    run_ai(AIMiniMaxer)
