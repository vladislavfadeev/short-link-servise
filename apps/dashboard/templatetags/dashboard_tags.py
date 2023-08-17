from django import template
from datetime import datetime

register = template.Library()


@register.filter(name="group_clicks")
def group_clicks(value):
    count = 0
    entered_links = value.linkmodel_set.all()
    for link in entered_links:
        count += link.statistics.all().count()
    return count


@register.filter(name="expired_items")
def expired_item(object, relation):
    related_objects = getattr(object, relation)
    queryset = related_objects.filter(date_expire__lte=datetime.now())
    return len(queryset)
