from django.http.response import HttpResponseNotFound
from django.contrib.sites.shortcuts import get_current_site

from allauth.account.views import ConfirmEmailView


def page_does_not_exist(request):
    return HttpResponseNotFound


class MyConfirmEmailView(ConfirmEmailView):
    def get_context_data(self, **kwargs):
        ctx = kwargs
        site = get_current_site(self.request)
        if self.object:
            upd_data = {
                "site": site,
                "confirmation": self.object,
                "can_confirm": self.object.email_address.can_set_verified(),
                "email": self.object.email_address.email,
            }
        else:
            upd_data = {
                "site": site,
                "confirmation": None,
                "can_confirm": None,
                "email": None,
            }
        return ctx.update(upd_data)
