import string

from pyaoc2019.utils import chunks, read_file

priority = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))


def part1(name):
    """calculate priority sum per compartment"""
    rucksacks_by_compartment = (
        (set(l[: (half := len(l) // 2)]), set(l[half:])) for l in read_file(name)
    )
    return sum(priority[(c1 & c2).pop()] for c1, c2 in rucksacks_by_compartment)


def part2(name):
    """calculate priority sum by shared"""
    return sum(
        priority[set.intersection(*map(set, sacks)).pop()]
        for sacks in chunks(read_file(name), 3)
    )


print(part1(3))
print(part2(3))
