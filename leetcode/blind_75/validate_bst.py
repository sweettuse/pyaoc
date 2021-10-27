__author__ = 'acushner'

# https://leetcode.com/problems/validate-binary-search-tree/

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def _traverse(n: TreeNode):
    if n is not None:
        yield from _traverse(n.left)
        yield n
        yield from _traverse(n.right)


class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        cur = float('-inf')
        for v in _traverse(root):
            if cur >= v.val:
                return False
            cur = v.val
        return True


def __main():
    pass


if __name__ == '__main__':
    __main()
