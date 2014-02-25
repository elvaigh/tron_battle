"""
Base class for class-based AIs.
"""

import argparse


class ParamDescr(object):
    """AI parameter descriptor."""

    def __init__(self, **kw):
        if 'name' not in kw:
            raise ValueError('name is mandatory.')
        self.kw = kw

    def update(self, **kw):
        for key, value in kw.items():
            if value is not None:
                self.kw[key] = value

    @property
    def arg_args(self):
        """Return option names for ``argparse.add_argument``."""
        ret = ['--' + self.kw['name'].replace('_', '-')]
        if 'letter' in self.kw:
            ret.append('-' + self.kw['letter'])
        return ret

    @property
    def arg_kw(self):
        """Return keyword args for ``argparse.add_agrument``."""
        kw = dict(self.kw)
        for drop in ['name', 'letter']:
            if drop in kw:
                del kw[drop]
        if self.kw['type'] == bool:
            kw['action'] = 'store_true'
            del kw['type']
        return kw


class AIBase(object):
    """Configure from the config object and provide basic __call__."""

    def __init__(self):
        super(AIBase, self).__init__()

    def add_param(self, name, letter=None, type=int, default=None, help=None):
        """Add a parameter to the algorithm."""
        if default is None and hasattr(self, name):
            default = getattr(self, name)

        descriptor_name = '_' + name + '_descriptor'

        if hasattr(self, descriptor_name):
            descriptor = getattr(self, descriptor_name)
            descriptor.update(letter=letter, type=type, default=default,
                    help=help)
        else:
            descriptor = ParamDescr(name=name, letter=letter, type=type,
                    default=default, help=help)
            setattr(self, descriptor_name, descriptor)

    def configure(self):
        """Configure from script agruments based on parameters."""
        parser = argparse.ArgumentParser(description=self.__doc__,
                formatter_class=argparse.RawTextHelpFormatter)
        for var in sorted(vars(self)):
            if var.endswith('_descriptor'):
                descriptor = getattr(self, var)
                parser.add_argument(*descriptor.arg_args, **descriptor.arg_kw)
        config = parser.parse_args()
        for key in vars(config):
            setattr(self, key, getattr(config, key))

    @property
    def my_pos(self):
        """Return the position as an index in the grid."""
        return self.grid.coords2index(self.my_x, self.my_y)

    def go(self):
        """Override to return the direction."""
        return 'LEFT'

    def __call__(self, players_count, my_number, players, grid):
        """Store the basic values."""
        self.players_count = players_count
        self.my_number = my_number
        self.players = players
        self.grid = grid
        self.my_x, self.my_y = players[my_number].head
        return self.go()
