import random
from datetime import datetime

from celery.result import AsyncResult

from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.db_model.models import GroupLinkModel, LinkModel, StatisticsModel
from apps.cutter.forms import RedirectPasswordForm
from apps.cutter.tasks import make_link_task
from apps.utils import requester
from apps.utils.info_normalizer import get_user_info
from apps.dashboard.forms import DashboardLinkForm


class BaseRedirect(RedirectView):
    @staticmethod
    def _get_obj(model, **kwargs):
        obj = model.objects.filter(
            (Q(date_expire__gte=datetime.now()) | Q(date_expire=None)), **kwargs
        ).first()
        if not obj:
            raise Http404
        return obj

    def _get_user_data(self, request, link):
        try:
            device = (str(request.user_agent).split("/")[0]).strip()
            # meta = request.META.items()
            # meta.sort()
            StatisticsModel.objects.create(
                link=link,
                user_agent_unparsed=str(request.user_agent),
                # fingerprint=meta,
                device=device,
                os=str(request.user_agent.os.family),
                browser=str(request.user_agent.browser.family),
                ref_link=requester.extract_domain(request.META.get("HTTP_REFERER")),
                user_ip=str(request.META.get("REMOTE_ADDR", "Not defined")),
            )
        except:
            pass


class GroupRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def _get_links_list(self, group):
        links = LinkModel.objects.filter(
            (Q(date_expire__gte=datetime.now()) | Q(date_expire=None)),
            group=group,
            disabled=False,
        )
        if not links:
            raise Http404
        return links

    def _get_rotation_url(self, group):
        links = self._get_links_list(group)
        link = random.choice(links)
        self._get_user_data(self.request, link)
        return link.long_link

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        group = self._get_obj(GroupLinkModel, slug=slug, disabled=False)
        if group.rotation and group.password is None:
            url = self._get_rotation_url(group)
            return HttpResponseRedirect(url)
        if group.password:
            form = self.form_class()
            return render(
                request, "cutter/redirect_password.html", context={"form": form}
            )
        links = self._get_links_list(group)
        return render(
            request,
            "cutter/group_link_page.html",
            context={"group": group, "links": links},
        )

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        group = self._get_obj(GroupLinkModel, slug=slug, disabled=False)
        form_data = request.POST.dict()
        form_data.setdefault("encoded_pwd", group.password)
        form = self.form_class(form_data)
        if form.is_valid():
            if group.rotation:
                url = self._get_rotation_url(group)
                return HttpResponseRedirect(url)
            links = self._get_links_list(group)
            return render(
                request,
                "cutter/group_link_page.html",
                context={"group": group, "links": links},
            )
        return render(request, "cutter/redirect_password.html", context={"form": form})


class LinkRedirect(BaseRedirect):
    form_class = RedirectPasswordForm

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        link = self._get_obj(LinkModel, slug=slug, disabled=False)
        if link.password:
            form = self.form_class()
            return render(
                request, "cutter/redirect_password.html", context={"form": form}
            )
        self._get_user_data(request, link)
        return HttpResponseRedirect(link.long_link)

    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        link = self._get_obj(LinkModel, slug=slug, disabled=False)
        form_data = request.POST.dict()
        form_data.setdefault("encoded_pwd", link.password)
        form = self.form_class(form_data)
        if form.is_valid():
            self._get_user_data(request, link)
            return HttpResponseRedirect(link.long_link)
        return render(request, "cutter/redirect_password.html", context={"form": form})


class CreateLinkView(View):
    form_class = DashboardLinkForm

    @csrf_exempt
    def post(self, request):
        form = self.form_class(request.POST, initial={})
        if form.is_valid():
            location = request.POST.get("location")
            uid = request.COOKIES.get("_uid")
            form_data = form.cleaned_data
            force = form_data.pop("force")
            if request.user.is_authenticated:
                form_data["user_id"] = request.user.id
            user_info = get_user_info(request)
            task = make_link_task.delay(form_data, user_info, force, location, uid)
            return JsonResponse({"task_id": task.id}, status=202)
        return JsonResponse({"errors": form.errors.as_ul()}, status=422)


class TaskStatusView(View):
    def get(self, request, task_id, *args, **kwargs):
        task = AsyncResult(task_id)
        status = 202
        if task.successful():
            status = 200
        elif task.failed():
            status = 422
        result = {
            "task_id": task_id,
            "task_status": task.status,
            "task_result": str(task.result),
        }
        return JsonResponse(result, status=status)
