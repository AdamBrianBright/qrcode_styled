from PIL import Image

from qrcode_styled import ERROR_CORRECT_Q, QRCodeStyled

qr = QRCodeStyled()

# Save to the file
with open('test.webp', 'wb') as _fh:
    qr.get_image('payload').save(_fh, 'WEBP', lossless=False, quaility=80, method=2)

# Get BytesIO buffer
qrcode = qr.get_buffer('payload', _format='WEBP', lossless=False, quality=80, method=2)

# You may put Image in the center of a QR Code
im = Image.open('image.png')

qr.error_correction = ERROR_CORRECT_Q
qrcode = qr.get_buffer('payload', image=im, _format='WEBP')

# Print real bytes from buffer
print(qrcode.getvalue())
