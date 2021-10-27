__author__ = 'acushner'


class Listy:
    def __init__(self, l: list[int]):
        self.l = l

    def __getitem__(self, i):
        if i >= len(self.l):
            return -1
        return self.l[i]


def find(l: Listy, v):
    if v == 1:
        return 0

    def find_end():
        cur = 1
        while l[cur] >= 0:
            cur *= 2
        return cur

    start, end = 0, find_end()
    while True:
        mid = (start + end) // 2

        if (cur := l[mid]) == v:
            print(start, mid, end)
            return mid

        if start >= end:
            raise ValueError('val not in list')

        if v < cur or cur == -1:
            end = mid
        else:
            start = mid + 1





def __main():
    l = [1, 2, 3, 3, 3, 3, 7, 9]
    l = [1, 2, 3, 4, 7, 9]
    print(len(l))
    print(find(Listy(l), 7))
    pass


if __name__ == '__main__':
    __main()
