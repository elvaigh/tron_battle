"""
MiniMax algorithm.
"""


class Move(object):
    """Move record."""

    def __init__(self, player_number, is_mine, direction):
        """Move record.

        :param int player_number: Moving player.
        :param bool is_mine: Me or opponent.
        :param str direction: Move direction.
        """
        self.player_number = player_number
        self.is_mine = is_mine
        self.direction = direction

    def __repr__(self):
        return '{}:{}'.format(self.player_number, self.direction)


class State(object):
    """State after several moves."""

    def __init__(self, moves, grid, player2pos, next_player, prev_state=None):
        self.moves = moves
        self.grid = grid
        self.player2pos = player2pos
        self.next_player = next_player
        self.prev_state = prev_state
        self.next_states = []
        self.value = 0

    def __repr__(self):
        return '[{}->{}]'.format(self.moves, self.value)

    @property
    def player_number(self):
        """Number of the player that moved last."""
        return self.moves[-1].player_number

    def add_next_state(self, next_state):
        """Add next state to the state tree."""
        self.next_states.append(next_state)


class MiniMax(object):
    """MiniMax."""

    def __init__(self, grid, player, full_bfs=None):
        """Initialize the algorithm.

        :param TronGrid grid: grid before the move.
        :param Player player: index
        """
        self.grid = grid
        self.my_number = player.number
        self.my_pos = grid.coords2index(player.x1, player.y1)
        if full_bfs is None:
            full_bfs = grid.bfs_probe(self.my_pos)
        self.full_bfs = full_bfs
        self.detect_opponents()
        self.create_init_state()
        self.layers = []

    def find_best_move(self, max_layers=5, max_layer_size=60):
        """Find the best move by analyzing at most max_layers."""
        for i in xrange(max_layers):
            self.compute_next_layer()
            if len(self.layers[-1]) > max_layer_size:
                break
        self.compute_state_values()

        options = sorted((state.value, state) for state in self.layers[0])
        if options:
            return options[-1][0], options[-1][1].moves[-1].direction
        else:
            return -100, None

    def unlink_states(self):
        """Unlink the tree of states so it can be GC'd."""
        for layer in self.layers:
            for state in layer:
                state.prev_state = None
                state.next_states = None

    def detect_opponents(self):
        """Detect the opponents' heads in our pocket.

        Ignore the players that are not in our pocket because we can't really
        interact with them.
        """
        self.opponents = {}
        for i in xrange(4):
            if i == self.my_number: continue
            head = self.grid.head_of(i)
            if head in self.full_bfs.objects:
                self.opponents[i] = self.full_bfs.obj2pos[head]

    def create_init_state(self):
        """Create initial state."""
        player2pos = dict(self.opponents)
        player2pos[self.my_number] = self.my_pos
        self.init_state = State([], self.grid, player2pos, self.my_number)

    def compute_next_layer(self):
        """Compute next layer of the moves."""
        if self.layers:
            prev_layer = self.layers[-1]
            player_number = self.next_player_after(prev_layer[0].player_number)
        else:
            prev_layer = [self.init_state]
            player_number = self.my_number  # our player starts

        new_layer = list(self.compute_layer(prev_layer, player_number))
        self.layers.append(new_layer)

    def next_player_after(self, player_number):
        """Return next player in the moving order."""
        np = (player_number + 1) % 4
        while np != self.my_number and np not in self.opponents:
            np = (np + 1) % 4
        return np

    def compute_layer(self, prev_layer, player_number):
        """Compute and yield the next layer of decision tree."""
        for state in prev_layer:
            cur_pos = state.player2pos[player_number]
            for dir, offset in self.grid.DIRECTIONS.items():
                new_pos = cur_pos + offset
                if state.grid[new_pos] == 0:
                    grid = state.grid.copy()
                    grid[new_pos] = grid.head_of(player_number)
                    grid[cur_pos] = grid.body_of(player_number)
                    move = Move(player_number,
                            player_number == self.my_number, dir)
                    moves = state.moves + [move]
                    player2pos = dict(state.player2pos)
                    player2pos[player_number] = new_pos
                    new_state = State(moves, grid, player2pos,
                            self.next_player_after(player_number), state)
                    state.add_next_state(new_state)
                    yield new_state

    def evaluate_state(self, state):
        """Evaluate the value of the state for us."""

        def player_probe(player_number):
            return state.grid.bfs_probe(state.player2pos[player_number],
                    limit=40).empty_count

        my_volume = player_probe(self.my_number)
        other_volumes = [player_probe(number) for number in self.opponents]

        max_volume = max([my_volume] + other_volumes)
        state.value = (my_volume - max(other_volumes)) * 80.0 / max_volume

    def aggredate_state(self, state):
        """Aggregate the value from the states below this."""
        next_is_me = state.next_player == self.my_number
        if state.next_states:
            if next_is_me:
                state.value = max(ns.value for ns in state.next_states)
            else:
                state.value = min(ns.value for ns in state.next_states)
        else:
            if next_is_me:
                state.value = -100  # dead end
            else:
                state.value = 100 / len(self.opponents)  # kill

    def compute_state_values(self):
        """Compute the values of all states we've calculated."""
        for i, layer in enumerate(reversed(self.layers)):
            for state in layer:
                if i == 0:
                    self.evaluate_state(state)
                else:
                    self.aggredate_state(state)
