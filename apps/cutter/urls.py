from django.urls import path
from apps.cutter.views import (
    GroupRedirect,
    LinkRedirect,
    CreateLinkView,
    TaskStatusView,
)

app_name = "cutter"

urlpatterns = [
    path("g/<str:slug>", GroupRedirect.as_view(), name="redirect_group_url"),
    path("<str:slug>", LinkRedirect.as_view(), name="redirect_url"),
    path("create_link/", CreateLinkView.as_view(), name="create_link"),
    path("task_status/<task_id>", TaskStatusView.as_view(), name="get_status"),
]
