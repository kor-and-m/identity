from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.contrib import auth
import base64
import jwt
import json
from datetime import datetime, timedelta, timezone
from django.core.mail import EmailMessage
from django.shortcuts import redirect


from django.contrib.auth import get_user_model

from user.serializers import UserSerializer
from scopes.models import Scope


class LoginView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def post(request):
        password = request.JSON.get('password', None)
        email = request.JSON.get('email', None)

        if email is None:
            return Response("Не передан email", status=400)

        if password is None:
            return Response("Не передан password", status=400)

        user = auth.authenticate(email=email.lower(), password=password)

        if not user:
            return Response("Неверный логин или пароль", status=403)

        token = jwt.encode({
            'iss': 'identity_server',
            'aud': 'identity_server',
            'exp': int((datetime.now() + timedelta(hours=720)).replace(tzinfo=timezone.utc).timestamp()),
            'out_key': str(user.out_key),
            'email': user.email,
            'roles': [i.name for i in user.groups.all()],
        }, settings.SECRET_KEY, algorithm='HS256')

        response = Response(token, status=200)

        return response


class SetTokenView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def get(request):
        scope_name = request.GET.get('scope_name', None)

        if scope_name is None:
            return redirect('/')

        if not request.user.is_authenticated:
            return redirect('/')

        try:
            scope=Scope.objects.get(name=scope_name)
        except Scope.DoesNotExist:
            return redirect('/')

        return redirect('%s?token=%s' % (scope.back_url, scope.set_token(request.user)))


class RegistrationView(APIView): 
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def get(request):
        jwt_token = request.GET.get('token', None)

        if jwt_token is None:
            return Response('token не передан', status=400)

        token_decoded = jwt_token.split('.')

        headers_string = base64.b64decode(token_decoded[0]).decode('utf-8')
        headers = json.loads(headers_string)
        alg = headers['alg']

        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=[alg], audience='identity_server')

        if int(payload['exp']) < int(datetime.now().replace(tzinfo=timezone.utc).timestamp()):
            return Response('Ссылка просроченв', status=403)

        try:
            user = get_user_model().objects.get(email=payload['email'].lower())

        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(email=payload['email'].lower(), password=payload['password'])

        token = jwt.encode({
            'iss': 'identity_server',
            'aud': 'identity_server',
            'exp': int((datetime.now() + timedelta(hours=720)).replace(tzinfo=timezone.utc).timestamp()),
            'out_key': str(user.out_key),
            'email': user.email,
            'roles': [i.name for i in user.groups.all()],
        }, settings.SECRET_KEY, algorithm='HS256')
        response = redirect('/')
        response.set_cookie('AUTH_COOKIE', token)
        return response


    @staticmethod
    def post(request):
        email = request.JSON.get('email', None)
        password = request.JSON.get('password', None)

        if email is None:
            return Response('email не передан', status=400)

        if password is None:
            return Response('password не передан', status=400)

        if get_user_model().objects.filter(email=email.lower()).exists():
            return Response('Пользователь с таким email уже зарегистрирован', status=403)

        token = jwt.encode({
            'aud': 'identity_server',
            'iss': 'identity_server',
            'exp': int((datetime.now() + timedelta(hours=24)).replace(tzinfo=timezone.utc).timestamp()),
            'email': email.lower(),
            'password': password,
        }, settings.SECRET_KEY, algorithm='HS256')

        body = {
            "subject": 'Подтвердите регистрацию',
            "body": '''
                Ваш пароль (он будет действителен после активации по ссылке) %s 
                для подтверждения регистрации перейдите по ссылке
                /api/auth/registration/?token=%s она действительна
                в течении суток''' % (password, token),
                "from_email": 'gussman7777@gmail.com',
                "to": [email],
            }

        msg = EmailMessage(
            **body
        )
        msg.send()


        return Response(status=204)
        