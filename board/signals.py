# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def send_newsletter(sender, instance, created, **kwargs):
    if created:
        # Используем шаблон для письма с новостной рассылкой
        message = render_to_string('email/newsletter.txt', {'user': instance})
        send_mail(
            subject='Добро пожаловать на наш ресурс',
            message=message,
            from_email='vitalivoloshin1975@yandex.co.il',
            recipient_list=[instance.email],
        )


