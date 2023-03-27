from django.urls import path , include
from django.views.generic import TemplateView
# from django.contrib.auth import views
import apps.user_profile.views as views

# app_name = 'authuser'


urlpatterns = [
    path('', views.DashBoardView.as_view(), name='profile'),
    path('user/', views.ProfileView.as_view(), name='user_page')
]