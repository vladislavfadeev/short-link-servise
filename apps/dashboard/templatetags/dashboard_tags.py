from django import template

register = template.Library()


@register.filter(name='group_clicks')
def group_clicks(value):
    count = 0
    entered_links = value.linkmodel_set.all()
    for link in entered_links:
        count += link.statistics.all().count()
    return count