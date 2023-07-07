import io
import base64
from qrcode import QRCode
from qrcode.image.svg import SvgImage


class QRMaker(QRCode):

    def __init__(self, box_size = 20, border = 2) -> None:
        super().__init__()
        self.box_size = box_size
        self.border = border
        self.buffer = io.BytesIO()

    def _flush(self) -> None:
        self.clear()
        self.buffer.seek(0)
        self.buffer.truncate(0)

    def _bytes(self, data, factory = None) -> bytes:
        self._flush()
        self.add_data(data)
        img = self.make_image(image_factory=factory)
        img.save(self.buffer)
        return self.buffer.getvalue()
    
    def make_base64(self, data) -> str:
        return "data:image/png;base64," + base64.b64encode(self._bytes(data)).decode("utf-8")
    
    def make_png(self, data) -> bytes:
        return self._bytes(data)
    
    def make_svg(self, data) -> bytes:
        factory = SvgImage
        return self._bytes(data, factory)
    

qr = QRMaker()



# def make_qr(data):
#     img_png = qrcode.make(data, box_size=20)
#     # img_png_name = 'qr-' + data[16:] + '.png'
#     img_png.save(f"{settings.MEDIA_ROOT}/qr.png")
#     img_svg = qrcode.make(data,
#                         image_factory=SvgImage, 
#                         box_size=20)
#     # img_svg_name = 'qr-' + data[16:] + '.svg'
#     img_svg.save(f"{settings.MEDIA_ROOT}/qr.svg")

    # return img_png_name, img_svg_name