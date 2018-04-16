from django.db import models
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from django.utils.translation import ugettext_lazy as _

class Scope(models.Model):
    name = models.CharField(_('Название зоны'), max_length=30)
    back_url = models.URLField(_('Обратный адрес зоны'), max_length=255)
    hours_exp = models.SmallIntegerField(_('Часов до сгорания токена'), default=168)
    secret = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Внешний ключ", unique=True)
    icon = models.ImageField(_('Иконка зоны'), upload_to='scopes/icon', blank=True, null=True)

    def set_token(self, user):
    	return jwt.encode({
    		'iss': 'identity_skillbox',
    		'aud': self.name,
    		'exp': int((datetime.now() + timedelta(hours=self.hours_exp)).replace(tzinfo=timezone.utc).timestamp()),
    		'out_key': str(user.out_key),
    		'email': user.email,
    		'roles': [i.name for i in user.groups.all()],
    	}, str(self.secret), algorithm='HS256')

    class Meta:
        verbose_name = _('Зона')
        verbose_name_plural = _('Зоны')

    def __str__(self):
    	return self.name
