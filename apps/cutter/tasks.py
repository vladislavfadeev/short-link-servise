from celery import shared_task
from apps.utils.header_requester import requester
from apps.db_model.models import LinkModel, UserInfoModel


@shared_task
def make_link_task(form_data, user_info, force, location, uid):
    link = LinkModel(**form_data)
    link.user_info = UserInfoModel(**user_info)
    if link.title is None:
        status, msg = requester(link.long_link, force)
        if not status:
            raise Exception(msg)
        link.title = msg
    if not link.user or location == "home":
        link.unauth_relation = uid
    link.user_info.save()
    link.save()
    return "OK"