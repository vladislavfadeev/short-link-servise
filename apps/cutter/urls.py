from django.urls import path ,include
from . import views
from .views import (RedirectSlug,
                    HomeView,
                    FeaturesInfoView,
                    BotInfoView,
                    APIInfoView
                    )

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('test', views.test),
    path('features', FeaturesInfoView.as_view(), name='features'),
    path('bot', BotInfoView.as_view(), name='bot'),
    path('api', APIInfoView.as_view(), name='api'),
    path('download/<str:file>', views.download_file),
    path('<str:slug>', RedirectSlug.as_view(), name='redirect_url'), 

]
