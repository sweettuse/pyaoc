__author__ = 'acushner'

import sys
from collections import defaultdict, Counter
from functools import lru_cache, partial
from itertools import chain, islice, groupby, accumulate, tee, permutations, combinations
from typing import NamedTuple, Optional

from pyaoc2019.utils import timer


def min_cost(costs):
    """https://leetcode.com/problems/min-cost-climbing-stairs/"""
    tab = [float('inf')] * (len(costs) + 1)
    costs = costs + [0]
    tab[0] = costs[0]
    tab[1] = costs[1]
    for i in range(2, len(costs)):
        tab[i] = min(tab[0], tab[1]) + costs[i]

    return tab


def min_cost2(costs):
    """https://leetcode.com/problems/min-cost-climbing-stairs/"""
    costs = costs + [0]

    @lru_cache(None)
    def _min_cost(idx=len(costs) - 1):
        if idx < 0:
            return 0
        return costs[idx] + min(_min_cost(idx - 1), _min_cost(idx - 2))

    return _min_cost()


def min_cost3(costs):
    costs = costs + [0]
    tab = [float('inf')] * (len(costs) + 1)
    tab[0] = 0
    for i, c in enumerate(tab):
        if i + 1 <= len(costs):
            tab[i + 1] = min(tab[i + 1], c + costs[i])
        if i + 2 <= len(costs):
            tab[i + 2] = min(tab[i + 2], c + costs[i + 1])
    return tab[-1]


def arithmetic_slices(nums):
    """https://leetcode.com/problems/arithmetic-slices/"""
    if len(nums) < 3:
        return 0

    diffs = [n2 - n1 for n1, n2 in zip(nums, islice(nums, 1, None))]

    def _calc_num_subs(n):
        n = n - 1
        if n < 1:
            return 0
        return n * (n + 1) // 2

    total = 0
    for _, vals in groupby(diffs):
        total += _calc_num_subs(sum(1 for _ in vals))
    return total


def max_product_subarray_orig(nums):
    """https://leetcode.com/problems/maximum-product-subarray/"""
    best = float('-inf') if 0 not in nums else 0

    def _add(start, i):
        tmp = nums[start:i]
        if tmp:
            groups.append(tmp)

    groups = []
    start = 0
    for i, v in enumerate(nums):
        if not v:
            _add(start, i)
            start = i + 1
    _add(start, None)

    def _process_group(g):
        negs = [i for i, v in enumerate(g) if v < 0]

    return groups


def max_product_subarray(nums):
    """https://leetcode.com/problems/maximum-product-subarray/"""
    cur_max = cur_min = res = nums[0]
    for v in islice(nums, 1, None):
        vals = v, cur_max * v, cur_min * v
        cur_max = max(vals)
        cur_min = min(vals)
        res = max(res, cur_max)
    return res


def max_subarray(nums):
    t, for_mins = tee(accumulate(nums))
    mins = accumulate(for_mins, min, initial=0)
    return max((n - mn for n, mn in zip(t, mins)), default=nums[0])


def max_turbulent(nums):
    """https://leetcode.com/problems/longest-turbulent-subarray/"""
    if not nums:
        return

    if len(nums) == 1:
        return 1

    def _get_comp():
        if n1 == n2:
            return 0
        if n1 < n2:
            return -1
        return 1

    res = []
    for n1, n2 in zip(nums, islice(nums, 1, None)):
        res.append(_get_comp())
    print([0] + res)

    prev_comp = 0
    streak = 0
    max_streak = 0
    for n1, n2 in zip(nums, islice(nums, 1, None)):
        cur_comp = _get_comp()
        if cur_comp == 0:
            streak = 0
        elif prev_comp == 0 or cur_comp == prev_comp:
            streak = 1
        else:
            streak += 1
        prev_comp = cur_comp
        max_streak = max(max_streak, streak)

    return max_streak + 1


def unique_paths2(grid):
    """https://leetcode.com/problems/unique-paths-ii/
    down/right movement with obstacles
    """
    num_r = len(grid)
    num_c = len(grid[0])
    tab = [[0] * (num_c + 1) for _ in range(num_r + 1)]
    tab[1][1] = 1

    for r_idx, r in enumerate(grid):
        for c_idx, v in enumerate(r):
            if v:
                tab[r_idx + 1][c_idx + 1] = None

    def _get_val(r, c):
        val = tab[r][c]
        return 0 if val is None else val

    for r in range(1, num_r + 1):
        for c in range(1, num_c + 1):
            cur = tab[r][c]
            if cur is None:
                continue
            tab[r][c] += _get_val(r - 1, c) + _get_val(r, c - 1)

    return tab[-1][-1] or 0


def unique_paths2_rec(grid):
    """https://leetcode.com/problems/unique-paths-ii/
    down/right movement with obstacles
    """
    num_rows = len(grid)
    num_cols = len(grid[0])

    @lru_cache(None)
    def _paths(r=num_rows - 1, c=num_cols - 1):
        if r < 0 or c < 0:
            return 0

        if grid[r][c]:
            return 0

        if r == c == 0:
            return 1

        return _paths(r - 1, c) + _paths(r, c - 1)

    return _paths()


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


@timer
def num_unique_bsts2(n):
    """https://leetcode.com/problems/unique-binary-search-trees-ii/"""

    # return len(list(permutations(range(1, n + 1))))
    @lru_cache(None)
    def _trees(n=n) -> int:
        if n <= 1:
            return 1
        if n == 2:
            return 2

        return sum(_trees(left) * _trees(n - left - 1) for left in range(n))

    try:
        return _trees()
    finally:
        print(_trees.cache_info())

    # this is gonna be a great way to code.
    # maybe this is the height i want. we'll try this for now, let's see.


