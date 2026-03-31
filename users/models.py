from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, password=None, role='student'):
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        if not full_name:
            raise ValueError('Имя обязательно')
        if not password:
            raise ValueError('Пароль обязателен')

        user = self.model(
            phone_number=phone_number,
            full_name=full_name,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password=None):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            role='admin'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('psychologist', 'Психолог'),
        ('admin', 'Администратор'),
    ]

    full_name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name='Роль')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Доступ в админку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.full_name} ({self.phone_number})'
