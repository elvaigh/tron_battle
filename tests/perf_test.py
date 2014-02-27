# Tests for measuring performance of various components and algorithms.

import time
import sys
import os
import functools

dn = os.path.dirname
ap = os.path.abspath
sys.path.append(dn(dn(ap(__file__))))
sys.path.append(dn(ap(__file__)))

from test_grid import tg, tg_box1
from test_minimax import tg as mm_tg, player as mm_player

from minimax import MiniMax


TEMPLATE = '{name}\n\tx {count} = {msecs:.3f} ms, average = {once:.3f} {unit}'


def timed(times, in_times=1):
    def timed_decorator(function):
        @functools.wraps(function)
        def timed_func():
            start = time.time()
            for i in xrange(times):
                function()
            end = time.time()
            msecs = (end - start) * 1000.0
            once = msecs / times / in_times
            unit = 'ms'
            if once < 1:
                once *= 1000
                unit = '\xc2\xb5s'
            name = function.__doc__ or function.__name__
            if name.endswith('.'):
                name = name[:-1] + ':'
            print TEMPLATE.format(name=name, count=times * in_times,
                    msecs=msecs, once=once, unit=unit)
        return timed_func
    return timed_decorator


@timed(500)
def bfs_fill1():
    """Fill an empty grid."""
    t = tg()
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
def bfs_fill2():
    """Fill the grid with two dividers."""
    t = tg()
    for y in xrange(0, 19):
        idx1 = t.coords2index(10, y)
        idx2 = t.coords2index(20, 19 - y)
        t[idx1] = t[idx2] = 1
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
def bfs_fill3():
    """Fill a maze."""
    t = tg()
    for y in xrange(0, 19):
        for x in range(1, 29, 2):
            if x % 4 == 1:
                idx = t.coords2index(x, y)
            else:
                idx = t.coords2index(x, 19 - y)
            t[idx] = 1
    t.bfs_fill(42, [t.coords2index(0, 0)])
    return t


@timed(30, 100)
def replace600_100():
    """Replace a value that has 600 positions in the grid."""
    t = tg()
    for i in xrange(100):
        t.replace(i, i + 1)
    return t


@timed(30, 100)
def replace1_100():
    """Replace a value that has 1 position in the grid."""
    t = tg()
    t[655] = 1
    for i in xrange(1, 101):
        t.replace(i, i + 1)
    return t


@timed(50, 100)
def copy_100():
    """Copy the whole grid."""
    t = tg()
    for i in xrange(100):
        t1 = t.copy()
    return t1


@timed(1000)
def bfs_probe_empty():
    """BFS probe in the empty grid from the center."""
    t = tg()
    t.bfs_probe(t.coords2index(15, 10))


@timed(1000)
def bfs_probe_box():
    """BFS probe from the box in the center."""
    t = tg_box1(tg())
    t.bfs_probe(t.coords2index(15, 10))


@timed(1000)
def bfs_probe_limit10():
    """BFS probe with the limit of 10."""
    t = tg()
    t.bfs_probe(t.coords2index(15, 10), limit=10)


@timed(50, 100)
def ray_probe_empty0_100():
    """Ray probe from the center, width = 0."""
    t = tg()
    for i in xrange(100):
        t.ray_probe(t.coords2index(15, 10), t.DIRECTIONS['RIGHT'])


@timed(50, 100)
def ray_probe_empty5_100():
    """Ray probe from the center, width = 5."""
    t = tg()
    for i in xrange(100):
        t.ray_probe(t.coords2index(15, 10), t.DIRECTIONS['RIGHT'], 5)


@timed(50, 100)
def ray_probe_box10_100():
    """Ray probe inside the box, width = 10."""
    t = tg_box1(tg())
    for i in xrange(100):
        t.ray_probe(t.coords2index(15, 10), t.DIRECTIONS['RIGHT'], 10)


@timed(50, 100)
def ray_probe_l5_100():
    """Ray probe inside the box, width = 10, limit=5."""
    t = tg()
    for i in xrange(100):
        t.ray_probe(t.coords2index(15, 10), t.DIRECTIONS['RIGHT'], 10, limit=5)


@timed(30)
def mm_find_best():
    """MiniMax find best move (max_layers=3)."""
    t = mm_tg()
    t.vline(3, 0, 15, t.body_of(1))

    mm = MiniMax(t, mm_player())
    mm.find_best_move(max_layers=3)


if __name__ == '__main__':
    copy_100()
    replace1_100()
    replace600_100()
    bfs_fill1()
    bfs_fill3()
    bfs_probe_empty()
    bfs_probe_box()
    bfs_probe_limit10()
    ray_probe_empty0_100()
    ray_probe_empty5_100()
    ray_probe_box10_100()
    ray_probe_l5_100()
    mm_find_best()
