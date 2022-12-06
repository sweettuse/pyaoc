from __future__ import annotations
from itertools import repeat, chain
from rich import print


def josephus(n: int):
    """check the numberphile vid on this"""
    l = n.bit_length() - 1
    mask = 2 ** l - 1
    return 2 * (n & mask) + 1



def josephus_new_brute(n: int):
    l = list(range(1, n + 1))
    cur_idx = 0
    for _ in range(n - 1):
        cur_val = l[cur_idx]
        opp = (cur_idx + len(l) // 2) % len(l)
        l.pop(opp)
        cur_idx = (l.index(cur_val) + 1) % len(l)

    return l[0]


def highest_power_of_3(n):
    cur = 3
    while (nxt := cur * 3) <= n:
        cur = nxt
    return cur

def josephus_new(n: int):
    h3 = highest_power_of_3(n)
    if n == h3:
        return n
    diff = n - h3
    return min(diff, h3) + max(0, diff - h3) * 2


def _test():
    print(josephus_new_brute(5))
    # l = list(range(4))

    def base3(n: int) -> str:
        res = []
        while n:
            n, rem = divmod(n, 3)
            res.append(rem)
        return ''.join(map(str, reversed(res)))

    print(highest_power_of_3(27))
    print(highest_power_of_3(28))
    print(highest_power_of_3(80))
    print(highest_power_of_3(82))


    for i in range(2000, 2500):
        assert josephus_new(i) == josephus_new_brute(i)


def __main():
    _test()
    print(josephus(3014387))
    print(josephus_new(3014387))

__main()
# for n in range(1, 82):
#     jn = josephus_new_brute(n)
#     print(n, jn, base3(n), base3(jn))
    