@timer
def longest_string_chain(words):
    """https://leetcode.com/problems/longest-string-chain/"""
    len_word = defaultdict(set)
    for w in words:
        len_word[len(w)].add(w)

    def _is_successor(w1, w2):
        assert len(w2) == len(w1) + 1, 'you passing in bad words, dummy'
        i = j = 0
        for _ in range(len(w2)):
            if i == len(w1):
                return True

            if w1[i] == w2[j]:
                i += 1
                j += 1
            else:
                if j != i:
                    return False
                j += 1
        return True

    @lru_cache(None)
    def _longest_chain(w) -> int:
        possible = len_word.get(len(w) + 1, set())
        successors = filter(partial(_is_successor, w), possible)
        return 1 + max(map(_longest_chain, successors), default=0)

    return max(map(_longest_chain, words))


@timer
def longestStrChain(words) -> int:
    words = set(words)

    @lru_cache(None)
    def chain(word):
        potentials = (word[:i] + word[i + 1:] for i in range(len(word)))
        preds = filter(words.__contains__, potentials)
        return 1 + max(map(chain, preds), default=0)

    return max(map(chain, words), default=0)


def push_dominoes(dominoes):
    forces = [(i, v) for i, v in enumerate(dominoes) if v != '.']
    if not forces:
        return dominoes

    res = list(dominoes)
    for (li, lf), (ri, rf) in zip(forces, forces[1:]):
        if lf == 'L' and rf == 'R':
            continue

        if lf == rf:
            res[li + 1: ri] = lf * (ri - li - 1)
        else:
            to_fill = (ri - li - 1) // 2
            res[li + 1: li + to_fill + 1] = 'R' * to_fill
            res[ri - to_fill: ri] = 'L' * to_fill

    li, lf = forces[0]
    if lf == 'L':
        res[:li] = 'L' * li

    ri, rf = forces[-1]
    if rf == 'R':
        res[ri + 1:] = 'R' * (len(res) - ri - 1)
    return ''.join(res)


def min_stickers(stickers: list[str], target: str):
    """https://leetcode.com/problems/stickers-to-spell-word/"""
    s_target = set(target)

    @lru_cache(None)
    def counter(w):
        return Counter(w)

    def get_subword(w1, w2) -> Optional[str]:
        """
        word that is covered by another word, e.g. "jeb" is covered by "jebp"
        return subword if any, else None
        """
        w12diff = counter(w1) - counter(w2)
        w21diff = counter(w2) - counter(w1)

        if w12diff and not w21diff:
            return w2
        elif w21diff and not w12diff:
            return w1

    def reduce_stickers(stickers):
        stickers = [''.join(c for c in w if c in s_target) for w in stickers]
        subwords = (get_subword(*words) for words in combinations(stickers, 2))
        to_exclude = set(filter(bool, subwords))
        return set(stickers) - to_exclude

    stickers = reduce_stickers(stickers)

    if set(chain.from_iterable(stickers)) < s_target:
        return -1

    class CountStr(NamedTuple):
        count: int
        s: str

    min_s = float('inf')
    letter_to_count_str = defaultdict(list)
    target_count = Counter(target)
    for sticker in stickers:
        for c, num in Counter(sticker).items():
            if c in target_count:
                letter_to_count_str[c].append(CountStr(num, sticker))

    for v in letter_to_count_str.values():
        v.sort(key=lambda cs: (cs.count, len(cs.s)), reverse=True)

    return letter_to_count_str


def __main():
    # costs = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
    costs = [10, 15, 20]
    print(min_cost2(costs))
    print(min_cost3(costs))
    nums = [1]
    print(arithmetic_slices(nums))
    nums = [2, 12, -2, 4, 0, 6]
    print(max_product_subarray(nums))
    nums = [-1]
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    nums = [5, 4, -1, 7, 8]
    print(max_subarray(nums))
    print('=================')
    # nums = [9, 4, 2, 10, 7, 8, 8, 1, 9]
    # nums = [4, 8, 12, 16]
    nums = [9, 9]
    nums = [2, 0, 2, 4, 2, 5, 0, 1, 2, 3]
    print(max_turbulent(nums))
    print('==================')
    # grid = [[0, 1], [0, 0]]
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(unique_paths2(grid))
    print(unique_paths2_rec(grid))
    print('=================')
    print(num_unique_bsts2(30))
    print('=================')
    words = ["a", "b", "ba", "bca", "bda", "bdca"]
    words.extend(map(''.join, permutations('abcd')))
    words.extend(map(''.join, permutations('abcde')))
    words.extend(map(''.join, permutations('abcdef')))
    words.extend(map(''.join, permutations('abcdefg')))
    # print(words)
    # words = ["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"]
    # words = ["abcd", "dbqca"]
    # print(longest_string_chain(words))
    print(longestStrChain(words))
    print('=================')
    ds = ".L.R...LR..L.."
    ds = 'R....L'
    ds = '.L..R.'
    print(push_dominoes(ds))
    print('=================')
    stickers = 'with example science'.split()
    target = 'thehat'
    print(min_stickers(stickers, target))
    print(min_stickers(['jeb', 'jebe', 'jebp'], 'tuse'))


if __name__ == '__main__':
    __main()
