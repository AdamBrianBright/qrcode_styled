# noinspection PyProtectedMember
from PIL import Image, ImageDraw

from ..image import PilStyledImage

__all__ = [
    'Figure',
]


class Figure:
    def __init__(self, img: PilStyledImage):
        self.img = img

    @property
    def im(self) -> Image.Image:
        return self.img.im

    @property
    def ctx(self) -> ImageDraw.ImageDraw:
        return self.img.ctx

    def draw(self, x: int, y: int, size: int):
        raise NotImplementedError
