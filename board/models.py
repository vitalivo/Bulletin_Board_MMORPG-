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

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')  # Заголовок объявления
    content_text = RichTextField(verbose_name='Контент')  # Используем RichTextField для медиа-контента
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')  # Категория объявления
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # Автор объявления
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')  # Дата и время создания объявления
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')  # Дата и время последнего обновления объявления


    def get_absolute_url(self):
        return reverse('board:post-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')  # Объявление, к которому относится комментарий
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')  # Автор комментария
    content = models.TextField(verbose_name='Контент')  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано') # Дата и время создания комментария
    accepted = models.BooleanField(default=False, verbose_name='Принят')  # Флаг принятого комментария

    def __str__(self):
        return f'От {self.user.username} на "{self.post.title}"'
