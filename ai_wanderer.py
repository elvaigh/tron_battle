"""
Tron Battle AI. Very simple code that just doesn't go into obstacles if it can.
"""

from client import TronClient  # @include(client.py)


def ai_wanderer(players_count, my_number, players, grid):
    """Go randomly where there's path."""
    x, y = players[my_number].head
    pos = grid.coords2index(x, y)

    options = {}
    for dir, offset in grid.DIRECTIONS.items():
        new_pos = pos + offset
        if grid[new_pos] != 0: continue
        pr = grid.bfs_probe(new_pos, limit=5)
        weight = pr.max_distance
        if weight > 0:
            if pr.closest_obstacle_d is not None:
                weight -= pr.closest_obstacle_d
            options[weight] = dir

    if options:
        return options[max(options)]
    else:
        return '!'


if __name__ == '__main__':
    tc = TronClient(ai_wanderer)
    tc.run()
