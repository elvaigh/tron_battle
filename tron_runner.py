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
        total_score = sum(self.player_scores)
        for i, score in enumerate(self.player_scores):
            print '{}:{} got {} points ({:.2f}%)'.format(
                    i, self.player_titles[i], score,
                    score * 100.0 / total_score)

    def render(self, server):
        """Remember the players and the score if it's last turn."""
        if len(server.alive_players) < 2:
            players = server.players_list
            player_titles = [player.title for player in players]

            if not self.player_titles:
                self.player_titles = player_titles
                self.player_scores = [0 for player in players]

            ps = sorted([(p.is_alive, p.steps, p) for p in players])
            for i, p_s in enumerate(ps):
                player = p_s[2]
                player.score_inc = 2 ** (i - 1) if i > 0 else 0
                self.player_scores[player.number] += player.score_inc

            self.games += 1
            print 'Game {} finished.'.format(self.games)
            for i, player in enumerate(players):
                if player.is_alive:
                    state = 'won'
                else:
                    state = 'died at turn {}'.format(player.steps)

                print '{}:{} {} [+{} = {} total points]'.format(
                        i, player.title, state,
                        player.score_inc, self.player_scores[i])
                del player.score_inc
            print


class TronRunner(object):
    """Run the tron battle using the server and renderer."""

    def __init__(self, server, renderer, config):
        self.server = server
        self.renderer = renderer
        self.framerate = config.framerate
        self.games_number = config.games_number
        self.players_file = config.players_file

    def add_players(self):
        """Add players from the config file."""
        with open(self.players_file) as fp:
            for line in fp:
                line = line.strip()
                if not line: continue
                if line.startswith('#'): continue
                title, command = line.split(':')
                self.server.add_player(title.strip(), command.strip())

        time.sleep(0.05)  # let the players initialize

    def run(self):
        """Run the game displaying the field."""
        for i in xrange(self.games_number):
            self.add_players()
            while len(self.server.alive_players) > 1:
                start = time.time()
                self.server.play_turn()
                self.renderer.render(self.server)
                if self.framerate is not None:
                    delay = start + (1.0 / self.framerate) - time.time()
                    if delay > 0:
                        time.sleep(delay)
            server.reset()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tron Battle runner.')
    parser.add_argument('--games-number', '-n', type=int, default=1,
            metavar='N', help='Number of games to run.')
    parser.add_argument('--framerate', '-f', type=int, default=7,
            metavar='N', help='Framerate for single game.')
    parser.add_argument('--players-file', '-p', type=str,
            default='players.conf', metavar='PLAYERS',
            help='File with players configuration.')
    config = parser.parse_args()

    if config.games_number == 1:
        renderer = CursesRenderer()
    else:
        renderer = MultigameRenderer()
        config.framerate = None

    server = TronServer()
    with renderer as renderer:
        runner = TronRunner(server, renderer, config)
        runner.run()
