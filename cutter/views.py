from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import StreamingHttpResponse, Http404
from django.views.generic.base import (RedirectView,
                                       TemplateView,
                                       )
from django.views import View
from short_link import settings
from .forms import LinkModelForm
from .models import (LinkModel,
                     LinkTransitionsModel
                     )
import mimetypes
import os


class HomeView(View):
    
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
                return render(request, 'cutter/home.html',
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
                return render(request, 'cutter/home.html',
                              context = {'form': form, 
                                         'object': char
                                         })
        else:
            return render(request, 'cutter/home.html', context={'form': form})


    def get(self, request):

        form = LinkModelForm()
        return render(request, 'cutter/home.html', context={'form': form})



class RedirectSlug(RedirectView):

    def get_redirect_url(self, *args, **kwargs):

        slug = kwargs.get('slug')
        request = self.request
        link = LinkModel.objects.filter(slug=slug).first()

        if link:
            try:

                device = (str(request.user_agent).split('/')[0]).strip()
                LinkTransitionsModel.objects.create(
                    link = link,
                    user_agent_unparsed = request.headers['user-agent'],
                    device = device,
                    os = request.user_agent.os.family,
                    browser = request.user_agent.browser.family,
                    ref_link = request.META.get('HTTP_REFERER'),
                    user_ip = request.META['REMOTE_ADDR']
                ).save()
                return link.long_link
            
            except Exception as e:
                return link.long_link
            
        else:
            raise Http404()


# class CreateAccountView(TemplateView):

#     template_name = 'registration/sign_up.html'

#     def get(self, request):
#         context = {
#             'form': UserCreationForm()
#         }
#         return render(request, self.template_name, context)




def download_file(request, file):
    fl_path = f'{settings.MEDIA_ROOT}/{file}'
    response = StreamingHttpResponse(open(fl_path, 'rb'),
                                     content_type = mimetypes.guess_type(fl_path))
    response['Content-Length'] = os.path.getsize(fl_path)
    response['Content-Disposition'] = "Attachment; filename=%s" % file
    return response
                                     

def test(request):
    return render(request, 'cutter/test.html')


class FeaturesInfoView(TemplateView):
    template_name = 'cutter/features.html'


class BotInfoView(TemplateView):
    template_name = 'cutter/tg-bot.html'


class APIInfoView(TemplateView):
    template_name = 'cutter/api.html'
