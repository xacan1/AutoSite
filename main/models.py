from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Диспетчер пользовательских моделей, в котором email используется для аутентификации вместо username.
    Создание и запись пользователя  и суперпользователя с email и password
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(max_length=150, blank=True, verbose_name='Организация')
    phone = models.CharField(max_length=12, unique=True, blank=True, verbose_name='Телефон')
    inn = models.CharField(max_length=12, blank=True, verbose_name='ИНН')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    request_limit = models.IntegerField(null=False, default=100, verbose_name='Лимит запросов')
    cost_per_hour = models.DecimalField(max_digits=15, decimal_places=2, null=False, default=1000, verbose_name='Стоимость часа')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=250, unique=True, blank=False, verbose_name='Заголовок')
    content = models.TextField(blank=False, verbose_name='Текст')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата поста')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-time_create']
