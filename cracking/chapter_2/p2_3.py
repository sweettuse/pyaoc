__author__ = 'acushner'

# 2.3 Delete Middle Node: Implement an algorithm to delete a node in the middle (i.e., any node but
# the first and last node, not necessarily the exact middle) of a singly linked list, given only access to
# that node.
from cracking.chapter_2 import Node


def del_mid_node(head: Node):
    if (num_elts := len(head)) <= 2:
        return
    ante_mid = (num_elts - 1) // 2
    # n = head
    # for _ in range(ante_mid - 1):
    #     n = n.next
    for n, _ in zip(head, range(ante_mid)):
        pass
    n.rm_next()


def __main():
    n = Node.from_iter('ABCDE')
    n.display()
    del_mid_node(n)
    n.display()
    pass


if __name__ == '__main__':
    __main()
