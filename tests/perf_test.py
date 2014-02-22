# Tests for measuring performance of various components and algorithms.

import time
import sys
import os
import functools

dn = os.path.dirname
ap = os.path.abspath
sys.path.append(dn(dn(ap(__file__))))
sys.path.append(dn(ap(__file__)))

from util import TronGrid
from test_util import tg, tg_box1


TEMPLATE = '{name} ({count} times): {msecs:.0f} ms ({once:.3f} ms on average)'


def timed(times):
    def timed_decorator(function):
        @functools.wraps(function)
        def timed_func():
            start = time.time()
            for i in xrange(times):
                function()
            end = time.time()
            msecs = (end - start) * 1000.0
            once = msecs / times
            print TEMPLATE.format(name=function.__doc__ or function.__name__,
                    count=times, msecs=msecs, once=once)
        return timed_func
    return timed_decorator


@timed(500)
def bfs_fill1():
    """Fill an empty grid."""
    t = TronGrid()
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
def bfs_fill2():
    """Fill the grid with two dividers."""
    t = TronGrid()
    for y in xrange(0, 19):
        idx1 = t.coords2index(10, y)
        idx2 = t.coords2index(20, 19 - y)
        t[idx1] = t[idx2] = 1
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
def bfs_fill3():
    """Fill a maze."""
    t = TronGrid()
    for y in xrange(0, 19):
        for x in range(1, 29, 2):
            if x % 4 == 1:
                idx = t.coords2index(x, y)
            else:
                idx = t.coords2index(x, 19 - y)
            t[idx] = 1
    t.bfs_fill(42, [t.coords2index(0, 0)])
    return t


@timed(30)
def replace600_100():
    """Replace a value that has 600 positions in the grid."""
    t = TronGrid()
    for i in xrange(100):
        t.replace(i, i + 1)
    return t


@timed(30)
def replace1_100():
    """Replace a value that has 1 position in the grid."""
    t = TronGrid()
    t[655] = 1
    for i in xrange(1, 101):
        t.replace(i, i + 1)
    return t


@timed(50)
def copy_100():
    """Copy the whole grid 100 times."""
    t = TronGrid()
    for i in xrange(100):
        t1 = t.copy()
    return t1


@timed(500)
def bfs_probe_empty():
    """Probe in the empty grid from the center."""
    t = tg()
    t.bfs_probe(t.coords2index(15, 10))


@timed(500)
def bfs_probe_box():
    """Probe from the box in the center."""
    t = tg_box1(tg())
    t.bfs_probe(t.coords2index(15, 10))


@timed(500)
def bfs_probe_limit10():
    """Probe with the limit of 10."""
    t = tg()
    t.bfs_probe(t.coords2index(15, 10), limit=10)


if __name__ == '__main__':
    # copy_100()
    # replace1_100()
    # replace100_100()
    # bfs_fill1()
    bfs_fill3()
    bfs_probe_empty()
    bfs_probe_box()
    bfs_probe_limit10()
