__author__ = 'acushner'


# 17.12 BiNode: Consider a simple data structure called BiNode, which has pointers to two other nodes.
# public class BiNode {
# }
# public BiNode nodel, node2;
# public int data;
# The data structure BiNode could be used to represent both a binary tree (where nodel is the left
# node and node2 is the right node) or a doubly linked list (where nodel is the previous node and
# node2 is the next node). Implement a method to convert a binary search tree (implemented with
# BiNode) into a doubly linked list. The values should be kept in order and the operation should be
# performed in place (that is, on the original data structure).
# Hints: #509, #608, #646, #680, #707, #779

class BiNode:
    def __init__(self, data):
        self.data = data
        self.node1 = None
        self.node2 = None

    def in_order(self):
        if self.node1:
            yield from self.node1.in_order()
        yield self
        if self.node2:
            yield from self.node2.in_order()

    def __str__(self):
        return f'BiNode({self.data})'


def to_double_ll(head: BiNode):
    prev = dummy = BiNode(None)
    for n in head.in_order():
        prev.node2 = n
        n.node1 = prev
        prev = n
    dummy.node2.node1 = None
    return dummy.node2


def __main():
    n = head = BiNode(4)
    n.node1 = BiNode(2)
    n = n.node1
    n.node1 = BiNode(1)
    n.node2 = BiNode(3)
    n = head
    n.node2 = BiNode(6)
    n.node2.node1 = BiNode(5)
    t = to_double_ll(head)

    t = head
    while t.node2:
        print(t.node1, '<=>', t, '<=>', t.node2)
        t = t.node2
    print('===')
    while t.node1:
        print(t.node1, '<=>', t, '<=>', t.node2)
        t = t.node1
    pass


if __name__ == '__main__':
    __main()
