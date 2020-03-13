from collections import deque

import pyaoc2019.utils as U

__author__ = 'acushner'

N_STEPS = 312


def spin(n_steps=N_STEPS, size=2017):
    d = deque([0])
    for i in range(1, size + 1):
        d.rotate(-(n_steps % len(d)))
        d.append(i)
    return d


def aoc17_a():
    return spin()[0]


def aoc17_b(size=50_000_000):
    d = spin(size=size)
    return d[d.index(0) + 1]


def __main():
    print(aoc17_a())
    with U.localtimer():
        print(aoc17_b())


if __name__ == '__main__':
    __main()
