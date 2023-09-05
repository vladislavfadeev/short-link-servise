from django.urls import path, re_path, include
from .views import MyConfirmEmailView


urlpatterns = [
    re_path(
        r"^accounts/confirm-email/(?P<key>[-:\w]+)/$",
        MyConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path('accounts/', include('allauth.urls')),    
]
