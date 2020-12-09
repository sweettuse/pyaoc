from collections import deque

__author__ = 'acushner'

from pyaoc2019.utils import SliceableDeque, read_file, exhaust, timer

data = deque(range(10007))


def deal_into(deck):
    return deque(reversed(deck))


def cut(deck, n):
    n %= len(deck)
    deck.rotate(-n)
    return deck


def increment(deck, n):
    res = len(deck) * [None]
    for i, card in enumerate(deck):
        res[(i * n) % len(deck)] = card
    return deque(res)


def parse_data(fname=22):
    def _parse(l):
        if 'cut' in l:
            return cut, int(l.split()[-1])
        if 'increment' in l:
            return increment, int(l.split()[-1])
        return deal_into,

    return list(map(_parse, read_file(fname, 2019)))


print(parse_data())

d = deque(range(10))
print(cut(d, -4))


def part1():
    deck = deque(range(10007))
    for f, *args in parse_data(22):
        deck = f(deck, *args)
    return deck.index(2019)

def part2():
    deck = deque(range(119315717514047))
    for f, *args in parse_data('22.test'):
        deck = f(deck, *args)
    print(len(deck))


@timer
def __main():
    print(part1())
    print(part2())
    pass


if __name__ == '__main__':
    __main()
