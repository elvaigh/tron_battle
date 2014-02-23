Tron Battle
===========

Tools for making AI Players for Tron Battle
(http://www.codingame.com/cg/#!ranking:20).

To create an AI player:

    from client import TronClient  # @include(client.py)

    def lefter(players_count, my_number, players, grid):
        return 'LEFT'

    tc = TronClient(lefter)
    tc.run()

Note the `# @include(client.py)` comment in the first line. This is needed for
building a single-file client for using with online Tron Battle.

To test the player (assuming the code is in `ai_lefter.py`):

    from server import TronServer

    server = TronServer()
    server.add_player('Wanderer', 'python ai_wanderer.py')
    server.add_player('Lefter', 'python ai_lefter.py')
    server.run(framerate=7)

To make a single script that is usable for the online Tron Battle:

    $ python build_ai.py ai_lefter.py ~/output/ai_lefter.py
