"""
Tron runner script.
"""

import time
import argparse

from curses_renderer import CursesRenderer
from server import TronServer


class MultigameRenderer(object):
    """Renderer for multiple games."""

    def __enter__(self):
        self.player_titles = []
        self.player_scores = []
        self.games = 0
        return self

    def __exit__(self, *_):
        print '{} Games finished:'.format(self.games)
        for i, score in enumerate(self.player_scores):
            print '{}:{} won {} times ({:.2f}%)'.format(
                    i, self.player_titles[i], score,
                    score * 100.0 / self.games)

    def render(self, server):
        """Remember the players and the score if it's last turn."""
        if len(server.alive_players) < 2:
            players = server.players_list
            player_titles = [player.title for player in players]

            if self.player_titles:
                if player_titles != player_titles:
                    raise Exception('Player titles changed in progress.')
                for i, player in enumerate(players):
                    if player.is_alive:
                        self.player_scores[i] += 1
            else:
                self.player_titles = player_titles
                self.player_scores = [1 if player.is_alive else 0
                        for player in players]

            self.games += 1
            print 'Game {} finished.'.format(self.games)
            for i, player in enumerate(players):
                if player.is_alive:
                    state = 'won'
                else:
                    state = 'died at turn {}'.format(player.steps)

                print '{}:{} {} [{} total victories]'.format(
                            i, player.title, state, self.player_scores[i])
            print


class TronRunner(object):
    """Run the tron battle using the server and renderer."""

    def __init__(self, server, renderer, framerate=None):
        self.server = server
        self.renderer = renderer
        self.framerate = framerate

    def run(self):
        """Run the game displaying the field."""
        time.sleep(0.1)  # let the players initialize

        while len(self.server.alive_players) > 1:
            start = time.time()
            self.server.play_turn()
            self.renderer.render(self.server)
            if self.framerate is not None:
                remaining_delay = start + (1.0 / self.framerate) - time.time()
                if remaining_delay > 0:
                    time.sleep(remaining_delay)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tron Battle runner.')
    parser.add_argument('--games-number', '-n', type=int, default=1,
            metavar='N', help='Number of games to run.')
    parser.add_argument('--framerate', '-f', type=int, default=7,
            metavar='N', help='Framerate for single game.')
    config = parser.parse_args()

    if config.games_number == 1:
        renderer = CursesRenderer()
    else:
        renderer = MultigameRenderer()
        config.framerate = None

    with renderer as renderer:
        for i in xrange(config.games_number):
            server = TronServer()
            runner = TronRunner(server, renderer, config.framerate)
            server.add_player('wanderer', 'python ai_wanderer.py')
            server.add_player('wanderer', 'python ai_wanderer.py -s 10 -o 10')
            server.add_player('wanderer', 'python ai_wanderer.py -o -100')
            runner.run()
