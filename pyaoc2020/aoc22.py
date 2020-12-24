from collections import deque
from functools import wraps
from itertools import islice
from operator import lt, mul

from cytoolz.itertoolz import take

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def _parse_data(fname=22):
    res = deque(), deque()
    idx = 0
    it = iter(read_file(fname, 2020))
    next(it)
    for line in it:
        if not line:
            idx += 1
            next(it)
        else:
            res[idx].append(int(line))
    return res


def _calc_score(d: deque):
    return sum(map(mul, reversed(d), range(1, len(d) + 1)))


def part1():
    decks = _parse_data()
    while all(decks):
        cards = tuple(map(deque.popleft, decks))
        decks[lt(*cards)].extend(sorted(cards, reverse=True))
    return _calc_score(next(filter(bool, decks)))


def part2():
    def _weirdo_game(*decks):
        seen = set()
        d1, d2 = decks
        while all(decks):
            ts = tuple(d1), tuple(d2)
            if ts in seen:
                return 0, d1

            seen.add(ts)
            c1, c2 = d1.popleft(), d2.popleft()

            if len(d1) >= c1 and len(d2) >= c2:
                winner, _ = _weirdo_game(deque(take(c1, d1)), deque(take(c2, d2)))
            else:
                winner = c1 < c2

            decks[winner].extend((c2, c1) if winner else (c1, c2))
        return bool(d2), decks[bool(d2)]

    _, d = _weirdo_game(*_parse_data())
    return _calc_score(d)


@timer
def __main():
    print(part1())
    print(part2())


# 32489
# 35676
# '__main' took 1.616337866 seconds

if __name__ == '__main__':
    __main()
