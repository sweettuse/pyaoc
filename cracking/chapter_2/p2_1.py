__author__ = 'acushner'

from cracking.chapter_2 import Node


# 2.1 Remove Dups! Write code to remove duplicates from an unsorted linked list.
# FOLLOW UP
# How would you solve this problem if a temporary buffer is not allowed?
# Hints: #9, #40

def rm_dups(head: Node):
    seen = set()
    prev = head
    for cur in head:
        if cur.val in seen:
            prev.rm_next()
        else:
            seen.add(cur.val)
            prev = cur


def rm_dups_no_buff(head: Node):
    for n in head:
        if not n.next:
            break

        target = n.val
        prev = n
        for cur in n.next:
            if cur.val == target:
                prev.rm_next()
            else:
                prev = cur


def __main():
    l = [2, 1, 1, 2, 3, 1, 2, 5]
    head = Node.from_iter(l)
    head.display()
    rm_dups(head)
    head.display()


if __name__ == '__main__':
    __main()
