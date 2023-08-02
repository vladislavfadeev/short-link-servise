from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render

from apps.db_model.statistics import Statistics
from apps.db_model.models import GroupLinkModel, LinkModel
from apps.dashboard.forms import DashboardLinkForm, DashboardGroupForm


class BaseDashboard(LoginRequiredMixin):
    login_url = '/login'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        segments = self.request.path.replace('?', '/').split('/')
        kwargs.setdefault('segment', segments)
        return super().get_context_data(**kwargs)


class DashboardView(BaseDashboard, TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        account_info = Statistics.account_info(request.user)
        kwargs.setdefault('account', account_info)
        return super().get(request, *args, **kwargs)


class ProfileView(BaseDashboard, TemplateView):
    template_name = 'dashboard/icon-feather.html'


class LinksListView(BaseDashboard, ListView):
    template_name = 'dashboard/links.html'
    paginate_by = 15
    context_object_name = 'links'
    ordering = '-date_created'
    model = LinkModel

    def get_queryset(self) -> QuerySet[Any]:
        self.queryset = self.model.objects.filter(user=self.request.user)
        return super().get_queryset()


class LinksDetailView(BaseDashboard, DetailView):
    template_name = 'dashboard/page-blank.html'

    def get(self, request):
        return render(request, self.template_name)


class LinksCreateView(BaseDashboard, CreateView):
    template_name = 'dashboard/links-create.html'
    success_url = reverse_lazy('links')
    form_class = DashboardLinkForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context = {'form': form})


class LinksEditView(BaseDashboard, UpdateView):
    template_name = 'dashboard/links-create.html'
    success_url = reverse_lazy('links')
    model = LinkModel
    form_class = DashboardLinkForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class LinksDeleteView(BaseDashboard, View):
    model = LinkModel

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(self.model, user=request.user, slug=slug)
        obj.delete()
        return HttpResponse(status=204)


class GroupsListView(BaseDashboard, ListView):
    template_name = 'dashboard/groups.html'
    paginate_by = 15
    context_object_name = 'groups'
    ordering = '-date_created'
    model = GroupLinkModel

    def get_queryset(self) -> QuerySet[Any]:
        self.queryset = self.model.objects.filter(user=self.request.user)
        return super().get_queryset()
    

class GroupsCreateView(BaseDashboard, CreateView):
    template_name = 'dashboard/groups-create.html'
    success_url = 'groups'
    form_class = DashboardGroupForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class GroupsEditView(BaseDashboard, UpdateView):
    template_name = 'dashboard/groups-create.html'
    success_url = 'groups'
    model = GroupLinkModel
    form_class = DashboardGroupForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class GroupsDeleteView(BaseDashboard, View):
    model = GroupLinkModel

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        obj = get_object_or_404(self.model, user=request.user, slug=slug)
        obj.delete()
        return HttpResponse(status=204)