from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.db import models
import qrcode.image.svg
import string
import random


User = get_user_model()


class GroupLinkModel(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=True)
    password = models.CharField(max_length=128)


class LinkModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        max_length=30,
        unique=True
    )
    long_link = models.URLField(max_length=30000)
    statistics = models.BooleanField(default=False)
    group = models.ForeignKey(
        GroupLinkModel,
        on_delete=models.SET_NULL,
        null=True
    )
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    svg_image = models.CharField(max_length=30)
    png_image = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    date_expire = models.DateField()
    use_alias = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def make_slug():
        count = 0
        slug = ''

        while count < 8:
            slug += random.choice(string.ascii_letters + string.digits)
            count += 1
        return slug


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
    

    def get_url(self):
        return f'https://clkr.su/{self.slug}'
    

class LinkTransitionsModel(models.Model):

    link = models.ForeignKey(
        LinkModel,
        on_delete=models.CASCADE
    )
    user_agent_unparsed = models.CharField(max_length=150)
    device = models.CharField(max_length=20)
    os = models.CharField(max_length=20)
    browser = models.CharField(max_length=20)
    ref_link = models.CharField(max_length=30000)
    user_ip = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)

