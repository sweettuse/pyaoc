def sign(d1, d2):
    if (d2 < 0 < d1) or (d1 < 0 < d2):
        return -1
    return 1


def divmod(d1, d2):
    count = 0
    if d2 <= d1:
        count, d1 = divmod(d1, d2 + d2)
        count += count
    while d1 - d2 >= 0:
        d1 -= d2
        count += 1
    return count, d1


class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        res_sign = sign(dividend, divisor)
        d1, d2 = abs(dividend), abs(divisor)
        count, _ = divmod(d1, d2)
        res = res_sign * count
        if not -2 ** 31 <= res <= 2 ** 31 - 1:
            return 2 ** 31 - 1
        return res
