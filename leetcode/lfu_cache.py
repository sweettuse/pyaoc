__author__ = 'acushner'

# https://leetcode.com/problems/lfu-cache/
from collections import defaultdict
from typing import Dict, Any, DefaultDict


class KeyCount:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.count = 0
        self.left = None
        self.right = None

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def rm(self):
        if self.left:
            self.left.right = self.right
        if self.right:
            self.right.left = self.left

    def add_right(self, other):
        if not self.right:
            self.right = other
            return

        new_right = self.right

        other.left = self
        other.right = new_right
        self.right = other
        new_right.left = other

    def display(self):
        cur = self
        res = []
        while cur:
            res.append(cur.key)
            cur = cur.right
        print(' -> '.join(map(str, res)))

    def display_left(self):
        cur = self
        res = []
        while cur:
            res.append(cur.key)
            cur = cur.left
        print(' -> '.join(map(str, res)))


class HeadTail:
    """store LRU"""

    def __init__(self):
        self.head = KeyCount()
        self.tail = KeyCount()
        self.tail.left = self.head
        self.head.right = self.tail

    def __bool__(self):
        return self.head.right != self.tail

    def add_front(self, kc):
        self.head.add_right(kc)

    def add_back(self, kc):
        self.tail.left.add_right(kc)


class Store:
    def __init__(self):
        self.min_count = 1
        self.count_to_ht: DefaultDict[int, HeadTail] = defaultdict(HeadTail)
        self.key_to_kc: Dict[Any, KeyCount] = {}

    def _get_kc(self, key):
        kc = self.key_to_kc.pop(key, None)
        if kc is None:
            raise KeyError(f'really expected {key!r} to be here')
        return kc

    def update(self, key, value):
        if key in self.key_to_kc:
            kc = self.rm(key)
            kc.value = value
        else:
            kc = self.key_to_kc[key] = KeyCount(key, value)
        kc.count += 1
        self.count_to_ht[kc.count].head.add_right(kc)

    def rm(self, key):
        kc = self._get_kc(key)
        kc.rm()
        if not self.count_to_ht[kc.count]:
            del self.count_to_ht[kc.count]
            if kc.count == self.min_count:
                self.min_count += 1
        return kc

    def pop_lfu(self):
        node = self.count_to_ht[self.min_count].tail.left
        self.rm(node.key)
        del self.key_to_kc[node.key]

    def __len__(self):
        return len(self.key_to_kc)

# store by count
# store count by LRU

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.store = Store()

    def get(self, key):
        if key in self.store.key_to_kc:
            return self.store.key_to_kc[key].value
        return -1

    def put(self, key, value):
        if len(self.store) >= self.capacity:
            self.store.pop_lfu()
        self.store.update(key, value)



def _test():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    print(c.get(1))
    c.put(3, 3)
    print(c.get(2))
    print(c.get(3))
    c.put(4, 4)
    print(c.get(1))
    print(c.get(3))
    print(c.get(4))
    # ["LFUCache", "put", "put", "get", "put", "get", "get", "put", "get", "get", "get"]
    # [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3], [4, 4], [1], [3], [4]]

def __main():
    return _test()
    ht = HeadTail()
    kc = KeyCount(1)
    ht.add_front(kc)
    ht.add_front(KeyCount(2))
    ht.add_back(KeyCount(69))
    ht.head.display()
    kc.rm()
    ht.head.display()
    ht.tail.display_left()

    pass


if __name__ == '__main__':
    __main()
