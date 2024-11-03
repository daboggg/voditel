from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    return f'users/{instance.username}/{filename}'


class User(AbstractUser):
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Фотография')
    date_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')



