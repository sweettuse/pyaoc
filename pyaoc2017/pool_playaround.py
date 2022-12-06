import time

from concurrent.futures.process import ProcessPoolExecutor
from cluegen import Datum, FrozenDatum

__author__ = 'acushner'


class A:
    def to_map(self, n):
        time.sleep(n)
        return n

    def run(self):
        pool = ProcessPoolExecutor(4)
        print(list(pool.map(self.to_map, range(10))))


def __main():
    class D(FrozenDatum):
        a: int
        b: int

    d = D(1, 2)
    print(d)
    t = {d}
    print(t)
    del d.a
    print(d)
    t.add(D(1, 2))
    print(t)
    pass


if __name__ == '__main__':
    __main()
