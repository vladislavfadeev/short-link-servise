from django.urls import path , include
from django.contrib.auth import views as dj_views
import authuser.views as cust_views

app_name = 'authuser'


urlpatterns = [
    path('sign-in', dj_views.LoginView.as_view(), name='login'),
    # path('sign-up', cust_views.CreateUserView.as_view(), name='register'),
    path('logout', dj_views.LogoutView.as_view(), name='logout'),

    # path('', include('django.contrib.auth.urls')),
]