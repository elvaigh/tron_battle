# Tests for measuring performance of various components and algorithms.

import time
import sys
import os
import functools

dn = os.path.dirname
ap = os.path.abspath
sys.path.append(dn(dn(ap(__file__))))

from util import TronGrid


TEMPLATE = '{name} ({count} times): {msecs:.0f} ms ({once:.3f} ms on average)'


def timed(times):
    def timed_decorator(function):
        @functools.wraps(function)
        def timed_func():
            start = time.time()
            for i in xrange(times):
                function()
            end = time.time()
            secs = end - start
            msecs = secs * 1000.0
            once = msecs / times
            print TEMPLATE.format(name=function.__name__, count=times,
                    msecs=msecs, once=once)
        return timed_func
    return timed_decorator


@timed(500)
def bfs_fill1():
    t = TronGrid()
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
def bfs_fill2():
    t = TronGrid()
    for y in xrange(0, 19):
        idx1 = t.coords2index(10, y)
        idx2 = t.coords2index(20, 19 - y)
        t[idx1] = t[idx2] = 1
    t.bfs_fill(42, [t.coords2index(5, 10)])
    return t


@timed(500)
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


@timed(30)
def replace100_100():
    t = TronGrid()
    for i in xrange(100):
        t.replace(i, i + 1)
    return t


@timed(30)
def replace1_100():
    t = TronGrid()
    t[655] = 1
    for i in xrange(1, 101):
        t.replace(i, i + 1)
    return t


@timed(100)
def copy_100():
    t = TronGrid()
    for i in xrange(100):
        t1 = t.copy()
    return t1


if __name__ == '__main__':
    copy_100()
    replace1_100()
    replace100_100()
    bfs_fill1()
    bfs_fill3()
