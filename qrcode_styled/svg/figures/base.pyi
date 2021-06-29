import math

# noinspection PyProtectedMember
from lxml.etree import _Element

from qrcode_styled.svg.image import SVGStylingImage

__all__ = [
    'Figure',
]


class Figure:
    def __init__(self, img: SVGStylingImage):
        self.img: SVGStylingImage = img

    @property
    def svg(self) -> _Element:
        return self.img.svg

    def _rotate_figure(self, el: _Element, x: int, y: int, size: int, rotation: int = 0) -> _Element:
        deg = 180 * rotation / math.pi
        if deg:
            cx = x + size / 2
            cy = y + size / 2
            el.attrib['transform'] = f'rotate({deg},{cx},{cy})'
        return el

    def draw(self, x: int, y: int, size: int) -> _Element:
        raise NotImplementedError
