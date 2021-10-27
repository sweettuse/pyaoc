__author__ = 'acushner'

# https://leetcode.com/problems/climbing-stairs/

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        prev2, prev1 = 1, 2
        for i in range(3, n + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1



def __main():
    print(Solution().climbStairs(3))
    print(Solution().climbStairs(4))
    pass


if __name__ == '__main__':
    __main()
