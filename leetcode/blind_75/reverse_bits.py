__author__ = 'acushner'


class Solution:
    def reverseBits(self, n: int) -> int:
        return int(bin(n)[2:].zfill(32)[::-1], 2)


def __main():
    pass


if __name__ == '__main__':
    __main()
