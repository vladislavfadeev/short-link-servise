from django.urls import path
from apps.home.views import (
    HomeView,
    APIInfoView,
    DownloadFile,
    QRGeneratorView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api', APIInfoView.as_view(), name='api'),
    path('create-qr', QRGeneratorView.as_view(), name='qr_generator'),
    path('download/<str:model>/<str:slug>', DownloadFile.as_view(), name='download_qr'),
]