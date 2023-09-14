from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task
def celery_email_send(subject, body, alternatives, from_email, to, extra_headers):
    msg = EmailMultiAlternatives(subject, body, from_email, to, extra_headers)
    if alternatives:
        templ, mime = alternatives[0]
    msg.attach_alternative(templ, mime)
    msg.send()
    return "OK"
