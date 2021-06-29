__all__ = [
    'Figure',
]


class Figure:
    def __init__(self, img):
        self.img = img

    @property
    def im(self):
        return self.img.im

    @property
    def ctx(self):
        return self.img.ctx

    def draw(self, x: int, y: int, size: int, color=None):
        raise NotImplementedError
