from django.http import  Http404
from django.views.generic.base import RedirectView

from apps.db_model.models import (
    LinkModel,
    LinkTransitionsModel
)



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

