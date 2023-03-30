from django.urls import path ,include
from apps.cutter.views import RedirectSlug

app_name = 'cutter'

urlpatterns = [

    path('<str:slug>', RedirectSlug.as_view(), name='redirect_url'), 

]
