"""
Tron Battle client library. Basic code for talking to the server.
"""

from player import PlayerInfo  # @include(player.py)


class TronClient(object):

    players = None

    def __init__(self, handler):
        self.handler = handler

    @staticmethod
    def read_numbers():
        return map(int, raw_input().split())

    def handle_input(self):
        if self.players is None:
            self.players = {}

        self.players_count, self.my_number = self.read_numbers()

        for i in xrange(self.players_count):
            coords = self.read_numbers()
            if i not in self.players:
                self.players[i] = PlayerInfo(i, *coords)
            else:
                self.players[i].move(*coords)

    @property
    def my_player(self):
        if self.players is None:
            return None
        else:
            return self.players[self.my_number]

    def run(self):
        while 1:
            if self.my_player is not None and not self.my_player.alive:
                return
            self.handle_input()
            print self.handler(self)
