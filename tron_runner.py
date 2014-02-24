"""
Tron runner script.
"""

import time

from curses_renderer import CursesRenderer
from server import TronServer


class TronRunner(object):
    """Run the tron battle using the server and renderer."""

    def __init__(self, server, renderer, framerate=5):
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
            remaining_delay = start + (1.0 / self.framerate) - time.time()
            if remaining_delay > 0:
                time.sleep(remaining_delay)


if __name__ == '__main__':
    with CursesRenderer() as renderer:
        server = TronServer()
        runner = TronRunner(server, renderer, 10)
        server.add_player('wanderer 5', 'python ai_wanderer.py 5')
        server.add_player('wanderer 15', 'python ai_wanderer.py 15')
        server.add_player('wanderer 45', 'python ai_wanderer.py 45')
        runner.run()
