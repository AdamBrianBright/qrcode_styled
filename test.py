from qrcode_styled import QRCodeStyled
from qrcode_styled.svg.image import SVGStylingImage

qr = QRCodeStyled()

with open('wiki/img/test.webp', 'wb') as _fh:
    qr.get_image(
        data='https://cifrazia.com/ru/',
    ).save(_fh, 'WEBP', lossless=False, quality=80, method=2)

qr = QRCodeStyled(image_factory=SVGStylingImage)

with open('wiki/img/test.svg', 'wb') as _fh:
    qr.get_image(
        data='https://cifrazia.com/ru/',
    ).save(_fh)
