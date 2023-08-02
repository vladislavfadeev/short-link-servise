from django.urls import path
from apps.cutter.views import GroupRedirect, LinkRedirect

app_name = 'cutter'

urlpatterns = [
    path('g/<str:slug>', GroupRedirect.as_view(), name='redirect_group_url'),
    path('<str:slug>', LinkRedirect.as_view(), name='redirect_url'),
]
