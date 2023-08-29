import io

from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import get_user_model
from apps.home.forms import HomeCreateLinkForm, QRGeneratorForm
from django.contrib.auth.models import AbstractUser
from apps.db_model.models import GroupLinkModel, LinkModel, QRCodeModel
from apps.utils.info_normalizer import get_user_info

User = get_user_model()


class HomeView(View):
    form_class = HomeCreateLinkForm
    template_name = "home/index.html"

    def get(self, request):
        return render(
            request, self.template_name, context={"main_form": self.form_class}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            if issubclass(request.user.__class__, AbstractUser):
                link.user = request.user
            link.user_info = get_user_info(request)
            link.save()
            return render(
                request, self.template_name, context={"main_form": form, "link": link}
            )
        return render(request, self.template_name, context={"main_form": form})


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
            qrcode.user_info = get_user_info(request)
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


class BotInfoView(TemplateView):
    template_name = "home/tg-bot.html"


class APIInfoView(TemplateView):
    template_name = "home/api.html"
