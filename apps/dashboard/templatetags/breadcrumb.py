from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def breadcrumb_schema():
    return "http://schema.org/BreadcrumbList"


@register.inclusion_tag("breadcrumb/home.tpl")
def breadcrumb_home(url=None, title=None):
    title = "" if not title else title
    return {"url": reverse(url), "title": title}


@register.inclusion_tag("breadcrumb/item.tpl")
def breadcrumb_item(url=None, title=None, position=None, **kwargs):
    title = "" if not title else title
    
    return {"url": reverse(url, kwargs=kwargs), "title": title, "position": position}


@register.inclusion_tag("breadcrumb/active.tpl")
def breadcrumb_active(url=None, title=None, prefix=None, position=None):
    title = "" if not title else title
    return {"url": url, "prefix": prefix, "title": title, "position": position}
