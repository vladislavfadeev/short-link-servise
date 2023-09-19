from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from apps.utils.tasks import celery_email_send


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        celery_email_send.delay(
            msg.subject,
            msg.body,
            msg.alternatives,
            msg.from_email,
            msg.to,
            msg.extra_headers,
        )

    def validate_unique_email(self, email):
        from allauth.account.models import EmailAddress

        if EmailAddress.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.error_messages["email_taken"])
        return email
