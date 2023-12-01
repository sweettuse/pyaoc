from itertools import count

from hashlib import md5

__author__ = "acushner"


data = "yzbqklnj"


def parts1and2(num_zeros):
    target = num_zeros * "0"
    for i in count():
        if md5(f"{data}{i}".encode()).hexdigest().startswith(target):
            return i

    print(parts1and2(5))
    print(parts1and2(6))


if __name__ == "__main__":
    __main()
