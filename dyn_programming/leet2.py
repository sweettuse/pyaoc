__author__ = 'acushner'

from collections import defaultdict
from functools import wraps, lru_cache
from itertools import accumulate, islice

from pyaoc2019.utils import exhaust, timer


def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__.center(30, '='))
        res = func(*args, **kwargs)
        print(res)
        return res

    return wrapper


@debug
def min_distance(w1, w2):
    """https://leetcode.com/problems/delete-operation-for-two-strings/"""
    # longest subsequence
    m, n = len(w1), len(w2)
    tab = [[0] * (m + 1) for _ in range(n + 1)]
    for i, c2 in enumerate(w2, 1):
        for j, c1 in enumerate(w1, 1):
            if c1 == c2:
                tab[i][j] = 1 + tab[i - 1][j - 1]
            else:
                tab[i][j] = max(tab[i - 1][j], tab[i][j - 1])

    return tab[-1][-1]


@timer
@debug
def two_keys_keyboard(n):
    """https://leetcode.com/problems/2-keys-keyboard/"""
    # 1 -> 0
    # 2 -> 2
    # 3 -> 3
    # 4 -> 4
    # 5 -> 5
    # store target -> {cur_buffer -> total_steps}
    tab = [defaultdict(lambda: float('inf')) for _ in range(n + 1)]
    tab[0][0] = 0
    tab[1][0] = 0
    for i in range(2, n + 1):
        cur = tab[i]
        for j in range(1, i):
            prev = tab[j]
            for buffer, steps in prev.items():
                if buffer:
                    add, rem = divmod(n, buffer)
                    if not rem:
                        cur[buffer] = min(cur[buffer], steps + add)
            add, rem = divmod(i - j, j)
            if not rem:
                cur[j] = min(cur[j], 1 + min(prev.values()) + add)
    return min(tab[-1].values())


@timer
def two_keys_keyboard2(n):
    """https://leetcode.com/problems/2-keys-keyboard/"""
    # 1 -> 0
    # 2 -> 2
    # 3 -> 3
    # 4 -> 4
    # 5 -> 5
    # store target -> {cur_buffer -> total_steps}
    tab = [defaultdict(lambda: float('inf')) for _ in range(n + 1)]
    tab[0][0] = 0
    tab[1][0] = 0
    for i in range(2, n + 1):
        cur = tab[i]
        for j in range(1, i):
            prev = tab[j]
            for buffer, steps in prev.items():
                if not buffer:
                    continue
                if not n % buffer:
                    cur[buffer] = min(cur[buffer], steps + n // buffer)

            if not (i - j) % j:
                cur[j] = min(cur[j], 1 + min(prev.values()) + (i - j) // j)
    return min(tab[-1].values())


@debug
def largest_sum_avg(nums, k):
    """https://leetcode.com/problems/largest-sum-of-averages/"""
    nums = [0] + list(accumulate(nums))
    tab = [[0] * (len(nums)) for _ in range(k)]

    mean = lambda left, right: (nums[right] - nums[left]) / (right - left)
    for i in range(1, len(nums)):
        tab[0][i] = mean(0, i)

    for r in range(1, k):
        for c in range(r + 1, len(nums) - k + r + 1):
            tab[r][c] = max(tab[r - 1][i] + mean(i, c) for i in range(r - 1, c))

    return tab[-1][-1]


@debug
def coin_change2(amount, coins):
    """https://leetcode.com/problems/coin-change-2/"""
    tab = [0] * (amount + 1)
    tab[0] = 1
    for c in coins:
        for i, v in enumerate(tab):
            if i + c > amount:
                break
            tab[i + c] += tab[i]
    return tab[-1]


@debug
def coin_change_2_2(amount, coins):
    @lru_cache(None)
    def _change(cur=amount):
        pass

    return _change()


@debug
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for i in coins:
        for j in range(1, amount + 1):
            if j >= i:
                dp[j] += dp[j - i]
    return dp[amount]


@debug
def tribonacci(n):
    """https://leetcode.com/problems/n-th-tribonacci-number/"""
    nums = a, b, c = 0, 1, 1
    if n <= 2:
        return nums[n]
    for _ in range(2, n):
        a, b, c = b, c, a + b + c
    return c


def __main():
    min_distance('leetcode', 'etco')
    nums = [9, 1, 2, 3, 9]
    k = 3
    nums = [1, 2, 3, 4, 5, 6, 7]
    k = 4
    largest_sum_avg(nums, k)
    coin_change2(5, [1, 2, 5])
    # coin_change2(10, [10])
    # coin_change2(3, [2])
    # coin_change2(5, [1, 2, 5])
    change(5, [1, 2, 5])
    tribonacci(25)
    pass


if __name__ == '__main__':
    __main()
