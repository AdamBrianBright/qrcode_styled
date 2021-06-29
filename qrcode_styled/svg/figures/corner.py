from lxml import etree as d

from qrcode_styled.types import num
from .base import Figure

__all__ = [
    'Corner',
    'ExtraRoundedCornerSquare',
    'ExtraRoundedCornerDot',
]


class Corner(Figure):
    def draw(self, x: num, y: num, size: num, rotation: num = 0):
        raise NotImplementedError


class ExtraRoundedCornerSquare(Corner):

    def draw(self, x: num, y: num, size: num, rotation: num = 0):
        dot_size = size / 7
        b = 2.5 * dot_size
        a = 2 * dot_size
        c = 1.5 * dot_size
        el = d.Element('path', attrib={
            'clip-rule': 'evenodd',
            'd': f'M {x} {y + b}'
                 f'v {a}'
                 f'a {b} {b}, 0, 0, 0, {b} {b}'
                 f'h {a}'
                 f'a {b} {b}, 0, 0, 0, {b} {-b}'
                 f'v {-a}'
                 f'a {b} {b}, 0, 0, 0, {-b} {-b}'
                 f'h {-a}'
                 f'a {b} {b}, 0, 0, 0, {-b} {b}'
                 f'M {x + b} {y + dot_size}'
                 f'h {a}'
                 f'a {c} {c}, 0, 0, 1, {c} {c}'
                 f'v {a}'
                 f'a {c} {c}, 0, 0, 1, {-c} {c}'
                 f'h {-a}'
                 f'a {c} {c}, 0, 0, 1, {-c} {-c}'
                 f'v {-a}'
                 f'a {c} {c}, 0, 0, 1, {c} {-c}'
        })
        return self._rotate_figure(el, x, y, size, rotation)


class ExtraRoundedCornerDot(Figure):
    def draw(self, x: num, y: num, size: num, rotation: num = 0):
        el = d.Element('circle', cx=str(x + size / 2), cy=str(y + size / 2), r=str(size / 2))
        return self._rotate_figure(el, x, y, size, rotation)
