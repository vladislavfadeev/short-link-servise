from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMessage



def send_email_verify(request, user):

    current_site = get_current_site(request)

    context = {
        'domain': current_site.domain,
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
        'protocol': 'http'
    }
    message = loader.render_to_string(
        'authuser/registration/email/email_verify.html',
        context=context,
    )
    email = EmailMessage(
        'Verify email',
        message,
        to=[user.email], 
    )
    email.send()



def get_redirect_url():

    try:
        from clkr_core.settings import LOGIN_REDIRECT_URL
        redirect_url = LOGIN_REDIRECT_URL
        
    except ImportError:
        redirect_url = None
        
    return redirect_url
