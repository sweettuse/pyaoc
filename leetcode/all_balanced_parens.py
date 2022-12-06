# https://www.codewars.com/kata/5426d7a2c2c7784365000783/train/python

from functools import cache


def balanced_parens(n) -> list[str]:
    res: set[tuple[str, ...]] = set()
    @cache
    def helper(nleft=n, nright=n, cur: tuple[str, ...] = ()):
        if nleft + nright == 0:
            res.add(cur)
            return
        
        if nleft:
            helper(nleft - 1, nright, cur + ('(',))
        if nright > nleft:
            helper(nleft, nright - 1, cur + (')',))
        
        
    helper(n, n)
    return [''.join(t) for t in res]


print(balanced_parens(3))

