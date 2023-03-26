from django.urls import path , include
from django.views.generic import TemplateView
from django.contrib.auth import views
import authuser.views as custom_views

# app_name = 'authuser'


urlpatterns = [

    # path('', include('django.contrib.auth.urls')),
    path(
        'registration', 
        custom_views.CreateUserView.as_view(), 
        name='registration'
    ),
    path(
        'email_confirm', 
        TemplateView.as_view(template_name='authuser/registration/email_confirm.html'), 
        name='email_confirm'
    ),
    path(
        'email_verify/<uidb64>/<token>/', 
        custom_views.EmailVerifyView.as_view(), 
        name='email_verify'
    ),
    path(
        'email_verify_invalid',
        TemplateView.as_view(
            template_name='authuser/registartion/email_verify_invalid.html'
        ),
        name='email_verify_invalid'
    ),
    path(
        'login', 
        custom_views.CustomLoginView.as_view(
            template_name='authuser/registration/login.html'
        ), 
        name='login'
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", 
        views.PasswordResetView.as_view(
            template_name='authuser/registration/password_reset_form.html',
            email_template_name='authuser/registration/email/password_reset_email.html'
        ), 
         name="password_reset"
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name = 'authuser/registration/password_reset_done.html'
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(
            template_name = 'authuser/registration/password_reset_confirm.html'
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

]