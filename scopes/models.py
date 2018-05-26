from django.db import models
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class ScopeStyles(models.Model):
    url_to_main = models.URLField(_('Стили контейнера'), max_length=255, blank=True, null=True)
    url_to_login = models.URLField(_('Стили формы авторизации'), max_length=255, blank=True, null=True)
    url_to_registration = models.URLField(_('Стили формы регистрации'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Стилизация зоны')
        verbose_name_plural = _('Стилизация зон')


class Scope(models.Model):
    name = models.AutoField(_('Название зоны'), primary_key=True, unique=True)
    title = models.CharField(_('Заголовок зоны'), max_length=255, unique=True)
    description = models.TextField(_('Описание зоны'), blank=True, null=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name=('Автор'), on_delete=models.CASCADE)
    styles = models.ForeignKey(
        to='ScopeStyles', verbose_name=('Кастомные стили'), on_delete=models.CASCADE, blank=True, null=True)
    back_url = models.URLField(_('Домен зоны'), max_length=255)
    hours_exp = models.PositiveSmallIntegerField(_('Часов до сгорания токена'), default=168)
    secret = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Внешний ключ", unique=True)
    icon = models.ImageField(_('Иконка зоны'), upload_to='scopes/icon', blank=True, null=True,
        width_field=1200, height_field=800)

    def get_exp(self, user):
        return (datetime.now() + timedelta(hours=self.hours_exp)).replace(tzinfo=timezone.utc)

    def set_token(self, user):
    	return jwt.encode({
    		'iss': self.name,
    		'aud': 'identity_server',
    		'exp': int(self.get_exp(user).timestamp()),
    		'out_key': str(user.out_key),
    		'email': user.email,
    		'roles': [i.name for i in user.groups.all()],
    	}, str(self.secret), algorithm='HS256')

    class Meta:
        verbose_name = _('Зона')
        verbose_name_plural = _('Зоны')

    def __str__(self):
    	return str(self.name)  
