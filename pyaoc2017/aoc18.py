from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import suppress
from io import BytesIO
from queue import Queue
from typing import List, NamedTuple, Tuple, Union

__author__ = 'acushner'

from pyaoc2019.utils import read_file


def _make_int_if_possible(v):
    with suppress(ValueError):
        return int(v)
    return v


class Command(NamedTuple):
    cmd: str
    args: Tuple[Union[int, str], ...]

    @classmethod
    def from_str(cls, s: str):
        cmd, *args = s.split()
        return cls(cmd, tuple(map(_make_int_if_possible, args)))


class Program:
    def __init__(self, commands: List[Command]):
        self._regs = defaultdict(int)
        self._pc = 0
        self._cmds = commands
        self._last_sound = None
        self.last_recovered = None

        self._done = False

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._regs[item]
        return item

    def __setitem__(self, key, value):
        self._regs[key] = value

    @property
    def _is_valid(self):
        return not self._done and 0 <= self._pc < len(self._cmds)

    def run(self):
        while self._is_valid:
            cmd, args = self._cmds[self._pc]
            getattr(self, cmd)(*args)
            self._pc += 1

    def snd(self, x):
        """play sound with freq x"""
        x = self._last_sound = self[x]
        return x

    def set(self, x, y):
        self[x] = self[y]

    def add(self, x, y):
        self[x] += self[y]

    def mul(self, x, y):
        self[x] *= self[y]

    def mod(self, x, y):
        self[x] %= self[y]

    def rcv(self, x):
        if self[x]:
            self.last_recovered = self._last_sound
            self._done = True

    def jgz(self, x, y):
        if self[x] > 0:
            self._pc += self[y] - 1


test = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

test_commands = [Command.from_str(s) for s in test.splitlines()]


def parse_data():
    return [Command.from_str(s) for s in read_file(18, 2017)]


def part1():
    prg = Program(parse_data())
    prg.run()
    return prg.last_recovered


# ======================================================================================================================
# ======================================================================================================================
class Manager:
    def __init__(self):
        self._qs: Tuple[Queue, Queue] = Queue(), Queue()

    def send(self, pid, val):
        self._qs[pid ^ 1].put(val)

    def recv(self, pid):
        return self._qs[pid].get(timeout=.2)


class P2(Program):
    mgr = Manager()

    def __init__(self, commands: List[Command], prog_id):
        super().__init__(commands)
        self._regs['p'] = self._pid = prog_id
        self.num_sent = 0

    def snd(self, x):
        self.num_sent += 1
        self.mgr.send(self._pid, self[x])

    def rcv(self, x):
        self[x] = self.mgr.recv(self._pid)


test2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

test2_commands = [Command.from_str(s) for s in test2.splitlines()]


def part2():
    commands = parse_data()
    with ThreadPoolExecutor(2) as pool:
        p0, p1 = P2(commands, 0), P2(commands, 1)
        pool.submit(p0.run)
        pool.submit(p1.run)
    return p1.num_sent


# ======================================================================================================================
# PLAY
# ======================================================================================================================

def play():
    class Play(Program):
        def __init__(self, commands: List[Command]):
            super().__init__(commands)
            self.sounds = []

        def snd(self, x):
            self.sounds.append(res := super().snd(x))
            return res

    p = Play(parse_data())
    p.run()
    print(p.sounds)

    import simpleaudio as sa
    from tones import SAWTOOTH_WAVE, SINE_WAVE, SQUARE_WAVE, TRIANGLE_WAVE
    from tones.mixer import Mixer
    mixer = Mixer(amplitude=.3)
    name = 'track'
    mixer.create_track(name, SAWTOOTH_WAVE, vibrato_frequency=None, vibrato_variance=3)
    for s in p.sounds:
        mixer.add_tone(name, s / 3, duration=.1)

    bio = BytesIO()
    mixer.write_wav(bio)
    bio.seek(0)

    wo = sa.WaveObject.from_wave_file(bio)
    wo.play().wait_done()


def __main():
    # print(part1())
    # print(part2())
    play()


if __name__ == '__main__':
    __main()
