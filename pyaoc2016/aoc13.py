from __future__ import annotations
from queue import Queue

from pyaoc2019.utils import timer


FAV_NUM = 1358


def is_open(x, y, fav_num=FAV_NUM):
    n = fav_num + x * x + 3 * x + 2 * x * y + y + y * y
    return not bin(n).count('1') % 2


def test():
    assert is_open(2, 0, 10)
    assert not is_open(0, 2, 10)
    assert is_open(7, 2, 10)
    assert is_open(0, 0, 10)
    assert is_open(0, 1, 10)
    assert is_open(1, 1, 10)


def part1(target, fav_num=FAV_NUM):
    q = Queue()
    start = 1, 1
    q.put((0, start))
    seen = {start}

    def _get_surrounding(x, y):
        for xo, yo in (1, 0), (-1, 0), (0, 1), (0, -1):
            xy = x + xo, y + yo

            if xy not in seen and xy[0] >= 0 and xy[1] >= 0 and is_open(*xy, fav_num):
                seen.add(xy)
                yield xy

    while not q.empty():
        level, xy = q.get()
        level += 1
        for xy_new in _get_surrounding(*xy):
            if xy_new == target:
                return level
            q.put((level, xy_new))


def part2(fav_num=FAV_NUM):
    q = Queue()
    start = 1, 1
    q.put((0, start))
    seen = {start}

    def _get_surrounding(x, y):
        for xo, yo in (1, 0), (-1, 0), (0, 1), (0, -1):
            xy = x + xo, y + yo

            if xy not in seen and xy[0] >= 0 and xy[1] >= 0 and is_open(*xy, fav_num):
                seen.add(xy)
                yield xy

    while not q.empty():
        level, xy = q.get()
        level += 1
        if level > 50:
            continue
        for xy_new in _get_surrounding(*xy):
            q.put((level, xy_new))
    return len(seen)


def __main():
    test()
    print(part1((7, 4), 10))
    print(part1((31, 39)))
    print(part2())


if __name__ == '__main__':
    __main()
