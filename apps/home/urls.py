from django.urls import path
from apps.home.views import (
    HomeView,
    FeaturesInfoView,
    BotInfoView,
    APIInfoView,
    DownloadFile
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('features', FeaturesInfoView.as_view(), name='features'),
    path('bot', BotInfoView.as_view(), name='bot'),
    path('api', APIInfoView.as_view(), name='api'),
    path('download/<str:model>/<str:slug>', DownloadFile.as_view(), name='download_qr'),
]