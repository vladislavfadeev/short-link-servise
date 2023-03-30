from django.urls import path ,include
from apps.home.views import (
    HomeView,
    FeaturesInfoView,
    BotInfoView,
    APIInfoView,
    download_qr
)

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('features', FeaturesInfoView.as_view(), name='features'),
    path('bot', BotInfoView.as_view(), name='bot'),
    path('api', APIInfoView.as_view(), name='api'),
    path('download/<str:file>', download_qr),

]