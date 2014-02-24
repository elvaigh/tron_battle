"""
Tests for the util module.
"""

import pytest

from grid import TronGrid


@pytest.fixture
def tg():
    return TronGrid()


@pytest.fixture
def center():
    return TronGrid.coords2index(15, 10)


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
    assert res.objects == {-1}


def test_ray_probe_center(tg, center):

    def check(dir, width, m, d, e):
        res = tg.ray_probe(center, tg.DIRECTIONS[dir], width)
        assert res.closest_obstacle_d == d + 1
        assert res.closest_obstacle == -1
        assert res.max_distance == m
        assert res.empty_count == e
        assert res.objects == {-1}

    check('UP', 0, 10, 10, 10)
    check('DOWN', 0, 9, 9, 9)
    check('LEFT', 0, 15, 15, 15)
    check('RIGHT', 0, 14, 14, 14)

    check('UP', 5, 10, 10, 50)
    check('UP', 10, 10, 10, 100)
    check('DOWN', 5, 9, 9, 41)
    check('DOWN', 10, 9, 9, 81)
    check('LEFT', 5, 15, 15, 113)
    check('LEFT', 10, 15, 10, 200)
    check('RIGHT', 5, 14, 14, 98)
    check('RIGHT', 10, 14, 10, 180)


def test_bsf_probe_objs(tg, center):
    tg.put(10, 8, 1)
    tg.put(5, 19, 2)

    res = tg.bfs_probe(center)

    assert res.closest_obstacle_d == 7
    assert res.closest_obstacle == 1
    assert res.max_distance == 25
    assert res.empty_count == 597  # subtract two points and start point
    assert res.objects == {1, 2, -1}
    assert res.obj2dist[1] == 7
    assert res.obj2dist[2] == 19
    assert res.obj2dist[-1] == 10


def test_ray_probe_objs(tg, center):
    tg.put(20, 10, 1)
    tg.put(25, 10, 2)
    tg.put(25, 13, 3)

    res = tg.ray_probe(center, tg.DIRECTIONS['RIGHT'], 0)
    assert res.objects == {1}
    assert res.obj2dist[1] == 5

    res = tg.ray_probe(center, tg.DIRECTIONS['RIGHT'], 4)
    assert res.objects == {1, 3, -1}
    assert res.obj2dist[3] == 10


@pytest.fixture
def tg_box1(tg):
    """Field with the tail of tron #1 going around the middle."""
    for x in xrange(5, 25):
        tg.put(x, 5, tg.body_of(0))
        tg.put(x, 15, tg.body_of(0))
    for y in xrange(5, 15):
        tg.put(5, y, tg.body_of(0))
        tg.put(25, y, tg.body_of(0))
    return tg


@pytest.fixture
def tg_box1_in(tg_box1):
    """Field with the tron #0 in the middle inside of its own tail."""
    tg_box1.put(6, 6, tg_box1.head_of(0))
    return tg_box1


@pytest.fixture
def tg_box1_out(tg_box1):
    """Field with the tron #0 in the middle just outside of its own tail."""
    tg_box1.put(5, 4, tg_box1.head_of(0))
    return tg_box1


def test_bsf_probe_box1(tg_box1):
    res = tg_box1.bfs_probe(tg_box1.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == tg_box1.body_of(0)
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 1
    assert res.objects == {tg_box1.body_of(0)}


def test_bsf_probe_box1_limit(tg_box1):
    res = tg_box1.bfs_probe(tg_box1.coords2index(15, 10), limit=3)

    assert res.closest_obstacle_d is None
    assert res.closest_obstacle is None
    assert res.max_distance == 3
    assert res.empty_count == 24
    assert res.objects == set()


def test_bsf_probe_box1_in(tg_box1_in):
    res = tg_box1_in.bfs_probe(tg_box1_in.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == tg_box1_in.body_of(0)
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 2
    assert res.objects == {tg_box1_in.body_of(0), tg_box1_in.head_of(0)}


def test_bsf_probe_box1_out(tg_box1_out):
    res = tg_box1_out.bfs_probe(tg_box1_out.coords2index(15, 10))

    assert res.closest_obstacle_d == 5
    assert res.closest_obstacle == tg_box1_out.body_of(0)
    assert res.max_distance == 13
    assert res.empty_count == (9 * 19) - 1
    assert res.objects == {tg_box1_out.body_of(0)}


def test_bfs_probe_pois(tg_box1):
    c2i = tg_box1.coords2index
    right = c2i(16, 10)
    left = c2i(14, 10)
    up = c2i(15, 9)
    out = c2i(1, 1)

    res = tg_box1.bfs_probe(c2i(15, 10), pois={right, left, up, out})

    assert res.pois_reached == {left, right, up}
