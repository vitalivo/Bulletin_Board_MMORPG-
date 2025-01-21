# signals.py

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Post  # Убедитесь, что модель Post импортирована

User = get_user_model()

@receiver(post_save, sender=User)
def add_permissions(sender, instance, created, **kwargs):
    if created:
        # Добавьте пользователя в группу, если она есть
        group, _ = Group.objects.get_or_create(name='Editors')
        instance.groups.add(group)

        # Добавьте права на создание и изменение объявлений
        content_type = ContentType.objects.get_for_model(Post)  # Используем модель Post для ContentType
        permissions = Permission.objects.filter(content_type=content_type, codename__in=['add_post', 'change_post'])
        instance.user_permissions.add(*permissions)
