"""
build_ai.py -- package AI code into one file.

usage:
    build_ai.py <main_ai_file.py> <target_file.py>
"""

import sys


included = set()


def read_file(filename):
    if filename in included:
        return []
    else:
        included.add(filename)
        with open(filename, 'rt') as fp:
            return ['### {}'.format(filename)] + fp.readlines()


source, target = sys.argv[1:]


with open(target, 'wt') as fp:
    lines = read_file(source)
    while lines:
        line = lines.pop(0)
        inc = line.find('# @include(')
        if inc == -1:
            fp.write(line)
        else:
            lines = read_file(line[inc + 11].split(')')[0]) + lines
