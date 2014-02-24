"""
Tron Battle server.
"""

import os
import random
import time
import datetime
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
        self.points = []
        self.process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE,
                stderr=PIPE)

    def log(self, msg):
        """Log the message (to the server log)."""
        self.server_log('[Player {}:{}] {}'.format(self.number,
            self.title, msg))

    def get_move(self, index):
        """Return the move with a given number as a string.

        :return: "UP", "DOWN", "LEFT", "RIGHT" or None.
        """
        try:
            if index >= 0:
                last = self.points[index + 1]
                prev = self.points[index]
            else:
                last = self.points[index]
                prev = self.points[index - 1]
        except IndexError:
            return None

        last, prev = map(lambda pt: TronGrid.coords2index(*pt), [last, prev])
        offset = last - prev
        r_dir = {off: dir for dir, off in TronGrid.DIRECTIONS.items()}
        return r_dir.get(offset, None)

    @property
    def avg_step_time(self):
        return self.total_step_time / self.steps

    def move(self, x0, y0, x1, y1):
        """Add logging to moving."""
        PlayerInfo.move(self, x0, y0, x1, y1)

        if self.points:
            if self.points[-1] != (x1, y1):
                self.points.append((x1, y1))
        else:
            if (x0, y0) == (x1, y1):
                self.points = [(x1, y1)]
            else:
                self.points = [(x0, y0), (x1, y1)]

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
        self.players = {}
        self.open_log_file()
        self.reset()
        random.seed(time.time())

    def open_log_file(self):
        """Open the log file."""
        self.log_filename = os.path.join(os.getcwd(),
                time.strftime('tron-log-%Y%m%d%H%M%S'))
        self.log_fp = open(self.log_filename, 'at')
        self.log('Opened log')

    def reset(self):
        """Reset the game."""
        if self.players:
            for player in self.alive_players:
                player.die('Game finished.')
        self.grid = TronGrid()
        self.player_count = 0
        self.turn_count = 0
        self.players = {}
        self.log('Initialized battle field.')

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

    @property
    def players_list(self):
        """Return the players as a list."""
        return [self.players[i] for i in xrange(len(self.players))]

    def play_turn(self):
        """Play one turn for all alive players."""
        self.turn_count += 1
        self.log('Starting turn {}'.format(self.turn_count))
        for player in self.alive_players:
            self.play_player_turn(player)
        self.log('Completed turn {}'.format(self.turn_count))
