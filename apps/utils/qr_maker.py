import io
import base64
from qrcode import make
from qrcode.image.svg import SvgImage


class QRMaker:
    @staticmethod
    def _bytes(data, factory=None):
        buffer = io.BytesIO()
        qr = make(data, image_factory=factory, box_size=20, border=1)
        qr.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @classmethod
    def make_base64(cls, data) -> str:
        return "data:image/png;base64," + base64.b64encode(cls._bytes(data)).decode(
            "utf-8"
        )

    @classmethod
    def make_png(cls, data) -> bytes:
        return cls._bytes(data)

    @classmethod
    def make_svg(cls, data) -> bytes:
        return cls._bytes(data, factory=SvgImage)


qr = QRMaker()
