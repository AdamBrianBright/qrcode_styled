# [WIP] QRCode Styled Generator

### This is a python port for a [browser QRCode generator](https://github.com/kozakdenys/qr-code-styling) by [Denys Kozak](https://github.com/kozakdenys)

```python
from qrcode_styled import QRCodeStyled

qr = QRCodeStyled()

# Save to file
with open('test.webp', 'wb') as _fh:
    qr.get_image('payload').save(_fh, 'WEBP', lossless=False, quaility=80, method=2)

# Get to BytesIO buffer
qrcode = qr.get('payload', _format='WEBP', lossless=False, quality=80, method=2)


# Also supports basic asyncio workaround
async def main():
    with open('test.webp', 'wb') as fh:
        img = await qr.get_image_async('payload')
        img.save(fh, 'WEBP', lossless=False, quaility=80, method=2)

    qrcode = await qr.get_async('payload', _format='WEBP', lossless=False, quality=80, method=2)


# You may put Image in the center of a QR Code

from PIL import Image

im = Image.open('image.png')
qrcode = qr.get('payload', im, _format='WEBP')
```

![Example 1](./test.webp)