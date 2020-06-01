import webbrowser
from typing import Tuple

from webcolors import hex_to_rgb, rgb_to_hex
import re

COLOR_VIEWER_URL = "miquelvir.github.io/color/%s"


class Color:
    def __init__(self, hex_: str = None, rgb_: Tuple[int, int, int] = None):
        self._rgb = None
        self._alpha = 1

        if hex_ is not None and rgb_ is not None:
            raise ValueError("provide just one color initialization")

        if hex_ is not None:
            self.hex = hex_
        elif rgb_ is not None:
            self.rgb = rgb_

    @staticmethod
    def is_valid_hex(color):
        return re.match('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color)

    @staticmethod
    def is_valid_alpha(alpha):
        return 0 <= alpha <= 1

    @property
    def hex(self):
        return rgb_to_hex(self._rgb)

    @hex.setter
    def hex(self, color):
        if not self.is_valid_hex(color):
            raise ValueError("invalid hex")

        self._rgb = hex_to_rgb(color)

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, color: Tuple[int, int, int]):
        if len(color) != 3:
            raise ValueError("3 parameters needed")
        self._rgb = color

    def r(self) -> int:
        return self._rgb[0]

    def g(self) -> int:
        return self._rgb[1]

    def b(self) -> int:
        return self._rgb[2]

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        if not self.is_valid_alpha(value):
            raise ValueError("invalid alpha, must be float between 0 and 1")

        self._alpha = value

    def __add__(self, other):
        def mix(base, transparent):
            r = base.r() + (transparent.r() - base.r()) * transparent.alpha
            g = base.g() + (transparent.g() - base.g()) * transparent.alpha
            b = base.b() + (transparent.b() - base.b()) * transparent.alpha
            return int(r), int(g), int(b)

        if not type(other) == Color:
            raise ValueError("can't add")
        if other.alpha is not 1 and self.alpha is not 1:
            raise ValueError("at least one color must have alpha 1")

        if other.alpha == 1:
            return Color(rgb_=mix(other, self))
        else:
            return Color(rgb_=mix(self, other))


def main():
    try:
        c1 = Color(input("base color in hex (include #): "))
        c2 = Color(input("overlay color in hex (include #): "))

        transparency = None
        transparencies = []
        while transparency != "":
            transparency = input("transparency (int in [0, 100]; empty for results): ")

            if transparency != "":
                transparency = int(transparency)
                if not 0 <= transparency <= 100:
                    raise ValueError("transparency must be between 0 and 100")

                transparencies.append(transparency)
    except ValueError as e:
        print(e)
    else:
        for transparency in transparencies:
            c2.alpha = transparency / 100
            c_result = c1 + c2
            print(c_result.hex)
            webbrowser.open(COLOR_VIEWER_URL % c_result.hex)
    finally:
        print("closing...")


main()
