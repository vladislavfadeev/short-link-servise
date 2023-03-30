from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import StreamingHttpResponse, Http404
from django.views.generic.base import (RedirectView,
                                       TemplateView,
                                       )
from django.views import View
from clkr_core import settings
from apps.home.forms import LinkModelForm
from apps.db_model.models import (LinkModel,
                     LinkTransitionsModel
                     )
import mimetypes
import os




class HomeView(View):

    def get(self, request):

        form = LinkModelForm()
        return render(request, 'home/index.html', context={'form': form})
    
    def post(self, request):
        form = LinkModelForm(request.POST)

        if form.is_valid():
            slug_uniq = LinkModel.make_slug()
            obj = LinkModel.objects.filter(slug=slug_uniq).exists()

            if not obj:
                LinkModel.make_qr(slug_uniq)
                char = LinkModel(
                            slug=slug_uniq,
                            long_link=form.cleaned_data['long_link'],
                            statistics=form.cleaned_data['statistics']
                            )
                char.save()
                return render(request, 'home/index.html',
                              context = {'form': form, 
                                         'object': char
                                         })
            
            else:
                while obj:
                    slug_uniq = LinkModel.make_slug()
                    obj = LinkModel.objects.filter(slug=slug_uniq).exists()

                LinkModel.make_qr(slug_uniq)
                char = LinkModel(
                            slug=slug_uniq,
                            long_link=form.cleaned_data['long_link'],
                            statistics=form.cleaned_data['statistics']
                            )
                char.save()
                return render(request, 'home/index.html',
                              context = {'form': form, 
                                         'object': char
                                         })
        else:
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