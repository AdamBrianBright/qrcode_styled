from qrcode_styled import QRCodeStyled

qr = QRCodeStyled()

with open('test.webp', 'wb') as _fh:
    qr.get_image('https://cifrazia.com/ru/').save(_fh, 'WEBP', lossless=False, quality=80, method=2)
