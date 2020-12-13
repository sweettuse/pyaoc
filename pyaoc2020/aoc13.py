from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def parse_data1(fname=13):
    leave_time, buses = read_file(fname, 2020)
    buses = [int(v) for v in buses.split(',') if v != 'x']
    return int(leave_time), buses


def parse_data2(fname=13):
    _, buses = read_file(fname, 2020)
    return _to_offset_bid(buses)


def _to_offset_bid(s):
    return [(i, int(v)) for i, v in enumerate(s.split(',')) if v != 'x']


def part1():
    leave, buses = parse_data1()
    wait, bus_id = min((b - leave % b, b) for b in buses)
    return wait * bus_id


def part2():
    """
    find v such that
    bid0 % v == 0 and
    bid1 % v == 1 and
    ...
    bidn % v == n
    """
    buses = parse_data2()
    (offset, mag), *rest = buses
    for new_offset, new_mag in rest:
        mag, offset = combine_phased_rotations(mag, offset, new_mag, new_offset)

    return -offset % mag


# ======================================================================================================================
# from SO https://math.stackexchange.com/a/3864593/861686

def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


# ======================================================================================================================

@timer
def __main():
    """
    ginormous hat tip to https://math.stackexchange.com/a/3864593/861686
    google search that led me there was: "lcm with offset periodicity"
    """
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
