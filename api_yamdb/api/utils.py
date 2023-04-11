from django.conf import settings
from django.core.mail import send_mail


def send_mail_to_user(email, confirmation_code):
    send_mail(
        'Код подтверждения YaMDb',
        f'Your confirmation_code: {confirmation_code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
