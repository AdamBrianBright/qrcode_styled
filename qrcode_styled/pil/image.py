import math
from typing import Optional

from PIL import Image, ImageDraw, ImageFilter

from qrcode_styled.base.image import BaseStyledImage, CORNERS, DOT_MASK, SQUARE_MASK
from .figures.corner import Corner, ExtraRoundedCornerSquare
from .figures.dot import Dot, ExtraRoundedDot

__all__ = [
    'PilStyledImage',
]


class PilStyledImage(BaseStyledImage):
    DOT = ExtraRoundedDot
    CORNER = ExtraRoundedCornerSquare
    CORNER_DOT = None  # ExtraRoundedCornerDot

    kind = 'PNG'
    allowed_kinds = ('PNG', 'JPG', 'WEBP', 'GIF')

    def __init__(self, border, width, box_size, *args, **kwargs):
        super().__init__(border, width, box_size, *args, **kwargs)
        self.im: Optional[Image.Image] = None
        self.ctx: Optional[ImageDraw.ImageDraw] = None

        if self.background == 'transparent' or self.background == 'translucent':
            self.background = None

        self.dot: Optional[Dot] = self.DOT(self) if self.DOT else None
        self.corner: Optional[Corner] = self.CORNER(self) if self.CORNER else None
        self.corner_dot: Optional[Corner] = self.CORNER_DOT(self) if self.CORNER_DOT else None

    def draw(self):
        res = super().draw()
        self.im: Image.Image = self.im.filter(ImageFilter.SMOOTH)
        return res

    def clear(self):
        self.im = Image.new('RGBA', (self._width, self._height))
        self.ctx = ImageDraw.Draw(self.im)

    def save(self, stream, kind=None, **kwargs):
        self.draw()
        self.im.save(stream, self.check_kind(kind), **kwargs)

    def draw_background(self):
        if self.background:
            self.ctx.rectangle(((0, 0), (self._width, self._height)), self.background, False)

    def draw_dots(self, _filter):
        count = self.width
        size = self.dot_size
        x = math.floor((self._width - count * size) / 2)
        y = math.floor((self._height - count * size) / 2)

        for i, row in enumerate(self.matrix):
            for j, cell in enumerate(row):
                if not cell:
                    continue
                if _filter and not _filter(i, j):
                    continue
                _x = x + i * size
                _y = y + j * size
                self.dot.draw(
                    _x, _y, size, self._dot_color,
                    self.get_neighbour(i, j, 0, -1, _filter),
                    self.get_neighbour(i, j, 1, 0, _filter),
                    self.get_neighbour(i, j, 0, 1, _filter),
                    self.get_neighbour(i, j, -1, 0, _filter),
                )

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

            if self.corner:
                self.corner.draw(x, y, c_square_size, self._corner_color, rotation)
            else:
                self._draw_mask(SQUARE_MASK, x, y, dot_size, self._corner_color)

            if self.corner_dot:
                self.corner_dot.draw(x + dot_size * 2, y + dot_size * 2, c_dot_size, self._corner_dot_color, rotation)
            else:
                self._draw_mask(DOT_MASK, x, y, dot_size, self._corner_dot_color)

    def _draw_mask(self, mask, x, y, size, color):
        for i, row in mask.items():
            for j, cell in row.items():
                if not cell:
                    continue
                _x = x + i * size
                _y = y + j * size
                self.dot.draw(
                    _x, _y, size, color,
                    self._get_mask(mask, i, j - 1),
                    self._get_mask(mask, i + 1, j),
                    self._get_mask(mask, i, j + 1),
                    self._get_mask(mask, i - 1, j),
                )

    def draw_image(self):
        size = self.width * self.dot_size
        margin = self.image_margin
        x_beginning = math.floor((self._width - size) / 2)
        y_beginning = math.floor((self._height - size) / 2)
        dx = x_beginning + margin + (size - self.draw_image_size['width']) / 2
        dy = y_beginning + margin + (size - self.draw_image_size['height']) / 2
        dw = self.draw_image_size['width'] - margin * 2
        dh = self.draw_image_size['height'] - margin * 2

        self.im.paste(self.image.resize((int(dw), int(dh))), (int(dx), int(dy)))
