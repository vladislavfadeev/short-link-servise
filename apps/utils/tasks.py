from celery import shared_task


@shared_task(bind=True)
def celery_email_send(self, msg):
    msg.send()
    return "OK"
