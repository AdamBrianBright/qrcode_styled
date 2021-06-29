import math
from typing import BinaryIO, Callable, Optional

from lxml import etree as d
# noinspection PyProtectedMember
from lxml.etree import _Element

from qrcode_styled.base.image import BaseStyledImage, CORNERS, DOT_MASK, SQUARE_MASK
from qrcode_styled.svg.figures.corner import Corner, ExtraRoundedCornerSquare
from qrcode_styled.svg.figures.dot import Dot, ExtraRoundedDot

__all__ = [
    'SVGStylingImage',
]

UTF_8 = 'utf-8'
_HEAD = b"""<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
 "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
 """


class SVGStylingImage(BaseStyledImage):
    DOT = ExtraRoundedDot
    CORNER = ExtraRoundedCornerSquare
    CORNER_DOT = None  # ExtraRoundedCornerDot

    def __init__(self, border, width, box_size, *args, **kwargs):
        super().__init__(border, width, box_size, *args, **kwargs)
        self.svg: Optional[_Element] = None
        self.defs: Optional[_Element] = None
        self.dots_clip_path: Optional[_Element] = None
        self.corner_dot_clip_path: Optional[_Element] = None
        self.corner_square_clip_path: Optional[_Element] = None

        self.dot: Optional[Dot] = None
        self.corner: Optional[Corner] = None
        self.corner_dot: Optional[Corner] = None

    def save(self, stream: BinaryIO, kind=None, **kwargs):
        self.draw()
        stream.write(_HEAD)
        stream.write(d.tostring(self.svg))

    def clear(self):
        x = self._width
        self.svg = d.Element('svg', version='1.0', xmlns='http://www.w3.org/2000/svg',
                             width=f'{x}px', height=f'{x}px',
                             viewBox=f'0 0 {x} {x}', preserveAspectRation='xMidYMid meet')
        self.defs = d.Element('defs')
        self.svg.append(self.defs)
        self.dots_clip_path = d.Element('clipPath', id='clip-path-dot-color')
        self.defs.append(self.dots_clip_path)
        self.dot = self.DOT(self) if self.DOT else None
        self.corner = self.CORNER(self) if self.CORNER else None
        self.corner_dot = self.CORNER_DOT(self) if self.CORNER_DOT else None

    def draw_background(self):
        if not self.background:
            return
        self._create_color(self.background,
                           x=0, y=0, height=self._width, width=self._width,
                           name='background-color')

    def draw_dots(self, _filter: Callable[[int, int], bool] = None):
        count = self.width
        dot_size = self.dot_size

        x_beginning = math.floor((self._width - count * dot_size) / 2)
        y_beginning = math.floor((self._height - count * dot_size) / 2)
        self._create_color(background=self._dot_color,
                           x=x_beginning, y=y_beginning,
                           height=count * dot_size, width=count * dot_size,
                           name='dot-color')

        for i in range(count):
            for j in range(count):
                if _filter and not _filter(i, j):
                    continue
                if not self.matrix[i][j]:
                    continue

                _x = x_beginning + i * dot_size
                _y = y_beginning + j * dot_size

                el = self.dot.draw(
                    _x, _y, dot_size,
                    self.get_neighbour(i, j, 0, -1, _filter),
                    self.get_neighbour(i, j, 1, 0, _filter),
                    self.get_neighbour(i, j, 0, 1, _filter),
                    self.get_neighbour(i, j, -1, 0, _filter),
                )

                if el is not None and self.dots_clip_path is not None:
                    self.dots_clip_path.append(el)

    def draw_corners(self):
        count = self.width
        dot_size = self.dot_size
        c_square_size = dot_size * 7
        c_dot_size = dot_size * 3
        x_beginning = math.floor((self._width - count * dot_size) / 2)
        y_beginning = math.floor((self._height - count * dot_size) / 2)

        for column, row, rotation in CORNERS:
            x = x_beginning + column * dot_size * (count - 7)
            y = y_beginning + row * dot_size * (count - 7)
            c_square_clip_path = self.dots_clip_path
            c_dot_clip_path = self.dots_clip_path

            if self._corner_color:
                c_square_clip_path = d.Element('clipPath', id=f'clip-path-corners-square-color-{column}-{row}')
                self.defs.append(c_square_clip_path)
                self.corner_square_clip_path = self.corner_dot_clip_path = c_dot_clip_path = c_square_clip_path

                self._create_color(background=self._corner_color, x=x, y=y,
                                   height=c_square_size, width=c_square_size,
                                   name=f'corners-square-color-{column}-{row}',
                                   rotation=rotation)
            if self.corner:
                el = self.corner.draw(x, y, c_square_size, rotation)
                if el is not None and c_square_clip_path is not None:
                    c_square_clip_path.append(el)
            else:
                self._draw_mask(SQUARE_MASK, x, y, dot_size, c_square_clip_path)

            if self._corner_dot_color:
                c_dot_clip_path = d.Element('clipPath', id=f'clip-path-corners-dot-color-{column}-{row}')
                self.defs.append(c_dot_clip_path)
                self.corner_dot_clip_path = c_dot_clip_path

                self._create_color(background=self._corner_dot_color,
                                   x=x + dot_size * 2, y=y + dot_size * 2,
                                   height=c_dot_size, width=c_dot_size, name=f'corners-dot-color-{column}-{row}')

            if self.corner_dot:
                el = self.corner_dot.draw(x=x + dot_size * 2, y=y + dot_size * 2, size=c_dot_size, rotation=rotation)
                if el is not None and c_dot_clip_path is not None:
                    c_dot_clip_path.append(el)
            else:
                self._draw_mask(DOT_MASK, x, y, dot_size, c_dot_clip_path)

    def _draw_mask(self, mask, x, y, size, clip):
        for i, row in mask.items():
            for j, cell in row.items():
                if not cell:
                    continue
                _x = x + i * size
                _y = y + j * size
                el = self.dot.draw(
                    _x, _y, size,
                    self._get_mask(mask, i, j - 1),
                    self._get_mask(mask, i + 1, j),
                    self._get_mask(mask, i, j + 1),
                    self._get_mask(mask, i - 1, j),
                )
                if el is not None and clip is not None:
                    clip.append(el)

    def draw_image(self):
        count = self.width
        x_beginning = math.floor((self._width - count * self.dot_size) / 2)
        y_beginning = math.floor((self._height - count * self.dot_size) / 2)
        dx = x_beginning + self.image_margin + (count * self.dot_size - self.draw_image_size['width']) / 2
        dy = y_beginning + self.image_margin + (count * self.dot_size - self.draw_image_size['height']) / 2
        dw = self.draw_image_size['width'] - self.image_margin * 2
        dh = self.draw_image_size['height'] - self.image_margin * 2

        image = d.Element('image', href=self.image_url, x=str(dx), y=str(dy), width=f'{dw}px', height=f'{dh}px')
        self.svg.append(image)

    def _create_color(self, background: str, x: int, y: int, height: int, width: int, name: str, rotation: int = 0):
        rect = d.Element('rect', attrib={
            'x': str(x),
            'y': str(y),
            'height': str(height),
            'width': str(width),
            'clip-path': f"url('#clip-path-{name}')",
            'fill': background,
        })
        self.svg.append(rect)
