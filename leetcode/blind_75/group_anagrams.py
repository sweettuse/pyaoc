__author__ = 'acushner'

from typing import List
from collections import defaultdict

# https://leetcode.com/problems/group-anagrams/


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        for s in strs:
            res[str(sorted(s))].append(s)
        return list(res.values())


def __main():
    pass


if __name__ == '__main__':
    __main()
