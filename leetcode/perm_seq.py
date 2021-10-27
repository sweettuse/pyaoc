__author__ = 'acushner'

from itertools import accumulate, permutations
from operator import mul


# https://leetcode.com/problems/permutation-sequence/

def _factorials(n):
    res = list(accumulate(range(1, n + 1), mul))
    res.reverse()
    return res


def _perms(n):
    for i, v in enumerate(permutations(range(1, n + 1)), 1):
        print(i, v)


def kth_perm(n, k):
    k -= 1
    fs = _factorials(n - 1)
    res = []
    nums = list(range(1, n + 1))

    def _helper(f_idx=0, k=k):
        if f_idx >= len(fs):
            return

        cur_idx, new_k = divmod(k, fs[f_idx])
        res.append(nums[cur_idx])
        nums.remove(nums[cur_idx])
        _helper(f_idx + 1, new_k)

    _helper()
    if nums:
        res.append(nums[0])
    return ''.join(map(str, res))


def __main():
    n = 3
    for k in range(1, 7):
        print(k, n, kth_perm(n, k))
    print(kth_perm(4, 9))
    print(kth_perm(3, 1))
    print('==============')
    return _perms(n)


if __name__ == '__main__':
    __main()
