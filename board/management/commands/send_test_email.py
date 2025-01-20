from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a test email'

    def handle(self, *args, **kwargs):
        subject = 'Тестовое письмо'
        message = 'Это тестовое письмо для проверки отправки одноразового кода.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['vitalivoloshin1975@yandex.co.il']  # Измените на адрес вашей электронной почты

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Тестовое письмо отправлено успешно!'))
