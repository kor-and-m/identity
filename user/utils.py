from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from scopes.models import Scope
import jwt, base64, json
from datetime import datetime, timezone
from django.conf import settings


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('AUTH_COOKIE', None)
        if jwt_token is None:
            return None

        token_decoded = jwt_token.split('.')
        
        if not len(token_decoded) == 3:
            return None

        headers = json.loads(base64.b64decode(token_decoded[0]))
        alg = headers['alg']

        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[alg], audience='identity_server')

        if payload['exp'] is None:
            return None

        if int(payload['exp']) < int(datetime.now().replace(tzinfo=timezone.utc).timestamp()):
            return None

        try:
            user = get_user_model().objects.get(out_key=payload['out_key']) 
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
