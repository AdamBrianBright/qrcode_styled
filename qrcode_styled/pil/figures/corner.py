from qrcode_styled.types import num
from .base import Figure

__all__ = [
    'Corner',
    'ExtraRoundedCornerSquare',
    # 'ExtraRoundedCornerDot',
]


class Corner(Figure):
    def draw(self, x: num, y: num, size: num, color=None, rotation: num = 0):
        raise NotImplementedError


class ExtraRoundedCornerSquare(Corner):

    def draw(self, x: num, y: num, size: num, color=None, rotation: num = 0):
        self.ctx.rounded_rectangle((x, y, x + size, y + size), size / 7 * 3, fill=None, outline=color, width=size // 7)

# class ExtraRoundedCornerDot(Figure):
#     def draw(self, x: num, y: num, size: num, color, rotation: num = 0):
#         ...
