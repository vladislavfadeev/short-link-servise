from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render


# @login_required
class DashBoardView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'user_profile/index.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    template_name = 'user_profile/page-user.html'