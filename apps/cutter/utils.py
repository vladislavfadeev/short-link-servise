from django.conf import settings
import qrcode.image.svg



def make_qr(data):
    img_png = qrcode.make(data, box_size=20)
    # img_png_name = 'qr-' + data[16:] + '.png'
    img_png.save(f"{settings.MEDIA_ROOT}/qr.png")
    img_svg = qrcode.make(data,
                        image_factory=qrcode.image.svg.SvgImage, 
                        box_size=20)
    # img_svg_name = 'qr-' + data[16:] + '.svg'
    img_svg.save(f"{settings.MEDIA_ROOT}/qr.svg")

    # return img_png_name, img_svg_name