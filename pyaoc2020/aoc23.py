from itertools import chain

from pyaoc2019.utils import timer, SliceableDeque

__author__ = 'acushner'

cups = SliceableDeque(map(int, '872495136'))


# cups = SliceableDeque(map(int, '389125467'))


def part1(cups=cups, n=100):
    num_cups = len(cups)
    orig_cups = list(cups)

    def _calc_dest():
        v = cups[-1] - 1
        if v == 0:
            v = num_cups
        while v in pickup:
            v -= 1
            if v == 0:
                v = 9
        return v

    for _ in range(n):
        cups.rotate(-1)
        pickup = cups[:3]
        cups[:3] = []
        dest = _calc_dest()
        ins = cups.index(dest)
        cups[ins + 1: ins + 1] = pickup
    cups.rotate(-cups.index(1) - 1)
    return ''.join(map(str, cups[:len(cups) - 1]))


def part2():
    many_cups = SliceableDeque(chain(cups, range(10, 1000001)))
    print(len(many_cups))
    part1(many_cups)

    pass


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
