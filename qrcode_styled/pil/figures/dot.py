from qrcode_styled.types import num
from .base import Figure

__all__ = [
    'Dot',
    'RoundedDot',
    'ExtraRoundedDot',
]


class Dot(Figure):
    def draw(self, x: num, y: num, size: num, color=None, top=0, right=0, bottom=0, left=0):
        raise NotImplementedError

    def _basic_dot(self, x, y, size, color, rotation):
        self.ctx.ellipse((x, y, x + size, y + size), fill=color, outline=None, width=0)

    def _basic_square(self, x, y, size, color, rotation):
        self.ctx.rectangle((x, y, x + size, y + size), fill=color, outline=None, width=0)

    def _basic_side_rounded(self, x, y, size, color, rotation):
        self.ctx.pieslice((x, y, x + size, y + size), 270 + rotation, 90 + rotation, fill=color, outline=None, width=0)
        rotate = rotation % 360
        half = size / 2
        if rotate == 0:
            self.ctx.rectangle((x, y, x + half, y + size), fill=color, outline=None, width=0)
        elif rotate in [90, -270]:
            self.ctx.rectangle((x, y, x + size, y + half), fill=color, outline=None, width=0)
        elif rotate in [180, -180]:
            self.ctx.rectangle((x + half, y, x + size, y + size), fill=color, outline=None, width=0)
        else:
            self.ctx.rectangle((x, y + half, x + size, y + size), fill=color, outline=None, width=0)

    def _basic_corner_rounded(self, x, y, size, color, rotation):
        rotate = ((rotation + 360) % 360)
        self.ctx.pieslice((x, y, x + size, y + size), rotation - 90, rotation, fill=color, outline=None, width=0)
        half = size / 2
        if rotate != 0:  # If top-right is not rounded, print square there
            self.ctx.rectangle((x + half, y, x + size, y + half), fill=color, outline=None, width=0)
        if rotate != 90:  # If bottom-right is not rounded, print square there
            self.ctx.rectangle((x + half, y + half, x + size, y + size), fill=color, outline=None, width=0)
        if rotate != 180:  # If bottom-left is not rounded, print square there
            self.ctx.rectangle((x, y + half, x + half, y + size), fill=color, outline=None, width=0)
        if rotate != 270:  # If top-left is not rounded, print square there
            self.ctx.rectangle((x, y, x + half, y + half), fill=color, outline=None, width=0)

    def _basic_corner_extra_rounded(self, x, y, size, color, rotation):
        rotate = rotation % 360
        _x = _y = 0
        if rotate == 0:
            _x = size
        elif rotate in [90, -270]:
            _x = _y = size
        elif rotate in [180, -180]:
            _y = size

        x1y1 = (x - _x, y - _y)
        x2y2 = (x + size * 2 - _x, y + size * 2 - _y)
        self.ctx.pieslice((x1y1, x2y2), rotation - 90, rotation, fill=color, outline=None, width=0)


class RoundedDot(Dot):
    def draw(self, x: num, y: num, size: num, color=None, top=0, right=0, bottom=0, left=0):
        n_count = right + top + bottom + left

        if n_count > 2 or (left and right) or (top and bottom):
            return self._basic_square(x, y, size, color, rotation=0)
        elif n_count == 2:
            rotation = 0
            if left and top:
                rotation = 90
            elif top and right:
                rotation = 180
            elif right and bottom:
                rotation = 270
            return self._basic_corner_rounded(x, y, size, color, rotation=rotation)
        elif n_count == 1:
            rotation = 0
            if top:
                rotation = 90
            elif right:
                rotation = 180
            elif bottom:
                rotation = 270
            return self._basic_side_rounded(x, y, size, color, rotation=rotation)
        else:
            return self._basic_dot(x, y, size, color, rotation=0)


class ExtraRoundedDot(Dot):
    def draw(self, x: num, y: num, size: num, color=None, top=0, right=0, bottom=0, left=0):
        n_count = right + top + bottom + left

        if n_count > 2 or (left and right) or (top and bottom):
            return self._basic_square(x, y, size, color, rotation=0)
        elif n_count == 2:
            rotation = 0
            if left and top:
                rotation = 90
            elif top and right:
                rotation = 180
            elif right and bottom:
                rotation = 270
            return self._basic_corner_extra_rounded(x, y, size, color, rotation=rotation)
        elif n_count == 1:
            rotation = 0
            if top:
                rotation = 90
            elif right:
                rotation = 180
            elif bottom:
                rotation = 270
            return self._basic_side_rounded(x, y, size, color, rotation=rotation)
        else:
            return self._basic_dot(x, y, size, color, rotation=0)
