__author__ = 'acushner'


# https://leetcode.com/problems/kth-smallest-element-in-a-bst/


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def traverse_orig(n: TreeNode):
    """in order"""

    stack = []
    while n:
        stack.append(n)
        n = n.left

    while stack:
        n = stack.pop()
        yield n
        yield from traverse(n.right)


def traverse(n: TreeNode):
    """in order"""
    if n.left:
        yield from traverse(n.left)
    yield n
    if n.right:
        yield from traverse(n.right)


class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        t = traverse(root)
        for _ in range(k):
            next(t)
        return next(t)


def __main():
    pass


if __name__ == '__main__':
    __main()
