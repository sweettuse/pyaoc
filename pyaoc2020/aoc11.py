from itertools import product, count

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

surrounding = frozenset(RC(r, c) for r, c in product(range(-1, 2), range(-1, 2))) - {RC(0, 0)}


def parse_map(fname=11, include_floor=False):
    res = {}
    for r, row in enumerate(read_file(fname, 2020)):
        for c, val in enumerate(row):
            if include_floor or val != '.':
                res[RC(r, c)] = val
    return res


def _find_equilibrium(data, new_state):
    cur, prev = data, None

    while cur != prev:
        prev, cur = cur, {rc: new_state(rc, cur) for rc in cur}

    return sum(v == '#' for v in cur.values())


def part1():
    data = parse_map(11)

    def _calc_occupied(rc, board):
        return sum(board.get(rc + offset) == '#' for offset in surrounding)

    def _new_state(rc, board):
        res = state = board[rc]
        occupied = _calc_occupied(rc, board)

        if state == 'L' and occupied == 0:
            res = '#'
        elif state == '#' and occupied >= 4:
            res = 'L'

        return res

    return _find_equilibrium(data, _new_state)


def part2():
    data = parse_map(11, include_floor=True)

    def _find_first_visible_seats(rc):
        res = set()

        for offset in surrounding:
            cur = rc + offset

            while True:
                if (state := data.get(cur)) is None:
                    break
                elif state in set('L#'):
                    res.add(cur)
                    break
                cur += offset

        return res

    visible_map = {rc: _find_first_visible_seats(rc) for rc in data}
    data = {rc: val for rc, val in data.items() if val != '.'}

    def _calc_occupied(board, visible):
        return sum(board[rc] == '#' for rc in visible)

    def _new_state(rc, board):
        res = state = board[rc]
        occupied = _calc_occupied(board, visible_map[rc])

        if state == 'L' and occupied == 0:
            res = '#'
        elif state == '#' and occupied >= 5:
            res = 'L'

        return res

    return _find_equilibrium(data, _new_state)


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
