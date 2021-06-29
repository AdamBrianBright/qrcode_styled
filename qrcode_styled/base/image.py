import math
from typing import Union

from PIL import Image
from qrcode import constants
from qrcode.image.base import BaseImage

__all__ = [
    'BaseStyledImage',
    'SQUARE_MASK',
    'DOT_MASK',
    'CORNERS',
]

_ERROR_CORRECTION_PERCENTS = {
    constants.ERROR_CORRECT_L: 0.07,
    constants.ERROR_CORRECT_M: 0.15,
    constants.ERROR_CORRECT_Q: 0.25,
    constants.ERROR_CORRECT_H: 0.3,
}

SQUARE_MASK = (
    (1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1),
)

DOT_MASK = (
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
)

SQUARE_MASK = {i: {j: c for j, c in enumerate(r)} for i, r in enumerate(SQUARE_MASK)}
DOT_MASK = {i: {j: c for j, c in enumerate(r)} for i, r in enumerate(DOT_MASK)}

CORNERS = (
    (0, 0, 0),
    (1, 0, 90),
    (0, 1, -90),
)


class BaseStyledImage(BaseImage):

    def __init__(self, border, width, box_size, *args, **kwargs):
        super().__init__(border, width, box_size, *args, **kwargs)
        self.matrix = [[0 for _ in range(self.width)] for _ in range(self.width)]
        self.image: Image.Image = kwargs.get('image', None)
        self.image_size = kwargs.get('image_size', 0.4)
        self.image_margin = kwargs.get('image_margin', 0)
        self.image_url = kwargs.get('image_url', '')
        self.correction_level = kwargs.get('correction_level', constants.ERROR_CORRECT_Q)
        self.background = kwargs.get('background', '#ffffff')
        self.draw_image_size = {
            'hide_x_dots': 0,
            'hide_y_dots': 0,
            'width': 0,
            'height': 0,
        }
        self._width = self._height = self.pixel_size
        self._dot_color = kwargs.get('dot_color', '#000000')
        self._corner_color = kwargs.get('corner_color', '#000000')
        self._corner_dot_color = kwargs.get('corner_dot_color', '#000000')

        self.dot_size = self.box_size
        self.border *= self.dot_size

        if self.image:
            self.draw_image_size = self.calculate_image_size()

    def drawrect(self, row, col):
        self.matrix[row][col] = 1

    def draw(self):
        if self.width > self._width or self.width > self._height:
            raise ValueError('Canvas is too small')

        self.clear()
        self.draw_background()
        self.draw_dots(self._draw_dots_filter)
        self.draw_corners()
        if self.image:
            self.draw_image()

    def save(self, stream, kind=None, **kwargs):
        raise NotImplementedError

    def calculate_image_size(self):
        cover_level = self.image_size * _ERROR_CORRECTION_PERCENTS[self.correction_level]
        max_hidden_dots = math.floor(cover_level * self.width * self.width)
        original_width = self.image.width
        original_height = self.image.height
        max_hidden_axis_dots = self.width - 14
        dot_size = self.dot_size

        if original_height <= 0 or original_width <= 0 or max_hidden_dots <= 0 or dot_size <= 0:
            return {
                'height': 0,
                'width': 0,
                'hide_x_dots': 0,
                'hide_y_dots': 0,
            }

        k = original_height / original_width

        # Getting the maximum possible axis hidden dots
        hide_x = math.floor(math.sqrt(max_hidden_dots / k))
        # The count of hidden dot's can't be less than 1
        if hide_x <= 0:
            hide_x = 1
        # Check the limit of the maximum allowed axis hidden dots
        if max_hidden_axis_dots and max_hidden_axis_dots < hide_x:
            hide_x = max_hidden_axis_dots
        # The count of dots should be odd
        if not hide_x % 2:
            hide_x -= 1
        # Calculate opposite axis hidden dots based on axis value.
        image_x = hide_x * dot_size
        # The value will be odd.
        # We use ceil to prevent dots covering by the image.
        hide_y = 1 + 2 * math.ceil((hide_x * k - 1) / 2)
        image_y = round(image_x * k)
        # If the result dots count is bigger than max - then decrease size and calculate again
        hide_y_range = bool(max_hidden_axis_dots and max_hidden_axis_dots < hide_y)
        if hide_y * hide_x > max_hidden_dots or hide_y_range:
            if hide_y_range:
                hide_y = max_hidden_axis_dots
                if not hide_y % 2:
                    hide_y -= 1
            else:
                hide_y -= 2
            image_y = hide_y * dot_size
            hide_x = 1 + 2 * math.ceil((hide_y / k - 1) / 2)
            image_x = round(image_y / k)

        return {
            'height': image_y,
            'width': image_x,
            'hide_y_dots': hide_y,
            'hide_x_dots': hide_x,
        }

    def _draw_dots_filter(self, i: Union[int, float], j: Union[int, float]) -> bool:
        hide_x = self.draw_image_size['hide_x_dots']
        hide_y = self.draw_image_size['hide_y_dots']
        count = self.width
        if (
                (count - hide_x) / 2 <= i < (count + hide_x) / 2 and
                (count - hide_y) / 2 <= j < (count + hide_y) / 2
        ):
            return False

        if self._get_mask(SQUARE_MASK, i, j) or self._get_mask(DOT_MASK, i, j):
            return False

        return True

    def _get_mask(self, mask, i: int, j: int) -> int:
        return (
                mask.get(i, {}).get(j, 0)
                or mask.get(i - self.width + 7, {}).get(j, 0)
                or mask.get(i, {}).get(j - self.width + 7, 0)
                or 0)

    def get_neighbour(self, x: int, y: int, i: int, j: int, _filter=None) -> bool:
        if i + x < 0 or j + y < 0 or i + x >= self.width or j + y >= self.width:
            return False
        if _filter and not _filter(i + x, j + y):
            return False
        try:
            return bool(self.matrix[i + x][j + y])
        except KeyError:
            return False

    def clear(self):
        raise NotImplementedError

    def draw_background(self):
        raise NotImplementedError

    def draw_dots(self, _filter):
        raise NotImplementedError

    def draw_corners(self):
        raise NotImplementedError

    def draw_image(self):
        raise NotImplementedError
