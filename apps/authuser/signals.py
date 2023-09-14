from apps.dashboard.signals import enter_to_dashboard
from apps.db_model.models import LinkModel


def created_links_handler(request, user, **kwargs):
    uid = request.COOKIES.get("_uid")
    links = LinkModel.objects.filter(unauth_relation=uid)
    if links:
        links.update(user=user, unauth_relation=None)


enter_to_dashboard.connect(created_links_handler)
