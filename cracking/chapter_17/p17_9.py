__author__ = 'acushner'

# 17 .9 Kth Multiple: Design an algorithm to find the kth number such that the only prime factors are 3, 5,
# and 7. Note that 3, 5, and 7 do not have to be factors, but it should not have any other prime factors.
# For example, the first several multiples would be (in order) 1, 3, 5, 7, 9, 15, 21.
# Hints:#488,#508,#550,#591,#622,#660,#686
from collections import deque
from heapq import heapify, heappop, heappush

from pyaoc2019.utils import timer, localtimer


def _yield_mults():
    """broken, see `_yield_mults3` for correct solution"""
    seen = set()
    vals = [1, 3, 5, 7]
    mults = 3, 5, 7
    heapify(vals)

    # @timer
    def _update_with_new_vals():
        new = {cur for s in seen for m in mults if (cur := s * m) not in seen}
        vals.extend(new)
        heapify(vals)
        seen.clear()

    while True:
        if not vals:
            _update_with_new_vals()
        t = heappop(vals)
        seen.add(t)
        yield t


def get_kth(k):
    mults = _yield_mults()
    res = None
    for _ in range(k):
        res = next(mults)
    return res


def kth_multiple(k: int):
    seq = [1]
    q3 = deque()
    q5 = deque()
    q7 = deque()

    def pop_min(cur, q3, q5, q7):
        # remove any dupes that may have already been chosen
        for q in (q3, q5, q7):
            if q[0] <= cur:
                q.popleft()

        n = min(q3[0], q5[0], q7[0])
        for q in (q3, q5, q7):
            if n == q[0]:
                q.popleft()

        return n

    while len(seq) < k:
        cur = seq[-1]
        q3.append(cur * 3)
        q5.append(cur * 5)
        q7.append(cur * 7)
        seq.append(pop_min(cur, q3, q5, q7))

    return seq[-1], seq


def kth_multiple2(k: int):
    seq = [1]
    deques = deque(), deque(), deque()

    def pop_min(cur, q3, q5, q7):
        # remove any dupes that may have already been chosen
        for q in (q3, q5, q7):
            if q[0] <= cur:
                q.popleft()

        n = min(q3[0], q5[0], q7[0])
        for q in (q3, q5, q7):
            if n == q[0]:
                q.popleft()

        return n

    while len(seq) < k:
        cur = seq[-1]
        q3.append(cur * 3)
        q5.append(cur * 5)
        q7.append(cur * 7)
        seq.append(pop_min(cur, q3, q5, q7))

    return seq[-1], seq


def _yield_mults3():
    vals = [1]
    mults = 3, 5, 7

    prev = float('-inf')
    while True:
        cur = heappop(vals)
        if cur <= prev:
            continue
        prev = cur
        yield cur
        for m in mults:
            heappush(vals, m * cur)


# @timer
def __main():
    size = 4500
    # with localtimer():
    #     r1 = take(size, _yield_mults2())
    with localtimer():
        ym3 = _yield_mults3()
        for _ in range(size):
            r2 = next(ym3)
    print(r2)
    return
    # print(get_kth(5))
    # return
    t = _yield_mults2()
    res = []
    for _ in range(1000):
        res.append(next(t))
    for i, (v1, v2) in enumerate(zip(kth_multiple(1000)[1], res)):
        if v1 != v2:
            print(i, v1, v2)
    # print(kth_multiple(100))
    # print(res)


if __name__ == '__main__':
    __main()
