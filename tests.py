# Tests for measuring performance of various components and algorithms.

from util import TronGrid


def bfs_fill1():
    t = TronGrid()
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


def bfs_fill2():
    t = TronGrid()
    for y in xrange(0, 19):
        idx1 = t.coords2index(10, y)
        idx2 = t.coords2index(20, 19 - y)
        t[idx1] = t[idx2] = 1
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


def bfs_fill3():
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


def replace1_100():
    t = TronGrid()
    for i in xrange(100):
        t.replace(i, i + 1)
    return t


def replace2_100():
    t = TronGrid()
    t[655] = 1
    for i in xrange(1, 101):
        t.replace(i, i + 1)
    return t


def copy_100():
    t = TronGrid()
    for i in xrange(100):
        t1 = t.copy()
    return t1