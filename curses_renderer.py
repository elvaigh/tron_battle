"""
Tron battlefield renderer using curses.
"""

import curses


class CursesRenderer(object):
    """Renderer using curses."""

    def __enter__(self):
        self._init_curses()
        self.screen.clear()
        self.screen.refresh()
        return self

    def _init_curses(self):
        """Initialize colors."""
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.curs_set(0)

    def __exit__(self, exc_type, exc_value, traceback):
        """Return the terminal to normal state."""
        curses.endwin()

    def render_field(self, server):
        """Render the field."""
        field = self.screen.subwin(22, 32, 1, 1)

        for player in server.alive_players:
            for point in player.points:
                field.addch(point[1] + 1, point[0] + 1, ord('#'),
                        self.player_color(player.number))

        field.border()

    def player_color(self, number):
        """Return color pair for drawing specific player."""
        return curses.color_pair(number + 1) | curses.A_BOLD

    def render_player_stats(self, server):
        """Render the information about the players."""
        stats_box = self.screen.subwin(5, 70, 23, 1)

        for i, player in sorted(server.players.items()):
            if player.is_alive:
                state = '{}:{} AVG:{:.2f} MAX:{:.2f} MSG:{}'.format(
                        i, player.title, player.avg_step_time,
                        player.max_step_time, player.msg)
            else:
                state = '{}:{} Dead at step {}'.format(
                    i, player.title, player.steps)

            stats_box.addstr(i + 1, 2, state, self.player_color(i))
            stats_box.chgat(i + 1, 2, self.player_color(i))

        stats_box.border()

    def render(self, server):
        """Render the game state."""
        self.screen.erase()
        self.render_field(server)
        self.render_player_stats(server)
        self.screen.refresh()


"""
class TTYServer(TronServer):

    PLAYER_COLORS = [colored.red, colored.green, colored.yellow, colored.blue]

    def __init__(self, framerate=5):
        TronServer.__init__(self)
        self.framerate = framerate

    def render_field(self):

        def format_cell(c):
            if c == 0: return ' '
            if 8 <= c < 12: c -= 4
            if 4 <= c < 8: c -= 4
            if 0 <= c < 4:
                return self.PLAYER_COLORS[c]('#').color_str
            return ' '

        def pg(c):
            return unichr(0x2500 + c).encode('utf-8')

        print pg(0x54) + pg(0x50) * 30 + pg(0x57)
        for start in range(0, 20 * 64, 64):
            print pg(0x51) + \
                    ''.join(map(format_cell, self.grid[start:start + 30]))\
                    + pg(0x51)
        print pg(0x5a) + pg(0x50) * 30 + pg(0x5d)

    def render_player_stats(self):
        for i, player in self.players.items():
            color = self.PLAYER_COLORS[i]
            if player.is_alive:
                print color()
            else:
                print color('{}:{} Dead at step {}'.format(
                    i, player.title, player.steps))

    def render(self):
        for i in xrange(20):
            print
        self.render_field()
        print
        self.render_player_stats()
"""
