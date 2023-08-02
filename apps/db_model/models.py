import string
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.utils.qr_maker import qr
from clkr_core.settings import DOMAIN_NAME

User = get_user_model()


class GroupLinkModel(models.Model):
    user = models.ForeignKey(
        User,
        related_name='link_groups',
        on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=30, unique=True, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=30, null=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_expire = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=1024, null=True, blank=True)
    rotation = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'title']

    @property
    def qr(self):
        return qr.make_base64(self.short_url)
    
    @property
    def png(self):
        return qr.make_png(self.short_url)
    
    @property
    def svg(self):
        return qr.make_svg(self.short_url)
    
    @property
    def short_url(self):
        return DOMAIN_NAME + self.get_absolute_url()

    @classmethod
    def make_slug(cls, **kwargs):
        data = string.ascii_letters + string.digits
        while True:
            slug = ''.join(random.choice(data) for _ in range(4))
            if not cls.objects.filter(slug=slug, **kwargs).exists():
                break
        return slug

    def get_absolute_url(self):
        return reverse('cutter:redirect_group_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.make_slug()
        return super().save(*args, **kwargs)


class LinkModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        GroupLinkModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )
    title = models.CharField(max_length=512, null=True, blank=True)
    long_link = models.URLField(max_length=30000)
    password = models.CharField(max_length=128, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_changed = models.DateTimeField(auto_now=True)
    date_expire = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def qr(self):
        return qr.make_base64(self.short_url)
    
    @property
    def png(self):
        return qr.make_png(self.short_url)
    
    @property
    def svg(self):
        return qr.make_svg(self.short_url)
    
    @property
    def short_url(self):
        return DOMAIN_NAME + self.get_absolute_url()

    @classmethod
    def make_slug(cls, **kwargs):
        data = string.ascii_letters + string.digits
        while True:
            slug = ''.join(random.choice(data) for _ in range(8))
            if not cls.objects.filter(slug=slug, **kwargs).exists():
                break
        return slug
    
    def get_absolute_url(self):
        return reverse('cutter:redirect_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.make_slug()
        return super().save(*args, **kwargs)


class StatisticsModel(models.Model):
    link = models.ForeignKey(
        LinkModel,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    user_agent_unparsed = models.CharField(max_length=150, default='Not defined')
    fingerprint = models.TextField(null=True, blank=True)
    device = models.CharField(max_length=20, default='Not defined')
    os = models.CharField(max_length=20,default='Not defined')
    browser = models.CharField(max_length=20,default='Not defined')
    ref_link = models.CharField(max_length=30000,default='Not defined')
    user_ip = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
