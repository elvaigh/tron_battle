"""
Tests for the minimax module.
"""

import pytest
import mock

from grid import TronGrid
from minimax import MiniMax


@pytest.fixture
def tg():
    """Grid with two player heads."""
    tg = TronGrid()
    tg.put(2, 15, tg.head_of(1))
    tg.put(0, 5, tg.head_of(2))
    return tg


@pytest.fixture
def player():
    """Player mock."""
    return mock.Mock(x1=2, y1=15, number=1)


def test_init(tg, player):
    """Test initialization."""
    mm = MiniMax(tg, player)

    assert mm.my_number == 1
    assert mm.my_pos == tg.coords2index(2, 15)
    assert mm.opponents == {2: tg.coords2index(0, 5)}


def test_first_layer(tg, player):
    """Test computing the first layer in open field."""
    mm = MiniMax(tg, player)
    mm.compute_next_layer()

    assert len(mm.layers) == 1
    assert len(mm.layers[0]) == 4
    assert {state.moves[0].direction for state in mm.layers[0]} ==\
            set(tg.DIRECTIONS.keys())

    for state in mm.layers[0]:
        assert len(state.moves) == 1
        move = state.moves[0]
        assert move.player_number == 1
        assert move.is_mine is True
        assert mm.my_pos + tg.DIRECTIONS[move.direction] == state.player2pos[1]


def test_second_layer(tg, player):
    """Test computing two layers in open field with opponent next to wall."""
    mm = MiniMax(tg, player)
    mm.compute_next_layer()
    mm.compute_next_layer()

    assert len(mm.layers) == 2
    assert len(mm.layers[0]) == 4
    assert len(mm.layers[1]) == 12

    for state in mm.layers[0]:
        assert state.next_player == 2
        assert len(state.next_states) == 3
        assert {nstate.moves[1].direction for nstate in state.next_states} ==\
                set(tg.DIRECTIONS.keys()) - {'LEFT'}
        for nstate in state.next_states:
            assert nstate.player_number == 2
            assert nstate.prev_state == state
            assert len(nstate.moves) == 2
            move = nstate.moves[1]
            assert move.is_mine == False
            assert move.player_number == 2
            assert mm.opponents[2] + tg.DIRECTIONS[move.direction] ==\
                    nstate.player2pos[2]


def test_catch(tg, player):
    """Test catching the other player."""
    tg.vline(3, 0, 15, tg.body_of(1))
    mm = MiniMax(tg, player)

    weight, move = mm.find_best_move(max_layers=3)
    assert move == 'LEFT'
