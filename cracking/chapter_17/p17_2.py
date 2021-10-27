__author__ = 'acushner'

from collections import Counter
from random import random, seed

from pyaoc2019.utils import timer


def shuffle(n=4):
    d = {v: random() for v in range(n)}
    return tuple(sorted(d, key=d.__getitem__))


@timer
def __main():
    seed()
    res = Counter(shuffle(4) for _ in range(100000000))
    total = sum(res.values())
    for v, t in res.items():
        print(v, t / total)


if __name__ == '__main__':
    __main()
