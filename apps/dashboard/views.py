from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
)

from apps.db_model.statistics import Statistics
from apps.db_model.models import GroupLinkModel, LinkModel, QRCodeModel
from apps.authuser.models import User, Token
from apps.dashboard.forms import DashboardLinkForm, DashboardGroupForm, QRCodeForm
from apps.dashboard.filters import LinksFilter, GroupFilter
from apps.utils.info_normalizer import get_user_info


class BaseDashboard(LoginRequiredMixin):
    login_url = "/login"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        segments = self.request.path.replace("?", "/").split("/")
        kwargs.setdefault("segment", segments)
        return super().get_context_data(**kwargs)


class DashboardView(BaseDashboard, TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        activity = Statistics.account_info(request.user)
        kwargs.setdefault("activity", activity)
        return super().get(request, *args, **kwargs)


class APIKeyView(BaseDashboard, TemplateView):
    template_name = "dashboard/api-dashboard.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(
            **kwargs, redoc="/api/v1/redoc", swagger="/api/v1/docs"
        )
        return self.render_to_response(context)

    def post(self, request):
        try:
            token = request.user.auth_token
        except User.auth_token.RelatedObjectDoesNotExist:
            token = Token(user=request.user)
            token.save()
        context = self.get_context_data()
        return self.render_to_response(context)


class LinksListView(BaseDashboard, ListView):
    template_name = "dashboard/links.html"
    paginate_by = 15
    context_object_name = "links"
    ordering = "-date_created"
    allow_order_params = []
    model = LinkModel

    def get_queryset(self) -> QuerySet[Any]:
        qs = self.model.objects.filter(user=self.request.user).order_by(self.ordering)
        self._f = LinksFilter(self.request.GET, queryset=qs, request=self.request)
        return self._f.qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        params = str()
        form_dict = self._f.form.data
        for key in form_dict.keys():
            if key in self._f.form.cleaned_data:
                params += "".join(f"{key}={self.request.GET.get(key)}&")
        kwargs.setdefault("filter", self._f)
        kwargs.setdefault("filter_query", params)
        return super().get_context_data(**kwargs)


class LinksDetailView(BaseDashboard, DetailView):
    template_name = "dashboard/links-info.html"
    model = LinkModel

    def get(self, request, *args, **kwargs):
        activity = Statistics.link_info(request.user, kwargs.get("slug"))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, activity=activity)
        return self.render_to_response(context)


class LinksCreateView(BaseDashboard, CreateView):
    template_name = "dashboard/links-create.html"
    success_url = reverse_lazy("links")
    form_class = DashboardLinkForm

    def get_initial(self):
        self.initial["user"] = self.request.user
        return super().get_initial()

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.user_info = get_user_info(request)
            link.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context={"form": form})


class LinksEditView(BaseDashboard, UpdateView):
    template_name = "dashboard/links-create.html"
    success_url = reverse_lazy("links")
    model = LinkModel
    form_class = DashboardLinkForm


class LinksDeleteView(BaseDashboard, View):
    model = LinkModel

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        obj = get_object_or_404(self.model, user=request.user, slug=slug)
        obj.delete()
        return HttpResponse(status=204)


class GroupsListView(BaseDashboard, ListView):
    template_name = "dashboard/groups.html"
    paginate_by = 15
    context_object_name = "groups"
    ordering = "-date_created"
    model = GroupLinkModel

    # def get_queryset(self) -> QuerySet[Any]:
    #     self.queryset = self.model.objects.filter(user=self.request.user)
    #     return super().get_queryset()

    def get_queryset(self) -> QuerySet[Any]:
        qs = self.model.objects.filter(user=self.request.user).order_by(self.ordering)
        self._f = GroupFilter(self.request.GET, queryset=qs)
        return self._f.qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        params = str()
        form_dict = self._f.form.data
        for key in form_dict.keys():
            if key in self._f.form.cleaned_data:
                params += "".join(f"{key}={self.request.GET.get(key)}&")
        kwargs.setdefault("filter", self._f)
        kwargs.setdefault("filter_query", params)
        return super().get_context_data(**kwargs)


class GroupsDetailView(BaseDashboard, DetailView):
    template_name = "dashboard/groups-info.html"
    model = GroupLinkModel

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        activity = Statistics.group_info(request.user, self.object.id)
        context = self.get_context_data(object=self.object, activity=activity)
        return self.render_to_response(context)


class GroupsLinkEntriesView(BaseDashboard, ListView, SingleObjectMixin):
    template_name = "dashboard/groups-links-entries.html"
    paginate_by = 15
    context_object_name = "links"
    ordering = "-date_created"
    allow_order_params = []
    model = LinkModel

    def get_queryset(self) -> QuerySet[Any]:
        self.object = get_object_or_404(
            GroupLinkModel,
            user=self.request.user,
            slug=self.kwargs.get(self.slug_url_kwarg),
        )
        qs = self.model.objects.filter(
            user=self.request.user, group=self.object
        ).order_by(self.ordering)
        self._f = LinksFilter(self.request.GET, queryset=qs)
        return self._f.qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        params = str()
        form_dict = self._f.form.data
        for key in form_dict.keys():
            if key in self._f.form.cleaned_data:
                params += "".join(f"{key}={self.request.GET.get(key)}&")
        kwargs.setdefault("filter", self._f)
        kwargs.setdefault("filter_query", params)
        return super().get_context_data(**kwargs)


class GroupsCreateView(BaseDashboard, CreateView):
    template_name = "dashboard/groups-create.html"
    success_url = reverse_lazy("groups")
    form_class = DashboardGroupForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.user_info = get_user_info(request)
            group.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context={"form": form})


class GroupsEditView(BaseDashboard, UpdateView):
    template_name = "dashboard/groups-create.html"
    success_url = reverse_lazy("groups")
    model = GroupLinkModel
    form_class = DashboardGroupForm


class GroupsDeleteView(BaseDashboard, View):
    model = GroupLinkModel

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        obj = get_object_or_404(self.model, user=request.user, slug=slug)
        obj.delete()
        return HttpResponse(status=204)


class QRCodeListView(BaseDashboard, ListView):
    template_name = "dashboard/qrcode.html"
    paginate_by = 15
    context_object_name = "qrcodes"
    ordering = "-date_created"
    model = QRCodeModel

    def get_queryset(self) -> QuerySet[Any]:
        self.queryset = self.model.objects.filter(user=self.request.user)
        return super().get_queryset()


class QRCodeCreateView(BaseDashboard, CreateView):
    template_name = "dashboard/qrcode-create.html"
    success_url = reverse_lazy("qrcode")
    form_class = QRCodeForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            qrcode = form.save(commit=False)
            qrcode.user = request.user
            qrcode.user_info = get_user_info(request)
            qrcode.save()
            return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, context={"form": form})


class QRCodeEditView(BaseDashboard, UpdateView):
    template_name = "dashboard/qrcode-create.html"
    success_url = reverse_lazy("qrcode")
    model = QRCodeModel
    form_class = QRCodeForm


class QRCodeDeleteView(BaseDashboard, View):
    model = QRCodeModel

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        obj = get_object_or_404(self.model, user=request.user, slug=slug)
        obj.delete()
        return HttpResponse(status=204)
