__author__ = 'acushner'


# https://leetcode.com/problems/binary-tree-maximum-path-sum/

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_path_sum(head: TreeNode):
    global_max = float('-inf')

    def _mps(n: TreeNode):
        nonlocal global_max
        left_sum = right_sum = 0

        if n.left:
            left_sum = max(_mps(n.left), 0)

        if n.right:
            right_sum = max(_mps(n.right), 0)

        global_max = max(global_max, n.val + left_sum + right_sum)
        return n.val + max(left_sum, right_sum)

    _mps(head)
    return global_max


def max_path_sum2(head: TreeNode):
    global_max = float('-inf')

    def _mps(n: TreeNode):
        nonlocal global_max
        if not n:
            return 0
        left_sum = max(_mps(n.left), 0)
        right_sum = max(_mps(n.right), 0)

        global_max = max(global_max, n.val + left_sum + right_sum)
        return n.val + max(left_sum, right_sum)

    _mps(head)
    return global_max


def __main():
    head = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    print(max_path_sum2(head))
    pass


if __name__ == '__main__':
    __main()
