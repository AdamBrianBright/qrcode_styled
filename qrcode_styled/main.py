import asyncio
import warnings
from functools import partial
from io import BytesIO
from typing import AnyStr, Optional, TypeVar

from PIL import Image
from qrcode import QRCode
from qrcode.constants import *

from .base.image import BaseStyledImage
from .pil.image import PilStyledImage

__all__ = [
    'ImageType',
    'QRCodeStyled',
    'ERROR_CORRECT_L',
    'ERROR_CORRECT_M',
    'ERROR_CORRECT_H',
    'ERROR_CORRECT_Q',
]

ImageType = TypeVar('ImageType', bound=BaseStyledImage)


class QRCodeStyled(QRCode):

    def __init__(
        self,
        version: Optional[int] = None,
        error_correction: int = ERROR_CORRECT_M,
        box_size: int = 32,
        border: int = 1,
        image_factory: type[ImageType] = PilStyledImage,
        mask_pattern: Optional[int] = None,
    ):
        super().__init__(version, error_correction, box_size, border, image_factory, mask_pattern)
        if self.image_factory is None:
            self.image_factory = PilStyledImage

    def set_data(self, data, optimize: int = 20):
        self.clear()
        self.add_data(data=data, optimize=optimize)

    def get_buffer(
        self,
        data: AnyStr,
        image: Image = None,
        _format: str = 'WEBP',
        optimize: int = 20,
        **kwargs,
    ) -> BytesIO:
        self.set_data(data, optimize=optimize)
        buff = BytesIO()
        if _format.upper() == 'WEBP':
            kwargs.setdefault('lossless', False)
            kwargs.setdefault('quality', 80)
            kwargs.setdefault('method', 2)
        self.make_image(image=image).save(buff, _format, **kwargs)
        return buff

    async def get_buffer_async(
        self,
        data: AnyStr,
        image: Image = None,
        _format: str = 'WEBP',
        optimize: int = 20,
        **kwargs,
    ) -> BytesIO:
        loop = asyncio.get_event_loop()
        part = partial(self.get_buffer,
                       data,
                       image,
                       _format,
                       optimize,
                       **kwargs)
        return await loop.run_in_executor(None, part)

    def get_image(
        self,
        data: AnyStr,
        image: Image = None,
        optimize: int = 20,
    ) -> ImageType:
        self.set_data(data, optimize=optimize)
        return self.make_image(image=image)

    async def get_image_async(
        self,
        data: AnyStr,
        image: Image = None,
        optimize: int = 20,
        **kwargs,
    ) -> ImageType:
        loop = asyncio.get_event_loop()
        part = partial(self.get_image, data, image, optimize, **kwargs)
        return await loop.run_in_executor(None, part)

    def get(self, *args, **kwargs):
        # TODO: Remove when 1.0.0
        warnings.warn('Renamed, use "get_buffer". Will be removed in 1.0.0', DeprecationWarning)
        return self.get_buffer(*args, **kwargs)

    async def get_async(self, *args, **kwargs):
        # TODO: Remove when 1.0.0
        warnings.warn('Renamed, use "get_buffer_async". Will be removed in 1.0.0', DeprecationWarning)
        return await self.get_buffer_async(*args, **kwargs)
