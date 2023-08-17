import random
from datetime import datetime

from django.http import  Http404, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import RedirectView

from apps.db_model.models import GroupLinkModel, LinkModel, StatisticsModel
from apps.cutter.forms import RedirectPasswordForm
from apps.utils import requester


class BaseRedirect(RedirectView):
    @staticmethod
    def _get_obj(model, **kwargs):
        obj = model.objects.filter((Q(date_expire__gte=datetime.now()) | Q(date_expire=None)), **kwargs).first()
        if not obj:
            raise Http404
        return obj


    def _get_user_data(self, request, link):
        try:
            device = (str(request.user_agent).split('/')[0]).strip()
            meta = request.META.items()
            meta.sort()
            StatisticsModel.objects.create(
                link = link,
                user_agent_unparsed = request.headers['user-agent'],
                fingerprint = meta,
                device = device,
                os = request.user_agent.os.family,
                browser = request.user_agent.browser.family,
                ref_link = requester.extract_domain(request.META.get('HTTP_REFERER')),
                user_ip = request.META['REMOTE_ADDR']
            )
        except:
            pass


class GroupRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def _get_links_list(self, group):
        links = LinkModel.objects.filter((Q(date_expire__gte=datetime.now()) | Q(date_expire=None)), group=group, disabled=False)
        if not links:
            raise Http404
        return links

    def _get_rotation_url(self, group):
        links = self._get_links_list(group)
        link = random.choice(links)
        self._get_user_data(self.request, link)
        return link.long_link
    
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        group = self._get_obj(GroupLinkModel, slug=slug, disabled=False)
        if group.rotation and group.password is None:
            url = self._get_rotation_url(group)
            return HttpResponseRedirect(url)
        if group.password:
            form = self.form_class()
            return render(request, 'cutter/redirect_password.html', context={'form': form})
        links = self._get_links_list(group)
        return render(request, 'cutter/group_link_page.html', context={'group': group, 'links': links})
    
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        group = self._get_obj(GroupLinkModel, slug=slug, disabled=False)
        form_data = request.POST.dict()
        form_data.setdefault('encoded_pwd', group.password)
        form = self.form_class(form_data)
        if form.is_valid():
            if group.rotation:
                url = self._get_rotation_url(group)
                return HttpResponseRedirect(url)
            links = self._get_links_list(group)
            return render(request, 'cutter/group_link_page.html', context={'group': group, 'links': links})
        return render(request, 'cutter/redirect_password.html', context={'form': form})
    

class LinkRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        link = self._get_obj(LinkModel, slug=slug, disabled=False)
        if link.password:
            form = self.form_class()
            return render(request, 'cutter/redirect_password.html', context={'form': form})
        self._get_user_data(request, link)
        return HttpResponseRedirect(link.long_link)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        link = self._get_obj(LinkModel, slug=slug, disabled=False)
        form_data = request.POST.dict()
        form_data.setdefault('encoded_pwd', link.password)
        form = self.form_class(form_data)
        if form.is_valid():
            self._get_user_data(request, link)
            return HttpResponseRedirect(link.long_link)
        return render(request, 'cutter/redirect_password.html', context={'form': form})
        