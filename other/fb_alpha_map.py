__author__ = 'acushner'

import string
from copy import copy
from functools import lru_cache
from typing import List, Iterator, Optional

s = '12432111'
s = '1243'
s = '123'

# abc
# lc
# aw

num_char_map = dict(zip(range(1, 27), string.ascii_lowercase))


def decode(s):
    def _helper(ints: Iterator[int]) -> Optional[List[List[int]]]:
        res = [[]]
        try:
            prev = next(ints)
        except StopIteration:
            return res

        for cur in ints:
            comb = 10 * prev + cur
            if comb <= 26:
                for r in _helper(copy(ints)):
                    res.append([*res[0], comb, *r])
            res[0].append(prev)
            prev = cur

        res[0].append(prev)
        return res

    ints = [int(i) for i in s]
    res = _helper(iter(ints))
    print(len(res))
    return {''.join(map(num_char_map.get, r)) for r in res}


# def decode(s):
#     @lru_cache(None)
#     def _helper(idx: int):
#         if idx > len(s):
#             return
#         if idx == len(s):
#             return int(s[idx])
#
#         res = []
#         if (cur := int(s[idx: idx + 2])) <= 26:
#             res.append(cur)
#         res.append


# def decode(s):
#     def _helper(ints: Iterator[int]) -> Optional[List[List[int]]]:
#         res = [[], []]
#         try:
#             prev = next(ints)
#         except StopIteration:
#             return res
#
#         for cur in ints:
#             comb = 10 * prev + cur
#             print(comb)
#             if comb <= 26:
#                 res[1].append(([*res[0], comb], _helper(copy(ints))))
#             res[0].append(prev)
#             prev = cur
#         res[0].append(prev)
#         return res
#
#     ints = [int(i) for i in s]
#     print(ints)
#     return _helper(iter(ints))


def __main():
    res = decode('12342121')
    print(len(res))
    print(res)
    pass


if __name__ == '__main__':
    __main()
