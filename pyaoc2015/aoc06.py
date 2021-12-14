from functools import partial

from pyaoc2019.utils import read_file, mapt, exhaust
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False, part=1):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    res = []
    to_rc = lambda s: eval(f'RC({s})')
    for l in read_file(filename, 2015):
        tokens = l.split()
        s, e = tokens[-3], tokens[-1]

        start_rc = to_rc(s)
        end_rc = to_rc(e)
        if part == 1:
            match tokens[1]:
                case 'on':
                    fn = _turn_on
                case 'off':
                    fn = _turn_off
                case _:
                    fn = _toggle
        else:
            match tokens[1]:
                case 'on':
                    fn = _inc
                case 'off':
                    fn = _dec
                case _:
                    fn = partial(_inc, amount=2)

        res.append(partial(fn, start_rc=start_rc, end_rc=end_rc))
    return res


class RC(NamedTuple):
    r: int
    c: int

    def to(self, other):
        return {RC(r, c)
                for r in range(self.r, other.r + 1)
                for c in range(self.c, other.c + 1)}


def _turn_on(points: set[RC], start_rc, end_rc):
    points |= set(start_rc.to(end_rc))
    return points


def _turn_off(points: set[RC], start_rc, end_rc):
    points -= set(start_rc.to(end_rc))
    return points


def _toggle(points: set[RC], start_rc, end_rc):
    area = start_rc.to(end_rc)
    to_add = area - points
    to_rm = area & points
    return (points | to_add) - to_rm


def part1(cmds):
    points = set()
    for cmd in cmds:
        points = cmd(points)
    return len(points)


# ======================================================================================================================

def _inc(points: dict[RC, int], start_rc, end_rc, amount=1):
    for rc in start_rc.to(end_rc):
        points[rc] += amount


def _dec(points: dict[RC, int], start_rc, end_rc):
    for rc in start_rc.to(end_rc):
        if points[rc] > 0:
            points[rc] -= 1


def part2(cmds):
    points = dict.fromkeys(RC(0, 0).to(RC(999, 999)), 0)
    exhaust(cmd(points) for cmd in cmds)
    return sum(points.values())


def __main():
    data = parse_data(debug=False)
    # exhaust(print, data[:10])
    # print(part1(parse_data(part=1)))
    print(part2(parse_data(part=2)))
    # print(part2(data))


if __name__ == '__main__':
    __main()
