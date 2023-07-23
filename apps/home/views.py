from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth import get_user_model
from clkr_core import settings
from apps.home.forms import HomeCreateLinkForm
import mimetypes
import os 

User = get_user_model()


class HomeView(View):
    form_class = HomeCreateLinkForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'home/index.html', context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user if isinstance(request.user, User) else None
            setattr(form, 'user', user)
            link = form.save()
            return render(request, 'home/index.html', context = {'form': form, 'link': link})
        else:
            print('else')
            return render(request, 'home/index.html', context={'form': form})



def download_qr(request, file):
    fl_path = f'{settings.MEDIA_ROOT}/{file}'
    response = StreamingHttpResponse(open(fl_path, 'rb'),
                                     content_type = mimetypes.guess_type(fl_path))
    response['Content-Length'] = os.path.getsize(fl_path)
    response['Content-Disposition'] = "Attachment; filename=%s" % file
    return response
                                     


class FeaturesInfoView(TemplateView):
    template_name = 'home/features.html'


class BotInfoView(TemplateView):
    template_name = 'home/tg-bot.html'


class APIInfoView(TemplateView):
    template_name = 'home/api.html'