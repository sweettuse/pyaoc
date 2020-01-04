import colorsys
import operator as op
from functools import reduce, wraps
from typing import List, NamedTuple

import sty

__author__ = 'acushner'


class RGB(NamedTuple):
    r: int
    g: int
    b: int

    @property
    def hex(self) -> str:
        return hex((self.r << 16) + (self.g << 8) + self.b)

    @property
    def color(self) -> 'Color':
        return Color.from_rgb(self)

    def color_str(self, s, set_bg=False) -> str:
        """
        create str with different foreground(default)/background color for use in terminal
        reset to default at end of str
        """
        layer = sty.bg if set_bg else sty.fg
        return f'{layer(*self[:3])}{s}{layer.rs}'

    @staticmethod
    def _add_components(v1, v2):
        return int(((v1 ** 2 + v2 ** 2) / 2) ** .5)

    def __add__(self, other) -> 'RGB':
        add = self._add_components
        return RGB(add(self.r, other.r), add(self.g, other.g), add(self.b, other.b))


def _replace(func):
    @wraps(func)
    def wrapper(self, val):
        return self._replace(**{func.__name__[2:]: val})

    return wrapper


class Color(NamedTuple):
    hue: int
    saturation: int
    brightness: int

    @_replace
    def r_hue(self, val):
        """replace hue"""
        pass

    @_replace
    def r_saturation(self, val):
        """replace saturation"""

    @_replace
    def r_brightness(self, val):
        """replace brightness"""


    _mult = 2 ** 16
    _max_complements = 1024

    # ==================================================================================================================
    # CREATE COLORS FROM OTHER COLOR SPACES
    # ==================================================================================================================

    @classmethod
    def from_hex(cls, h) -> 'Color':
        nums = []
        for _ in range(3):
            nums.append(h & 0xff)
            h >>= 8
        nums.reverse()
        return cls.from_rgb(RGB(*nums))

    @classmethod
    def from_rgb(cls, rgb: RGB) -> 'Color':
        h, s, b = colorsys.rgb_to_hsv(*rgb[:3])
        mult = cls._mult - 1
        return cls(*map(int, (h * mult, s * mult, b / 255 * mult)))

    # ==================================================================================================================
    # COLOR PROPERTIES
    # ==================================================================================================================
    @property
    def hex(self) -> str:
        return self.rgb.hex

    @property
    def rgb(self) -> RGB:
        mult = self._mult - 1
        h, s, b = self.hue / mult, self.saturation / mult, self.brightness / mult * 255
        return RGB(*map(int, colorsys.hsv_to_rgb(h, s, b)))

    @property
    def bounded(self) -> 'Color':
        """force values into acceptable ranges - rotate around when exceeded"""
        return Color(*map(self._to_2_16, self[:3]))

    @property
    def clamped(self) -> 'Color':
        """force values into acceptable ranges - min/max when exceeded"""
        return Color(*map(self._validate_hsb, self[:3]))

    def color_str(self, s, set_bg=False) -> str:
        """
        create str with different foreground(default)/background color for use in terminal
        reset to default at end of str
        """
        return self.rgb.color_str(s, set_bg)

    # ==================================================================================================================
    # COLOR METHODS
    # ==================================================================================================================

    def offset_hue(self, degrees) -> 'Color':
        hue = self._to_2_16(self.hue + degrees / 360 * self._mult)
        return self._replace(hue=hue)

    def get_complements(self, degrees) -> List['Color']:
        """
        return list of colors offset by degrees

        this list will contain all unique colors that can be produced by this
        degree offset (i.e., it will keep offsetting until it makes it around the color wheel,
        perhaps multiple times, back to the starting point)

        useful because it avoids rounding errors that can occur by doing something like:
        >>> c = Colors.YALE_BLUE
        >>> for _ in range(1000):
        >>>     c = c.offset_hue(30)
        """
        res = [self]
        for n in range(1, self._max_complements):
            n_deg = n * degrees
            if n_deg % 360 == 0:
                break

            res.append(self.offset_hue(n_deg))
        else:
            from warnings import warn
            warn(f'exceeded max number of complements: {self._max_complements}, something may have gone wrong')

        return res

    @staticmethod
    def _to_2_16(val):
        """force val to be between 0 and 65535 inclusive, rotate"""
        return int(min(65535, val % Color._mult))

    @staticmethod
    def _validate_hsb(val) -> int:
        """clamp to range [0, 65535]"""
        return int(min(max(val, 0), 65535))

    # ==================================================================================================================
    # ADD COLORS TOGETHER
    # ==================================================================================================================
    def __add__(self, other) -> 'Color':
        """avg colors together using math"""
        return (self.rgb + other.rgb).color

    def __iadd__(self, other):
        return self + other


class ColorsMeta(type):
    """make `Colors` more accessible"""

    def __iter__(cls):
        return ((name, val)
                for name, val in vars(cls).items()
                if isinstance(val, Color))

    def __getitem__(cls, item):
        return cls.__dict__[item]

    def __str__(cls):
        colors = '\n\t'.join(map(str, cls))
        return f'{cls.__name__}:\n\t{colors}'

    def sum(cls, *colors: Color) -> Color:
        """average together all colors provided"""
        return reduce(op.add, colors)

    def by_name(cls, name) -> List[Color]:
        """get colors if they contain `name` in their name"""
        name = name.lower()
        return [c for n, c in cls if name in n.lower()]


