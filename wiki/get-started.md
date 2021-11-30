# Getting Started

## Setup

```python
### Select Image factory

# SVG
from qrcode_styled.svg.image import SVGStylingImage
# Pillow
from qrcode_styled.pil.image import PilStyledImage

### Create QRCode factory

import qrcode_styled

qr = qrcode_styled.QRCodeStyled(
    # QRCode version. Default: auto
    version=None,
    # How much ECC. Default: M
    error_correction=qrcode_styled.ERROR_CORRECT_L,
    # Image border thickness in tiles. Default: 1
    border=1,
    # Size of each separate tile. Default: 32
    box_size=32,
    # Image processing library. Default: Pillow
    image_factory=SVGStylingImage,
    # QRCode mask pattern version: [0 to 7] included. Default: auto
    mask_pattern=None,
)

### Generate QRCode
img = qr.get_image(
    # Payload. Required
    data='https://cifrazia.com',
    # Image to put in the middle of QRCode. file handler.
    image=None,
    # Data encoding optimization level, not Image optimization.
    optimize=20,
)

### Store it in file
with open('link.webp') as _fh:
    img.save(_fh, 'WEBP')
```
