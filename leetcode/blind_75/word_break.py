__author__ = 'acushner'

from functools import lru_cache
from typing import List


# https://leetcode.com/problems/word-break/


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        words = set(wordDict)

        @lru_cache(None)
        def word_break(s: str) -> bool:
            if not s:
                return True

            for i in range(1, len(s) + 1):
                if s[-i:] in words and word_break(s[:-i]):
                    return True

            return False

        return word_break(s)


class Solution2:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        dp = [False] * (len(s) + 1)
        dp[0] = True

        for i in range(1, len(s) + 1):
            for j in range(i):
                print(dp, s[j:i])
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break
        print(dp)
        return dp[len(s)]


def __main():
    print(Solution().wordBreak('jebo', ['jeb']))
    print(Solution2().wordBreak('applepenapple', ['apple', 'pen']))
    print(80 * '=')
    print(Solution().wordBreak('applepenapple', ['apple', 'pen']))


if __name__ == '__main__':
    __main()
