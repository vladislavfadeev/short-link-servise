from django import template
from allauth.socialaccount.models import SocialAccount

register = template.Library()


@register.simple_tag(name="user_avatar")
def get_avatar_url(user):
    sa = SocialAccount.objects.filter(user=user).first()
    if sa:
        url = sa.get_avatar_url()
        return url
