from smtplib import SMTPException
from venv import logger

from allauth.account.forms import SignupForm
from allauth.account.models import EmailAddress
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.core.mail import send_mail



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )



class CustomSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        user.save()

        # Назначение разрешений пользователю
        permissions = ['add_post', 'change_post', 'delete_post', 'add_comment', 'change_comment', 'delete_comment', 'view_comment']
        for perm in permissions:
            permission = Permission.objects.get(codename=perm)
            user.user_permissions.add(permission)

        # Проверка и настройка адреса электронной почты пользователя
        (email_address, created) = EmailAddress.objects.get_or_create(user=user, email=user.email)
        if created:
            email_address.send_confirmation(request)

        # Отправка приветственного письма с логированием ошибок
        try:
            send_mail(
                subject='Добро пожаловать на наш ресурс',
                message=f'Вы зарегистрированы как: {user.username}',
                from_email='ваш_email@gmail.com',
                recipient_list=[user.email],
            )
        except SMTPException as e:
            logger.error(f"SMTPException: {e}")
        except Exception as e:
            logger.error(f"Exception: {e}")

        return user



