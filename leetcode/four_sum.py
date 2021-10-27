__author__ = 'acushner'

# https://leetcode.com/problems/4sum/
from collections import Counter
from itertools import combinations


def _compress(nums):
    c = Counter(nums)
    return Counter({k: min(4, v) for k, v in c.items()})


def four_sum(nums, target):
    c = _compress(nums)
    nums = [n for n, times in c.items() for _ in range(times)]
    res = set()

    def _validate_and_add(num_i, num_j, num_k):
        n = target - (num_i + num_j + num_k)

        if n not in c:
            return

        t = tuple(sorted((num_i, num_j, num_k, n)))
        cur_c = Counter(t)
        if (cur_c & c) == cur_c:
            res.add(t)

    for i, j, k in combinations(nums, 3):
        _validate_and_add(i, j, k)

    return res


def __main():
    print('wth')
    print(four_sum([1, 0, -1, 0, -2, 2], 0))
    nums = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
            2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    target = 8
    print(four_sum(nums, target))

    pass


if __name__ == '__main__':
    __main()
