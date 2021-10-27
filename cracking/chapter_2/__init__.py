__author__ = 'acushner'


class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

    @classmethod
    def from_iter(cls, iterable):
        n = head = None

        for v in iterable:
            if n is None:
                n = head = Node(v)
            else:
                n = n.add(v)
        return head

    def __bool__(self):
        return True

    def __len__(self):
        return sum(1 for _ in self)

    def __iter__(self):
        cur = self
        while cur is not None:
            yield cur
            cur = cur.next

    def __str__(self):
        return f'{type(self).__name__}({self.val})'

    __repr__ = __str__

    def display(self):
        print(self.display_str)

    @property
    def display_str(self):
        return ' -> '.join(map(str, (n.val for n in self)))

    def add(self, v):
        self.next = Node(v)
        return self.next

    def __add__(self, other):
        if isinstance(other, Node):
            self.next = other
            return self.next
        return self.add(other)

    def rm_next(self):
        if not self.next:
            return
        self.next = self.next.next


def __main():
    Node.from_iter(range(6)).display()
    pass


if __name__ == '__main__':
    __main()
