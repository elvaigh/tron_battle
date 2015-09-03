Tron Battle
===========

Tools for making AI Players for Tron Battle
(http://www.codingame.com/cg/#!ranking:20).

Here's a screenshot:

    ┌──────────────────────────────┐
    │                              │
    │                              │
    │                              │
    │                              │
    │                              │
    │                              │
    │                              │
    │                              │
    │ ┌───────────────┐            │
    │ │ ┌─────────────┘┌──────────┐│
    │ └┐└─────────────┐│┌─────────┘│
    │  │┌─────────────┘│└─────────┐│
    │┌┐│└────────┐┌────┘┌─────────┘│
    ││││┌────────┘│┌───┐└─────────┐│
    │││││┌┐┌┐┌┐┌┐┌┘└──┐└──────────┘│
    ││││││││││││││    └◆           │
    ││││││││││││││                 │
    ││└┘└┘└┘└┘└┘└┘                 │
    │└─────────────                │
    │                              │
    └──────────────────────────────┘
    ┌────────────────────────────────────────────────────────────────────┐
    │ Turn 246:                                                          │
    │ 0:wanderer 5 AVG:0.51 MAX:1.83 Died at turn 246                    │
    │ 1:wanderer 15 AVG:1.03 MAX:3.70 Died at turn 125                   │
    │ 2:wanderer 45 AVG:1.92 MAX:5.06 MSG:RIGHT                          │
    │                                                                    │
    └────────────────────────────────────────────────────────────────────┘

To create an AI player:

    from client import TronClient  # @include(client.py)

    def lefter(players_count, my_number, players, grid):
        return 'LEFT'

    tc = TronClient(lefter)
    tc.run()

Note the `# @include(client.py)` comment in the first line. This is needed for
building a single-file client for using with online Tron Battle.

To test a player add it to players.conf and run:

    $ python tron_runner.py

Tron runner can run one or several battles and it writes the game into a
logfile in the current directory. Run it with ``-h`` to get information about
the command line options.

To make a single script that is usable for the online Tron Battle:

    $ python build_ai.py ai_lefter.py ~/output/ai_lefter.py
