import io

from django.shortcuts import get_object_or_404, render
from django.http import FileResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import get_user_model
from apps.home.forms import HomeCreateLinkForm
from django.contrib.auth.models import AbstractUser
from apps.db_model.models import GroupLinkModel, LinkModel

User = get_user_model()


class HomeView(View):
    form_class = HomeCreateLinkForm
    template_name = 'home/index.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'main_form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            if issubclass(request.user.__class__, AbstractUser):
                link.user = request.user
            link.save()
            return render(request, self.template_name, context = {'main_form': form, 'link': link})
        else:
            return render(request, self.template_name, context={'main_form': form})


class DownloadFile(View):
    allow_mime = ['png', 'svg']
    models = {'link': LinkModel, 'group': GroupLinkModel}

    def get_object(self, type, slug):
        model = self.models.get(type)
        return get_object_or_404(model, slug=slug)
    
    def get(self, request, model, slug):
        buffer = io.BytesIO()
        req_mime = request.GET.get('mime')
        if req_mime not in self.allow_mime:
            req_mime = 'png'
        obj = self.get_object(model, slug)
        buffer.write(getattr(obj, req_mime))
        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename='%s_qr.%s' % (slug, req_mime))
        return response
                                     


class FeaturesInfoView(TemplateView):
    template_name = 'home/features.html'


class BotInfoView(TemplateView):
    template_name = 'home/tg-bot.html'


class APIInfoView(TemplateView):
    template_name = 'home/api.html'