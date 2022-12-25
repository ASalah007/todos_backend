from django.template.loader import render_to_string

from .tasks import send_email_task


def send_verification_email(recipient, message):
    context = {"recipient": recipient, "message": message}
    email_subject = "Verification"
    email_body = render_to_string("verification_email.html", context)
    send_email_task.delay(email_subject, recipient, email_body)


def send_reset_password_email(recipient, message):
    email_subject = "Reset Password"
    email_body = render_to_string("reset_password.html", {"message": message})
    send_email_task.delay(email_subject, recipient, email_body)

