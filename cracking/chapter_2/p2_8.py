__author__ = 'acushner'

# 2.8 Loop Detection: Given a circular linked list, implement an algorithm that returns the node at the
# beginning of the loop.
# DEFINITION
# Circular linked list: A (corrupt) linked list in which a node's next pointer points to an earlier node, so
# as to make a loop in the linked list.
# EXAMPLE
# Input: A -> B -> C -> D -> E -> C [the same C as earlier]
# Output: C
# Hints: #50, #69, #83, #90
from cracking.chapter_2 import Node


def _get_arbitrary_loop_node(head: Node):
    slow, fast = head, head.next
    try:
        while True:
            if slow is fast:
                return slow
            slow = slow.next
            fast = fast.next.next
    except AttributeError:
        return


def _in_loop(target: Node, loop: Node):
    sentinel = loop

    for n in loop.next:
        if target is n:
            return True
        if n is sentinel:
            return False


def get_beginning_of_loop(head: Node):
    if not (loop_node := _get_arbitrary_loop_node(head)):
        return

    print(loop_node)
    for n in head:
        if _in_loop(n, loop_node):
            return n


def __main():
    n = Node.from_iter('ABCDEFGH')
    for last in n:
        pass
    last.next = n
    print(get_beginning_of_loop(n))

# num_nodes = k


if __name__ == '__main__':
    __main()
