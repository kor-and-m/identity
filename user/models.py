from django.db import models
import uuid
import random
import string
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import EmailMessage


class Profile(models.Model):
    user = models.OneToOneField(
		to=settings.AUTH_USER_MODEL, verbose_name="Связная модель пользователя", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="Имя", null=True, blank=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", null=True, blank=True)
    avatar = models.ImageField(upload_to='user_photo/', null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    def __str__(self):
    	return self.user.email
		
    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Информация по профилям')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, groups=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password is None:
            password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        user.set_password(password)
        user.save(using=self._db)
        if not groups is None:
        	for g in Role.objects.filter(name__in=groups):
        		user.groups.add(g)

        body = {
            "subject": 'Спасибо за регистрацию',
            "body": '''вы были успешно зарегистрированны''',
            "from_email": 'gussman7777@gmail.com',
            "to": [email],
        }

        msg = EmailMessage(
            **body
        )

        try:
            msg.send()
        except Exception as e:
            pass
        
        Profile.objects.create(user=user, **extra_fields)
        return user

    def create_user(self, email, groups=[], password=None, **extra_fields):
        return self._create_user(email, password, groups, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, ['staff', 'admin'], **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, verbose_name="email", unique=True)
    out_key = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Внешний ключ", unique=True)
    groups = models.ManyToManyField(to="Role", verbose_name="Роли пользователя")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_superuser(self):
      return self.groups.filter(name='admin').exists()

    @property
    def is_staff(self):
      return self.groups.filter(name='staff').exists()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Role(models.Model):
    name = models.CharField(_('Название роли'), max_length=30)
    description = models.TextField(_('Описание'), max_length=30)

    class Meta:
        verbose_name = _('Роль')
        verbose_name_plural = _('Роли')

    def __str__(self):
    	return self.name
