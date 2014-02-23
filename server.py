"""
Tron Battle server.
"""

import os
import random
import time
import datetime
from clint.textui import colored
from subprocess import Popen, PIPE

from grid import TronGrid
from player import PlayerInfo


class PlayerProgram(PlayerInfo):
    """Controller of a player program."""

    def __init__(self, number, title, command, server_log):
        PlayerInfo.__init__(self, number)
        self.steps = 0
        self.total_step_time = 0
        self.max_step_time = 0
        self.title = title
        self.msg = ''
        self.server_log = server_log
        self.process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
                stderr=PIPE)

    def log(self, msg):
        """Log the message (to the server log)."""
        self.server_log('[Player {}:{}] {}'.format(self.number,
            self.title, msg))

    @property
    def avg_step_time(self):
        return self.total_step_time / self.steps

    def move(self, x0, y0, x1, y1):
        """Add logging to moving."""
        PlayerInfo.move(self, x0, y0, x1, y1)
        self.log('New coordinates: {} {} {} {}'.format(x0, y0, x1, y1))

    def send_numbers(self, *numbers):
        """Send space-separated line of numbers to the program."""
        to_send = ' '.join(map(str, numbers))
        try:
            self.process.stdin.write(to_send + '\n')
            self.process.stdin.flush()
            self.log('Sent {}'.format(to_send))
        except IOError, err:
            self.log('Error while sending: {}'.format(err))

    def send_game_info(self, player_count):
        """Send the opening line: player count and player number."""
        self.send_numbers(player_count, self.number)

    def send_player_coords(self, player):
        """Send the coordinates of the player."""
        self.send_numbers(*player.coords)

    def receive_command(self):
        """Receive one line from the program."""
        start = time.time()
        got = self.process.stdout.readline().strip()
        self.msg = got
        end = time.time()
        step_time = (end - start) * 1000.0
        self.steps += 1
        self.total_step_time += step_time
        if step_time > self.max_step_time:
            self.max_step_time = step_time
        self.log('Received {} (in {} ms)'.format(got, step_time))
        return got

    def check_stderr(self):
        """Check program stderr and return anything that got there."""
        # TODO
        return None

    def die(self, msg):
        """Terminate this player."""
        self.log('Died: {}'.format(msg))
        self.is_alive = False
        self.process.terminate()
        self.process = None


class TronServer(object):

    def __init__(self):
        self.grid = TronGrid()
        self.player_count = 0
        self.turn_count = 0
        self.players = {}
        self.open_log_file()
        random.seed(time.time())

    def open_log_file(self):
        """Open the log file."""
        self.log_filename = os.path.join(os.getcwd(),
                time.strftime('tron-log-%Y%m%d%H%M%S'))
        self.log_fp = open(self.log_filename, 'at')
        self.log('Opened log')

    def log(self, msg):
        """Write the message to the log."""
        timestamp = datetime.datetime.now().time().isoformat()
        self.log_fp.write('[{}] {}\n'.format(timestamp, msg))

    def find_empty_spot(self):
        """Find an empty point in the field."""
        while 1:
            x = random.randrange(30)
            y = random.randrange(20)
            if self.grid.get(x, y) == 0:
                return x, y

    def add_player(self, title, command):
        """Launch a player and add to the game."""
        index = self.player_count
        self.player_count += 1

        player = self.players[index] = \
                PlayerProgram(index, title, command, self.log)
        self.log('Added player {} as {} ({})'.format(title, index, command))

        x, y = self.find_empty_spot()
        player.move(x, y, x, y)

    def kill_player(self, player, msg):
        """Declare the player dead and remove from the field."""
        player.die(msg)
        self.grid.replace(self.grid.body_of(player.number), 0)
        self.grid.replace(self.grid.head_of(player.number), 0)

    def play_player_turn(self, player):
        """Play the turn of one player."""
        player.send_game_info(self.player_count)
        map(player.send_player_coords, self.players.values())

        cmd = player.receive_command()
        pos = self.grid.coords2index(*player.head)
        move = self.grid.DIRECTIONS.get(cmd, None)

        if move:
            new_pos = pos + move
            if self.grid[new_pos] != 0:
                self.kill_player(player, '{} is an illegal move.'.format(cmd))
            else:
                self.grid[pos] = self.grid.body_of(player.number)
                self.grid[new_pos] = self.grid.head_of(player.number)
                player.move(*(player.tail + self.grid.index2coords(new_pos)))
        else:
            self.kill_player(player, 'Invalid command: {}.'.format(cmd))

    @property
    def alive_players(self):
        """Return the list of alive players."""
        return filter(lambda p: p.is_alive, self.players.values())

    def play_turn(self):
        """Play one turn for all alive players."""
        self.turn_count += 1
        self.log('Starting turn {}'.format(self.turn_count))
        for player in self.alive_players:
            self.play_player_turn(player)
        self.log('Completed turn {}'.format(self.turn_count))

    def draw_field(self):
        """Display the field on the screen."""
        for i in xrange(20):
            print

        player_colors = [colored.red, colored.green, colored.yellow,
                colored.blue]

        def format_cell(c):
            if c == 0: return ' '
            if 8 <= c < 12: c -= 4
            if 4 <= c < 8: c -= 4
            if 0 <= c < 4:
                return player_colors[c]('#').color_str
            return ' '

        print '#' * 32
        for start in range(0, 20 * 64, 64):
            print '#' + ''.join(map(format_cell, self.grid[start:start + 30]))\
                    + '#'
        print '#' * 32

        for i, player in self.players.items():
            color = player_colors[i]
            if player.is_alive:
                print color('{}:{} AVG:{:.2f} MAX:{:.2f} MSG:{}'.format(
                    i, player.title, player.avg_step_time,
                    player.max_step_time, player.msg))
            else:
                print color('{}:{} Dead at step {}'.format(
                    i, player.title, player.steps))

    def run(self, framerate=10):
        """Run the game displaying the field."""
        time.sleep(0.1)  # let the players initialize
        delay = 1.0 / framerate
        while len(self.alive_players) > 1:
            start = time.time()
            self.play_turn()
            self.draw_field()
            time.sleep(start + delay - time.time())


if __name__ == '__main__':
    server = TronServer()
    server.add_player('wanderer 2', 'python ai_wanderer.py 2')
    server.add_player('wanderer 10', 'python ai_wanderer.py 10')
    server.add_player('wanderer 30', 'python ai_wanderer.py 30')
    server.run()