class Colors(metaclass=ColorsMeta):
    DEFAULT = Color(43520, 0, 39321)
    OFF = Color(0, 0, 0)

    RED = Color(65535, 65535, 65535)
    ORANGE = Color(6500, 65535, 65535)
    YELLOW = Color(9000, 65535, 65535)
    GREEN = Color(16173, 65535, 65535)
    CYAN = Color(29814, 65535, 65535)
    BLUE = Color(43634, 65535, 65535)
    PURPLE = Color(50486, 65535, 65535)
    MAGENTA = Color.from_hex(0xff00ff)
    PINK = Color(58275, 65535, 47142)

    WHITE = Color(58275, 0, 65535)
    COLD_WHITE = Color(58275, 0, 65535)
    WARM_WHITE = Color(58275, 0, 65535)
    GOLD = Color(58275, 0, 65535)
    BROWN = Color.from_hex(0xa0522d)

    COPILOT_BLUE = Color.from_hex(0x00b4e3)
    COPILOT_BLUE_GREEN = Color.from_hex(0x00827d)
    COPILOT_BLUE_GREY = Color.from_hex(0x386e8f)
    COPILOT_DARK_BLUE = Color.from_hex(0x193849)

    HANUKKAH_BLUE = Color.from_hex(0x09239b)

    MARIO_BLUE = Color.from_hex(0x049cd8)
    MARIO_YELLOW = Color.from_hex(0xfbd000)
    MARIO_RED = Color.from_hex(0xe52521)
    MARIO_GREEN = Color.from_hex(0x43b047)

    PYTHON_LIGHT_BLUE = Color.from_hex(0x4b8bbe)
    PYTHON_DARK_BLUE = Color.from_hex(0x306998)
    PYTHON_LIGHT_YELLOW = Color.from_hex(0xffe873)
    PYTHON_DARK_YELLOW = Color.from_hex(0xffd43b)
    PYTHON_GREY = Color.from_hex(0x646464)

    SNES_BLACK = Color.from_hex(0x211a21)
    SNES_DARK_GREY = Color.from_hex(0x908a99)
    SNES_DARK_PURPLE = Color.from_hex(0x4f43ae)
    SNES_LIGHT_GREY = Color.from_hex(0xcec9cc)
    SNES_LIGHT_PURPLE = Color.from_hex(0xb5b6e4)

    STEELERS_BLACK = Color.from_hex(0x101820)
    STEELERS_BLUE = Color.from_hex(0x00539b)
    STEELERS_GOLD = Color.from_hex(0xffb612)
    STEELERS_RED = Color.from_hex(0xc60c30)
    STEELERS_SILVER = Color.from_hex(0xa5acaf)

    XMAS_GOLD = Color.from_hex(0xe5d08f)
    XMAS_GREEN = Color.from_hex(0x18802b)
    XMAS_RED = Color.from_hex(0xd42426)

    YALE_BLUE = Color.from_hex(0xf4d92)


class LifxColors(metaclass=ColorsMeta):
    """colors available via voice from lifx"""
    WarmWhite = Color(hue=54612, saturation=0, brightness=32767)
    SoftWhite = Color(hue=54612, saturation=0, brightness=32767)
    White = Color(hue=54612, saturation=0, brightness=32767)
    Daylight = Color(hue=54612, saturation=0, brightness=32767)
    CoolWhite = Color(hue=54612, saturation=0, brightness=32767)

    Blue = Color(hue=43690, saturation=65535, brightness=65535)
    Crimson = Color(hue=63350, saturation=59551, brightness=65535)
    Cyan = Color(hue=32767, saturation=65535, brightness=65535)
    Fuchsia = Color(hue=54612, saturation=65535, brightness=65535)
    Gold = Color(hue=9102, saturation=65535, brightness=65535)
    Green = Color(hue=21845, saturation=65535, brightness=65535)
    Lavender = Color(hue=46420, saturation=32767, brightness=65535)
    Lime = Color(hue=13653, saturation=57670, brightness=65535)
    Magenta = Color(hue=54612, saturation=65535, brightness=65535)
    Orange = Color(hue=7099, saturation=65535, brightness=65535)
    Pink = Color(hue=63350, saturation=16449, brightness=65535)
    Purple = Color(hue=50425, saturation=56484, brightness=65535)
    Red = Color(hue=0, saturation=65535, brightness=65535)
    Salmon = Color(hue=3094, saturation=34078, brightness=65535)
    SkyBlue = Color(hue=35862, saturation=27727, brightness=65535)
    Teal = Color(hue=32767, saturation=65535, brightness=65535)
    Turquoise = Color(hue=31675, saturation=47106, brightness=65535)
    Violet = Color(hue=54612, saturation=29589, brightness=65535)


class ColorPower(NamedTuple):
    color: Color
    power: int
