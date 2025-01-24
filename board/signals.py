# signals.py
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

@receiver(post_save, sender=Post)
def send_newsletter(sender, instance, created, **kwargs):
    if not created:
        return
    emails = User.objects.filter(
        subscriptions__category=instance.category
    ).values_list('email', flat=True)

    subject = f'Новое объявление на нашем ресурсе {instance.title}'
    text_content = (
        f'Новое объявление: {instance.title}\n'
        f'В категории: {instance.category}\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{instance.get_absolute_url()}\n'
    )
    html_content = (
        f'Новое объявление: {instance.title}<br>'
        f'В категории: {instance.category}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">Ссылка на объявление</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



