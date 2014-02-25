"""
Tron battlefield renderer using curses.
"""

import curses


class CursesRenderer(object):
    """Renderer using curses."""

    def __enter__(self):
        self._init_curses()
        self._init_charmap()
        self.screen.clear()
        self.screen.refresh()
        return self

    def _init_charmap(self):
        """Initialize the map of characters for drawing snakes."""
        charmap = """
            _U,_D,UU,DD:VLINE
            _L,_R,LL,RR:HLINE
            UL,RD:URCORNER
            UR,LD:ULCORNER
            DL,RU:LRCORNER
            DR,LU:LLCORNER
            U_,D_,L_,R_,__:DIAMOND
        """
        self.charmap = {}
        for group in charmap.split():
            if not group: continue
            moves, charname = group.split(':')
            for move in moves.split(','):
                self.charmap[move] = getattr(curses, 'ACS_' + charname)

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

    def snake_char(self, move, next_move):
        """Return the character for drawing the move."""
        if move is None: move = '_'
        if next_move is None: next_move = '_'
        return self.charmap[move[0] + next_move[0]]

    def player_color(self, number):
        """Return color pair for drawing specific player."""
        return curses.color_pair(number + 1) | curses.A_BOLD

    def render_field(self, server):
        """Render the field."""
        field = self.screen.subwin(22, 32, 1, 1)

        for player in server.alive_players:
            for i, point in enumerate(player.points):
                if i == 0:
                    char = self.snake_char('_', player.get_move(0))
                else:
                    char = self.snake_char(player.get_move(i - 1),
                            player.get_move(i))
                field.addch(point[1] + 1, point[0] + 1, char,
                        self.player_color(player.number))

        field.border()

    def format_player_info(self, player):
        """Format the information about the player."""
        stats = 'AVG:{:.2f} MAX:{:.2f}'.format(player.avg_step_time,
                player.max_step_time)
        title = '{}:{}'.format(player.number, player.title)
        msg = 'MSG:{}'.format(player.msg) if player.is_alive\
                else 'Died at turn {} (MSG:{})'.format(player.steps,
                        player.msg)

        return '{} {} {}'.format(title, stats, msg)

    def render_player_info(self, server):
        """Render the information about the players."""
        stats_box = self.screen.subwin(7, 70, 23, 1)

        stats_box.addstr(1, 2, 'Turn {}:'.format(server.turn_count))
        for i, player in sorted(server.players.items()):
            stats_box.addstr(i + 2, 2, self.format_player_info(player),
                    self.player_color(i))

        stats_box.border()

    def render(self, server):
        """Render the game state."""
        self.screen.erase()
        self.render_field(server)
        self.render_player_info(server)
        self.screen.refresh()
