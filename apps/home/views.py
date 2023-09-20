import io
from typing import Any
from django.db.models.query import QuerySet

from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from apps.home.forms import HomeCreateLinkForm, QRGeneratorForm
from apps.db_model.models import GroupLinkModel, LinkModel, QRCodeModel, UserInfoModel
from apps.utils.info_normalizer import get_user_info

User = get_user_model()


class HomeView(ListView):
    form_class = HomeCreateLinkForm
    template_name = "home/index.html"
    context_object_name = "links"
    paginate_by = 5
    ordering = "-date_created"
    model = LinkModel

    def get_queryset(self) -> QuerySet[Any]:
        uid = self.request.COOKIES.get("_uid")
        self.queryset = self.model.objects.filter(unauth_relation__exact=uid)
        return super().get_queryset()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["form"] = self.form_class
        return super().get_context_data(**kwargs)


class QRGeneratorView(View):
    form_class = QRGeneratorForm
    template_name = "home/qr_generator.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={"form": self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            qrcode = form.save(commit=False)
            if issubclass(request.user.__class__, AbstractUser):
                qrcode.user = request.user
            qrcode.user_info = UserInfoModel(**get_user_info(request)).save()
            qrcode.save()
            return render(
                request, self.template_name, context={"form": form, "qrcode": qrcode}
            )
        return render(request, self.template_name, context={"form": form})


class DownloadFile(View):
    allow_mime = ["png", "svg"]
    models = {"link": LinkModel, "group": GroupLinkModel, "qrcode": QRCodeModel}

    def get_object(self, type, slug):
        model = self.models.get(type)
        return get_object_or_404(model, slug=slug)

    def get(self, request, model, slug):
        buffer = io.BytesIO()
        req_mime = request.GET.get("mime")
        if req_mime not in self.allow_mime:
            req_mime = "png"
        obj = self.get_object(model, slug)
        buffer.write(getattr(obj, req_mime))
        buffer.seek(0)
        response = FileResponse(
            buffer, as_attachment=True, filename="%s_qr.%s" % (slug, req_mime)
        )
        return response


class APIInfoView(TemplateView):
    template_name = "home/api.html"
