import string
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.cutter.utils import qr


User = get_user_model()


class GroupLinkModel(models.Model):
    user = models.ForeignKey(
        User,
        related_name='link_groups',
        on_delete=models.CASCADE
    )
    alias = models.SlugField(max_length=30, unique=True, blank=True, db_index=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=1024, null=True)
    rotation = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'title']

    @classmethod
    def make_alias(cls, **kwargs):
        data = string.ascii_letters + string.digits
        while True:
            alias = ''.join(random.choice(data) for _ in range(4))
            if not cls.objects.filter(alias=alias, **kwargs).exists():
                break
        return alias 


class LinkModel(models.Model):
    user = models.ForeignKey(
        User,
        # related_name='links',
        on_delete=models.CASCADE,
        null=True
    )
    group = models.ForeignKey(
        GroupLinkModel,
        related_name='links',
        on_delete=models.SET_NULL,
        null=True
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        db_index=True
    )
    long_link = models.URLField(max_length=30000)
    password = models.CharField(max_length=128, null=True)
    date_created = models.DateField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)
    date_expire = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def qr(self):
        return qr.make_base64(self.short_url)
    
    @property
    def qr_png(self):
        return qr.make_png(self.short_url)
    
    @property
    def qr_svg(self):
        return qr.make_svg(self.short_url)
    
    @property
    def short_url(self):
        return f'https://clkr.su/{self.slug}'
    
    @classmethod
    def make_slug(cls, **kwargs):
        data = string.ascii_letters + string.digits
        while True:
            slug = ''.join(random.choice(data) for _ in range(8))
            if not cls.objects.filter(slug=slug, **kwargs).exists():
                break
        return slug    
    

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
