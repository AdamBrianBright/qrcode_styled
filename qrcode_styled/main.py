import asyncio
from functools import partial
from io import BytesIO
from typing import AnyStr, TypeVar

from PIL import Image
from qrcode import QRCode, constants

from .base.image import BaseStyledImage
from .pil.image import PilStyledImage

__all__ = [
    'QRCodeStyled',
]

ImageType = TypeVar('ImageType', bound=BaseStyledImage)


class QRCodeStyled(QRCode):

    def __init__(self, version=None, error_correction=constants.ERROR_CORRECT_Q, box_size=32, border=1,
                 image_factory=PilStyledImage, mask_pattern=None):
        super().__init__(version, error_correction, box_size, border, image_factory, mask_pattern)
        if self.image_factory is None:
            self.image_factory = PilStyledImage

    def set_data(self, data, optimize: int = 20):
        self.clear()
        self.add_data(data=data, optimize=optimize)

    def get(self, data: AnyStr, image: Image = None, _format='WEBP', optimize: int = 20, **kwargs) -> BytesIO:
        self.set_data(data, optimize=optimize)
        buff = BytesIO()
        if _format.upper() == 'WEBP':
            kwargs.setdefault('lossless', False)
            kwargs.setdefault('quality', 80)
            kwargs.setdefault('method', 2)
        self.make_image(image=image).save(buff, _format, **kwargs)
        return buff

    async def get_async(self, data: AnyStr, image: Image = None, _format='WEBP', optimize: int = 20,
                        **kwargs) -> BytesIO:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self.get, data, image, _format, optimize, **kwargs))

    def get_image(self, data: AnyStr, image: Image = None, optimize: int = 20) -> ImageType:
        self.set_data(data, optimize=optimize)
        return self.make_image(image=image)

    async def get_image_async(self, data: AnyStr, image: Image = None, optimize: int = 20, **kwargs) -> ImageType:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self.get, data, image, optimize, **kwargs))
