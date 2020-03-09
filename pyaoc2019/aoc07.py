from itertools import repeat, permutations, cycle

from pyaoc2019.interpreter import Program, parse_file, parse_data, process

__author__ = 'acushner'

DONE = object()


def process_amps(program: Program):
    yield from process(program)
    yield DONE


def _input_stream(inp):
    yield inp
    while True:
        yield Program._output_register


def feedback(fn_or_data, inputs, as_data=True):
    Program._output_register = 0
    f = parse_data if as_data else parse_file
    amps = 'ABCDE'
    amp_map = {}
    inputs = iter(inputs)

    for a in cycle(amps):
        try:
            proc = amp_map[a]
        except KeyError:
            proc = amp_map[a] = process_amps(f(fn_or_data, _input_stream(next(inputs))))

        if next(proc) is DONE and a == 'E':
            break
    print()
    return Program._output_register


def get_best(input_range):
    return max(feedback(7, perm, as_data=False) for perm in permutations(input_range))


def __main():
    feedback('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0', [4, 3, 2, 1, 0])
    feedback('3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0', reversed([4, 3, 2, 1, 0]))
    feedback('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', [9, 8, 7, 6, 5])


if __name__ == '__main__':
    __main()
