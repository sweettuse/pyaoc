__author__ = 'acushner'


# https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
from collections import deque
from itertools import takewhile


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def _find(root, n):
    cur = root
    while True:
        yield cur
        if cur is n:
            break
        if n.val > cur.val:
            cur = cur.right
        else:
            cur = cur.left


class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        to_p = _find(root, p)
        to_q = _find(root, q)
        equals = takewhile(lambda pq: pq[0] is pq[1], zip(to_p, to_q))
        res = deque(equals, maxlen=1)
        return res[0][0]

        # OR

        # prev = None
        # for pn, qn in zip(to_p, to_q):
        #     if pn is not qn:
        #         break
        #     prev = pn
        # return prev


def __main():
    pass


if __name__ == '__main__':
    __main()
