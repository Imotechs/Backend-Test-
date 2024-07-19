from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.conf import settings
from .tokens import account_activation_token

from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()
host_user = settings.EMAIL_HOST_USER



def send_verification_email(user):
        mail_subject = "Email verification"
        message = render_to_string( "registration/account-activation.html", {
            'user': user,
            'domain': settings.FRONTEND_URL,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        from_email = f'no-Reply <{host_user}>'
        to_email = user.email
        send_mail(mail_subject, message, from_email, [to_email], html_message=message)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Send verification email on registration"""
    if created:
        send_verification_email(instance)