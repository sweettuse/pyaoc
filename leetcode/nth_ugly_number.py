__author__ = 'acushner'

from heapq import heappop, heappush
from itertools import count

from pyaoc2019.utils import timer


def _gen_uglies():
    heap = [1]
    seen = set()
    for i in count(1):
        cur = heappop(heap)
        t = yield cur
        if t:
            print(len(seen), len(heap))
        for u in 2, 3, 5:
            potential = cur * u
            if potential in seen:
                continue
            seen.add(potential)
            heappush(heap, potential)

        # if not i % 100000:
        #     seen = {v for v in seen if v >= heap[0]}


@timer
def nth_ugly_number(n):
    uglies = _gen_uglies()
    for _ in range(n - 1):
        next(uglies)

    return uglies.send(1)
    return next(uglies)


def __main():
    print(nth_ugly_number(9999999))
    pass


if __name__ == '__main__':
    __main()
