from cytoolz import first

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file, Direction

__author__ = 'acushner'

dirs = dict(zip('DRUL', (d.value for d in Direction)))

bounds = RC(0, 0), RC(3, 3)


def aoc02_a(instructions):
    keyboard = list(map(list, ('123 456 789'.split())))

    def _calc_row(cur, row):
        for d in row:
            next_pos = cur + dirs[d]
            if next_pos.in_bounds(*bounds):
                cur = next_pos
        return cur

    cur = RC(1, 1)
    res = []
    for row in instructions:
        r, c = cur = _calc_row(cur, row)
        res.append(keyboard[r][c])
    return ''.join(res)


def aoc02_b(instructions):
    keyboard = """       
   1   
  234  
 56789 
  ABC  
   D   
       """
    keyboard = list(map(list, keyboard.splitlines()))

    def _calc_row(cur, row):
        for d in row:
            r, c = next_pos = cur + dirs[d]
            if keyboard[r][c] != ' ':
                cur = next_pos
        return cur

    r, c = cur = RC(3, 1)
    print(keyboard[r][c])
    res = []
    for row in instructions:
        r, c = cur = _calc_row(cur, row)
        res.append(keyboard[r][c])
    return ''.join(res)


def __main():
    instructions = read_file(2, 2016)
    # instructions = read_file('02.test', 2016)
    print(aoc02_a(instructions))
    print(aoc02_b(instructions))


if __name__ == '__main__':
    __main()
