from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from kombu.serialization import register
from jsonpickle import dumps, loads


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clkr_core.settings")

app = Celery("clkr_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


# Register custom serializer
register(
    "jsonpickle",
    dumps,
    loads,
    content_type="application/json",
    content_encoding="utf-8",
)
