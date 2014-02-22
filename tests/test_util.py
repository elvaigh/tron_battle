"""
Tests for the util module.
"""

import pytest

from grid import TronGrid


@pytest.fixture
def tg():
    return TronGrid()


def test_constructor(tg):
    assert tg.grid.count(0) == 600


def test_bfs_fill(tg):
    tg.bfs_fill(42, [0])

    assert tg.grid.count(0) == 0
    assert tg.grid.count(42) == 600


def test_bfs_probe_center(tg):
    res = tg.bfs_probe(tg.coords2index(15, 10))

    assert res.closest_obstacle_d == 10
    assert res.closest_obstacle == -1
    assert res.max_distance == 25
    assert res.empty_count == 599  # start point is never counted
    assert res.values == {-1}


def test_bsf_probe_objs(tg):
    tg.put(10, 8, 1)
    tg.put(5, 19, 2)

    res = tg.bfs_probe(tg.coords2index(15, 10))

    assert res.closest_obstacle_d == 7
    assert res.closest_obstacle == 1
    assert res.max_distance == 25
    assert res.empty_count == 597  # subtract two points and start point
    assert res.values == {1, 2, -1}


@pytest.fixture
def tg_box1(tg):
    """Field with the tail of tron #1 going around the middle."""
    for x in xrange(5, 25):
        tg.put(x, 5, 1)
        tg.put(x, 15, 1)
    for y in xrange(5, 15):
        tg.put(5, y, 1)
        tg.put(25, y, 1)
    return tg


@pytest.fixture
def tg_box1_in(tg_box1):
    """Field with the tron #1 in the middle inside of its own tail."""
    tg_box1.put(6, 6, 5)
    return tg_box1


@pytest.fixture
def tg_box1_out(tg_box1):
    """Field with the tron #1 in the middle just outside of its own tail."""
    tg_box1.put(5, 4, 5)
    return tg_box1


def test_bsf_probe_box1(tg_box1):
    res = tg_box1.bfs_probe(tg_box1.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == 1
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 1
    assert res.values == {1}


def test_bsf_probe_box1_limit(tg_box1):
    res = tg_box1.bfs_probe(tg_box1.coords2index(15, 10), limit=3)

    assert res.closest_obstacle_d is None
    assert res.closest_obstacle is None
    assert res.max_distance == 3
    assert res.empty_count == 24
    assert res.values == set()


def test_bsf_probe_box1_in(tg_box1_in):
    res = tg_box1_in.bfs_probe(tg_box1_in.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == 1
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 2
    assert res.values == {1, 5}


def test_bsf_probe_box1_out(tg_box1_out):
    res = tg_box1_out.bfs_probe(tg_box1_out.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == 1
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 1
    assert res.values == {1}


def test_bfs_probe_pois(tg_box1):
    c2i = tg_box1.coords2index
    right = c2i(16, 10)
    left = c2i(14, 10)
    up = c2i(15, 9)
    out = c2i(1, 1)

    res = tg_box1.bfs_probe(c2i(15, 10), pois={right, left, up, out})

    assert res.pois_reached == {left, right, up}
