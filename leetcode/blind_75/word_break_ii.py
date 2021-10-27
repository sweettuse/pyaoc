__author__ = 'acushner'

# https://leetcode.com/problems/word-break-ii/
from functools import lru_cache
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)

        @lru_cache(None)
        def break_words(s: str) -> List[List[str]]:
            if not s:
                return [[]]

            res = []
            for w in words:
                if s.startswith(w):
                    res.extend([w] + r for r in break_words(s[len(w):]))
            return res

        return [' '.join(l) for l in break_words(s)]


class Solution2:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)

        @lru_cache(None)
        def break_words(s: str) -> List[List[str]]:
            if not s:
                return [[]]

            res = []
            for i in range(1, len(s) + 1):
                if (w := s[:i]) in words:
                    res.extend([w] + r for r in break_words(s[i:]))
            return res

        return [' '.join(l) for l in break_words(s)]


def __main():
    s = "catsanddog"
    wordDict = ["cat", "cats", "and", "sand", "dog"]
    # Output: ["cats and dog", "cat sand dog"]
    print(Solution2().wordBreak(s, wordDict))
    s = "pineapplepenapple"
    wordDict = ["apple", "pen", "applepen", "pine", "pineapple"]
    print(Solution().wordBreak(s, wordDict))

    pass


if __name__ == '__main__':
    __main()
