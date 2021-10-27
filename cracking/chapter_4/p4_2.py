__author__ = 'acushner'

# 4.2 Minimal Tree: Given a sorted (increasing order) array with unique integer elements,
# write an algorithm to create a binary search tree with minimal height.
# Hints: #79, #73, #7 76
from cracking.chapter_4 import BNode as Node


def short_tree(l) -> Node:
    if not l:
        return

    mid = len(l) // 2
    return Node(l[mid], short_tree(l[:mid]), short_tree(l[mid + 1:]))


def display(n):
    if not n:
        return
    next_row = []
    if isinstance(n, list):
        for t in n:
            if t:
                print(t, end=' | ')
                next_row.append(t.left)
                next_row.append(t.right)
        print()
    else:
        print(n)
        next_row.append(n.left)
        next_row.append(n.right)
    display(next_row)


def traverse(n: Node):
    if not n:
        return
    yield from traverse(n.left)
    yield n
    yield from traverse(n.right)


def __main():
    n = short_tree(list(range(12)))
    display(n)
    print(list(traverse(n)))
    while n:
        print(n)
        n = n.left
    pass


if __name__ == '__main__':
    __main()
