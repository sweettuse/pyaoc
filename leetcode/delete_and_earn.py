__author__ = 'acushner'

# https://leetcode.com/problems/delete-and-earn/
from collections import Counter
import random
from itertools import groupby
from operator import itemgetter


def delete_and_earn(nums):
    nums.sort()
    totals = {k: sum(vals) for k, vals in groupby(nums)}

    return totals
    c = Counter(nums)
    print(c)
    value = Counter({n: times * n for n, times in c.items()})
    print(value)
    total2 = {n: n_total - value[n - 1] - value[n + 1] for n, n_total in value.items()}
    total2 = dict(sorted(total2.items(), reverse=True, key=itemgetter(1)))
    return total2


def __main():
    random.seed(517)
    nums = [random.randrange(1, 10) for _ in range(15)]
    # nums = [2,2,3,3,3,4]
    print(delete_and_earn(nums))
    pass


if __name__ == '__main__':
    __main()
