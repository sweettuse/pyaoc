__author__ = 'acushner'

# 4.5 Validate BST: Implement a function to check if a binary tree is a binary search tree.
# Hints: #35, #57, #86, #113, #128
from cracking.chapter_4 import BNode
from cracking.chapter_4.p4_2 import short_tree
from cracking.chapter_4.p4_4 import is_balanced


def is_valid_bst(n: BNode):
    def _is_valid_bst(n, left_bound=float('-inf'), right_bound=float('inf')):
        if not n:
            return True
        return (left_bound < n.v < right_bound
                and _is_valid_bst(n.left, left_bound, n.v)
                and _is_valid_bst(n.right, n.v, right_bound))

    return _is_valid_bst(n) and is_balanced(n)


def __main():
    n = short_tree(list(range(15)))
    print(is_valid_bst(n))
    end = BNode(21, BNode(22))
    n.left.left.left.left = end
    print(is_valid_bst(n))
    pass


if __name__ == '__main__':
    __main()
