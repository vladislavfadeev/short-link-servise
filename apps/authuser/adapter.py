from allauth.account.adapter import DefaultAccountAdapter
from apps.utils.tasks import celery_email_send


class MyAccountAdapter(DefaultAccountAdapter):
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
