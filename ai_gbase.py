"""
Tron Battle AI: GBase (base for genetic algorithm).
"""

import sys

from client import run_ai  # @include(client.py)
from ai_base import AIBase  # @include(ai_base.py)


class AIGBase(AIBase):
    """Tron Battle AI: GBase.

    Base class for genetic algorithm AIs
    """

    def __init__(self):
        super(AIGBase, self).__init__()
        self.last_move = None

    def vars_from_probe(self, probe):
        """Extract vars from probe result (see ``calc_vars``)."""
        wall_distance = min(probe.obj2dist.get(-1, 100),
                probe.obj2dist.get(self.grid.body_of(self.my_number), 100))

        head_distance = 100
        body_distance = 100
        for i in set(xrange(4)) - {self.my_number}:
            h = probe.obj2dist.get(self.grid.head_of(i), 100)
            head_distance = min(h, head_distance)
            b = probe.obj2dist.get(self.grid.body_of(i), 100)
            body_distance = min(b, body_distance)

        return (probe.max_distance, probe.closest_obstacle_d,
                probe.empty_count, head_distance, body_distance, wall_distance)

    def vars_from_value(self, value):
        """Extract vars from one filled cell (see ``calc_vars``)."""
        for i in set(xrange(4)) - {self.my_number}:
            if value == self.grid.head_of(i):
                return (0, 0, 0, 0, 100, 100)
            elif value == self.grid.body_of(i):
                return (0, 0, 0, 100, 0, 100)
        return (0, 0, 0, 100, 100, 0)

    def calc_vars(self, direction):
        """Calculate decisions variables for a given direction.

        Performs a ray probe with width = 10 and a bfs probe in the given
        direction and returns a tuple with the following items:

        0. ray_max_distance,
        1. ray_closest_obstacle_d,
        2. ray_empty_count - number of empty points scanned,
        3. ray_head_distance - distance to closest enemy head,
        4. ray_body_distance - distance to closest enemy body,
        5. ray_wall_distance - distance to closest wall (or our body),
        6. bfs_max_distance,
        7. bfs_closest_obstacle_d,
        8. bfs_empty_count - number of empty points scanned,
        9. bfs_head_distance - distance to closest enemy head,
        10. bfs_body_distance - distance to closest enemy body,
        11. bfs_wall_distance - distance to closest wall (or our body).
        """
        offset = self.grid.DIRECTIONS[direction]
        value = self.grid[self.my_pos + offset]
        if value != 0:
            return self.vars_from_value(value) * 2
        else:
            ray = self.grid.ray_probe(self.my_pos, offset, width=10)
            bfs = self.grid.bfs_probe(self.my_pos + offset)
            return self.vars_from_probe(ray) + self.vars_from_probe(bfs)

    def go(self):
        """Wrapper for decision function."""
        directions = ['UP', 'RIGHT', 'DOWN', 'LEFT']

        if self.last_move is None:
            for i, d in enumerate(directions):
                if self.grid[self.my_pos + self.grid.DIRECTIONS[d]] == 0:
                    self.last_move = d
                    return d
        else:
            last_index = directions.index(self.last_move)
            left = directions[(last_index - 1) % 4]
            straight = self.last_move
            right = directions[(last_index + 1) % 4]

            full_bfs = self.grid.bfs_probe(self.my_pos)
            empty_count = full_bfs.empty_count
            heads = 0
            for i in xrange(4):
                if self.grid.head_of(i) in full_bfs.objects:
                    heads += 1

            self.left_vars = self.calc_vars(left)
            self.straight_vars = self.calc_vars(straight)
            self.right_vars = self.calc_vars(right)
            self.dir2vars = {-1: self.left_vars, 0: self.straight_vars,
                    1: self.right_vars}

            decisions = self.decide(empty_count, heads)
            if decisions:
                decision = self.pick_dir(decisions)
                self.last_move = directions[(last_index + decision) % 4]
                return self.last_move
            else:
                return ':('

    def pick_dir(self, dirs):
        """Pick the first or minimal direction from list/set."""
        try:
            return dirs[0]
        except:
            return min(dirs)

    def sort_dirs(self, *weights):
        """Sort directions by dir vars summed with weights (descending)."""
        w_ds = [(sum([v * w for v, w in zip(dv[1], weights)]), dv[0])
                for dv in self.dir2vars.items()]
        return [w_d[1] for w_d in sorted(w_ds, reverse=True)]

    def filter_dirs_lt(self, index, bound):
        """Return directions that have var at index < bound."""
        return {v[0] for v in self.dir2vars.items() if v[1][index] < bound}

    def filter_dirs_gt(self, index, bound):
        """Return directions that have var at index > bound."""
        return {v[0] for v in self.dir2vars.items() if v[1][index] > bound}

    def invert_dirs(self, dirs):
        """Return the dirs not in original set/list."""
        return {-1, 0, 1} - set(dirs)

    def intersect_dirs(self, *dirses):
        """Intersect several sets/lists of dirs.

        The first list in ``dirses`` is used for ordering. If there are no
        lists a set is returned (this is equivalent to ``set.intersection``).
        """
        dirs = set.intersection(*[set(d) for d in dirses])
        lists = filter(lambda d: type(d) == list, dirses)
        if lists:
            dirs = [d for d in lists[0] if d in dirs]
        return dirs

    def decide(self, empty_count, heads):
        """Return the instruction for the next move.

        The instructions are:
            * -1 - turn left,
            * 0 - go straight,
            * 1 - turn right.

        This is an example which implements hugger with enemy avoidance.
        """
        open_dirs = self.filter_dirs_gt(8, empty_count * 0.8)
        if open_dirs:
            return open_dirs
        else:
            close_enemies = self.filter_dirs_lt(3, 2)
            no_close_enemies = self.invert_dirs(close_enemies)
            sorted_by_volume = self.sort_dirs(0, 0, 1, 0, 0, 0, 0, 0, 1)
            sbv_nce = self.intersect_dirs(sorted_by_volume, no_close_enemies)
            if sbv_nce:
                return sbv_nce
            else:
                return sorted_by_volume


if __name__ == '__main__':
    run_ai(AIGBase)
