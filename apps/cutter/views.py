import random
from datetime import datetime

from django.http import  Http404, HttpResponseRedirect
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import RedirectView

from apps.db_model.models import GroupLinkModel, LinkModel, StatisticsModel
from apps.cutter.forms import RedirectPasswordForm


class BaseRedirect(RedirectView):
    @staticmethod
    def _get_obj(model: models.Model, **kwargs):
        obj = model.objects.filter((Q(date_expire__gte=datetime.now()) | Q(date_expire=None)), **kwargs).first()
        if not obj:
            raise Http404
        return obj

    def _get_user_data(self, request, link):
        try:
            device = (str(request.user_agent).split('/')[0]).strip()
            StatisticsModel.objects.create(
                link = link,
                user_agent_unparsed = request.headers['user-agent'],
                device = device,
                os = request.user_agent.os.family,
                browser = request.user_agent.browser.family,
                ref_link = request.META.get('HTTP_REFERER'),
                user_ip = request.META['REMOTE_ADDR']
            )
        except:
            pass

    def get_redirect_url(self, *args, **kwargs):
        raise NotImplementedError
    
    def get(self, request, *args, **kwargs):
        raise NotImplementedError


class GroupRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def _get_links_list(self, group):
        links = LinkModel.objects.filter((Q(date_expire__gte=datetime.now()) | Q(date_expire=None)), group=group, is_active=True)
        if not links:
            raise Http404
        return links

    def _get_rotation_url(self, group):
        links = self._get_links_list(group)
        link = random.choice(links)
        self._get_user_data(self.request, link)
        return link.long_link
    
    def get(self, request, *args, **kwargs):
        alias = kwargs.get('alias')
        group = self._get_obj(GroupLinkModel, alias=alias, is_active=True)
        if group.rotation and group.password is None:
            url = self._get_rotation_url(group)
            return HttpResponseRedirect(url)
        if group.password:
            form = self.form_class()
            return render(request, 'cutter/redirect_password.html', context={'form': form})
        links = self._get_links_list(group)
        return render(request, 'cutter/group_link_page.html', context={'links': links})
    
    def post(self, request, *args, **kwargs):
        alias = kwargs.get('alias')
        group = self._get_obj(GroupLinkModel, alias=alias, is_active=True)
        form_data = request.POST.dict()
        form_data.setdefault('encoded_pwd', group.password)
        form = self.form_class(form_data)
        if form.is_valid():
            if group.rotation:
                url = self._get_rotation_url(group)
                return HttpResponseRedirect(url)
            links = self._get_links_list(group)
            return render(request, 'cutter/group_link_pange.html', context={'links': links})
        return render(request, 'cutter/redirect_password.html', context={'form': form})
    

class LinkRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        link = self._get_obj(LinkModel, slug=slug, is_active=True)
        if link.password:
            form = self.form_class()
            return render(request, 'cutter/redirect_password.html', context={'form': form})
        self._get_user_data(request, link)
        return HttpResponseRedirect(link.long_link)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        link = self._get_obj(LinkModel, slug=slug, is_active=True)
        form_data = request.POST.dict()
        form_data.setdefault('encoded_pwd', link.password)
        form = self.form_class(form_data)
        if form.is_valid():
            self._get_user_data(request, link)
            return HttpResponseRedirect(link.long_link)
        return render(request, 'cutter/redirect_password.html', context={'form': form})
        