# Generated by Django 5.1.5 on 2025-01-24 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_category_alter_subscription_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('tanks', 'Танки'), ('healers', 'Хилы'), ('dd', 'ДД'), ('traders', 'Торговцы'), ('guildmasters', 'Гилдмастеры'), ('questgivers', 'Квестгиверы'), ('blacksmiths', 'Кузнецы'), ('leatherworkers', 'Кожевники'), ('alchemists', 'Зельевары'), ('spellmasters', 'Мастера заклинаний')], max_length=100, verbose_name='Категория'),
        ),
    ]
