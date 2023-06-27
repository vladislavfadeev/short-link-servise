from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

import string
import random


User = get_user_model()


class GroupLinkModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=True)
    password = models.CharField(max_length=1024)


class LinkModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    group = models.ForeignKey(
        GroupLinkModel,
        on_delete=models.SET_NULL,
        null=True
    )
    slug = models.SlugField(
        max_length=30,
        unique=True
    )
    long_link = models.URLField(max_length=30000)
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=128, null=True)
    svg_image = models.CharField(max_length=30, null=True)
    png_image = models.CharField(max_length=30, null=True)
    date_created = models.DateField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)
    date_expire = models.DateField(null=True, blank=True)
    use_alias = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def make_slug():
        count = 0
        slug = ''

        while count < 8:
            slug += random.choice(string.ascii_letters + string.digits)
            count += 1
        return slug    

    def get_url(self):
        return f'https://clkr.su/{self.slug}'
    

class StatisticsModel(models.Model):
    link = models.ForeignKey(
        LinkModel,
        on_delete=models.CASCADE,
        related_name='transfer_stat'
    )
    user_agent_unparsed = models.CharField(max_length=150, default='Not defined')
    device = models.CharField(max_length=20, default='Not defined')
    os = models.CharField(max_length=20,default='Not defined')
    browser = models.CharField(max_length=20,default='Not defined')
    ref_link = models.CharField(max_length=30000,default='Not defined')
    user_ip = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)