from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from users.models import UserToken
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_email_task(subject, email_address, email_body):
    email = EmailMultiAlternatives(
        subject,
        strip_tags(email_body),
        settings.EMAIL_HOST_USER,
        [email_address],
    )
    email.attach_alternative(email_body, "text/html")
    return email.send()


@shared_task 
def remove_tokens():
    # remove tokens older than two days 
    UserToken.objects.filter(created_at__lt=timezone.now()-timedelta(days=2)).delete()
    