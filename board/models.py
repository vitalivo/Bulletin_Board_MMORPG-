from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
# Create your models here.

CATEGORY_CHOICES = [
    ('tanks', 'Танки'),
    ('healers', 'Хилы'),
    ('dd', 'ДД'),
    ('traders', 'Торговцы'),
    ('guildmasters', 'Гилдмастеры'),
    ('questgivers', 'Квестгиверы'),
    ('blacksmiths', 'Кузнецы'),
    ('leatherworkers', 'Кожевники'),
    ('alchemists', 'Зельевары'),
    ('spellmasters', 'Мастера заклинаний'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name='Категория')

    def __str__(self):
        return self.get_name_display()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content_text = RichTextField(verbose_name='Контент')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')


    def get_absolute_url(self):
        return reverse('board:post-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    content = models.TextField(verbose_name='Контент')  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    accepted = models.BooleanField(default=False, verbose_name='Принят')

    def __str__(self):
        return f'От {self.user.username} на "{self.post.title}"'
