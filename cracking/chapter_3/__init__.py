__author__ = 'acushner'


class _StackNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class Stack:
    def __init__(self):
        self._stack: _StackNode = None

    @property
    def is_empty(self):
        return not bool(self)

    def push(self, val):
        self._stack = _StackNode(val, self._stack)

    def pop(self):
        res = self._stack.val
        self._stack = self._stack.next
        return res

    def peek(self):
        if self:
            return self._stack.val

    def __bool__(self):
        return self._stack is not None

    def __str__(self):
        res = []
        while self:
            res.append(self.pop())
        s = ' | '.join(map(str, reversed(res)))
        while res:
            self.push(res.pop())
        return s


class Queue:
    def __init__(self):
        self._head = self._tail = None

    def add(self, val):
        n = _StackNode(val)
        if self._tail:
            self._tail.next = n
        self._tail = n
        if not self._head:
            self._head = n

    def __bool__(self):
        return bool(self._head)

    def remove(self):
        if not self._head:
            raise Exception('empty queue')
        n = self._head
        self._head = n.next
        return n.val

    def peek(self):
        if not self._head:
            raise Exception('empty queue')
        return self._head.val



def __main():
    s = Stack()
    s.push(4)
    s.push(5)
    s.push(6)
    print(s.pop())
    print(s.pop())
    s.push(21)
    print(s.peek())
    print(s.is_empty)
    print(s.pop())
    print(s.peek())
    print('=' * 30)
    q = Queue()
    q.add(4)
    q.add(5)
    q.add(6)
    print(q.remove())
    print(q.remove())
    q.add(62)
    print(q.peek())
    print(q.remove())
    print(q.remove())


if __name__ == '__main__':
    __main()
