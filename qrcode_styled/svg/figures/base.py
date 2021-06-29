__all__ = [
    'Figure',
]


class Figure:
    def __init__(self, img):
        self.img = img

    @property
    def svg(self):
        return self.img.svg

    def _rotate_figure(self, el, x, y, size, rotation=0):
        if rotation:
            cx = x + size / 2
            cy = y + size / 2
            el.attrib['transform'] = f'rotate({rotation},{cx},{cy})'
        return el

    def draw(self, x: int, y: int, size: int):
        raise NotImplementedError
