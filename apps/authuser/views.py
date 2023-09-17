from django.contrib.sites.shortcuts import get_current_site

from allauth.account.views import ConfirmEmailView


class MyConfirmEmailView(ConfirmEmailView):
    # Current method was rewrited because if in confirmation
    # url has mistake server return 500 error.
    # If server can not find related user in self object have not
    # exist 'email_adress' attribute and in this case raise 
    # 'AttributeNotExist' error.
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
