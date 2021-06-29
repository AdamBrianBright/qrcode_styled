from lxml import etree as d

from qrcode_styled.types import num
from .base import Figure

__all__ = [
    'Dot',
    'ExtraRoundedDot',
]


class Dot(Figure):
    def draw(self, x: num, y: num, size: num, top=0, right=0, bottom=0, left=0):
        raise NotImplementedError

    def _basic_dot(self, x, y, size, rotation):
        el = d.Element('circle', cx=str(x + size / 2), cy=str(y + size / 2), r=str(size / 2))
        return self._rotate_figure(el, x, y, size, rotation)

    def _basic_square(self, x, y, size, rotation):
        el = d.Element('rect', x=str(x), y=str(y), width=str(size), height=str(size))
        return self._rotate_figure(el, x, y, size, rotation)

    def _basic_corner_extra_rounded(self, x, y, size, rotation):
        el = d.Element('path', attrib={
            'd': f'M {x} {y}'  # go to top left position
                 f'v {size}'  # draw line to left bottom corner
                 f'h {size}'  # draw line to right bottom corner
                 f'a {size} {size}, 0, 0, 0, {-size} {-size}'  # draw rounded top right corner
        })
        return self._rotate_figure(el, x, y, size, rotation)

    def _basic_side_rounded(self, x, y, size, rotation):
        el = d.Element('path', attrib={
            'd': f'M {x} {y}'  # go to top left position
                 f'v {size}'  # draw line to left bottom corner
                 f'h {size / 2}'  # draw line to left bottom corner + half of size right
                 f'a {size / 2} {size / 2}, 0, 0, 0, 0 {-size}'  # draw rounded corner
        })
        return self._rotate_figure(el, x, y, size, rotation)


class ExtraRoundedDot(Dot):
    def draw(self, x: num, y: num, size: num, top=0, right=0, bottom=0, left=0):
        n_count = right + top + bottom + left

        if n_count > 2 or (left and right) or (top and bottom):
            return self._basic_square(x, y, size, rotation=0)
        elif n_count == 2:
            rotation = 0
            if left and top:
                rotation = 90
            elif top and right:
                rotation = 180
            elif right and bottom:
                rotation = -90
            return self._basic_corner_extra_rounded(x, y, size, rotation=rotation)
        elif n_count == 1:
            rotation = 0
            if top:
                rotation = 90
            elif right:
                rotation = 180
            elif bottom:
                rotation = -90
            return self._basic_side_rounded(x, y, size, rotation=rotation)
        else:
            return self._basic_dot(x, y, size, rotation=0)
