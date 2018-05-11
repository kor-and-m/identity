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


from django.contrib.auth import get_user_model

from user.serializers import UserSerializer
from scopes.models import Scope


class LoginView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def post(request):
        password = request.JSON.get('password', None)
        scope_name = request.JSON.get('scope_name', None)
        email = request.JSON.get('email', None)
        content_type = 'application/json'

        if email is None:
            return Response("Не передан email", status=400, content_type=content_type)

        if scope_name is None:
            return Response("Не передан scope_name", status=400, content_type=content_type)

        if password is None:
            return Response("Не передан password", status=400, content_type=content_type)

        user = auth.authenticate(email=email.lower(), password=password)

        if not user:
            return Response("Неверный логин или пароль", status=403, content_type=content_type)

        try:
            scope = Scope.objects.get(name=scope_name)
        except Scope.DoesNotExist:
            return Response("Не зарегестрированно такое приложение", status=404, content_type=content_type)

        response = Response(scope.set_token(user), status=200, content_type=content_type)

        return response


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
        payload_string = token_decoded[1]
        payload_string += "=" * ((4 - len(payload_string) % 4) % 4)
        payload = json.loads(base64.b64decode(payload_string).decode('utf-8'))
        alg = headers['alg']
        iss = payload['iss']

        try:
            scope = Scope.objects.get(name=iss)
        except Scope.DoesNotExist:
            return Response('Приложение не найдено', status=404)

        payload = jwt.decode(jwt_token, str(scope.secret), algorithms=[alg], audience='identity_server')

        if int(payload['exp']) < int(datetime.now().replace(tzinfo=timezone.utc).timestamp()):
            return Response('Ссылка просроченв', status=403)

        try:
            user = get_user_model().objects.get(email=payload['email'].lower())
            return Response(scope.set_token(user), status=200)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(email=payload['email'].lower(), password=payload['password'])
            return Response(scope.set_token(user), status=201)


    @staticmethod
    def post(request):
        email = request.JSON.get('email', None)
        password = request.JSON.get('password', None)
        iss = request.JSON.get('scope_name', None)
        back_url = request.JSON.get('back_url', '/')

        if email is None:
            return Response('email не передан', status=400)

        if iss is None:
            return Response('iss не передан', status=400)

        if password is None:
            return Response('password не передан', status=400)

        if get_user_model().objects.filter(email=email.lower()).exists():
            return Response('Пользователь с таким email уже зарегистрирован', status=403)

        try:
            scope = Scope.objects.get(name=iss)
        except Scope.DoesNotExist:
            return Response('Приложение не найдено', 404)

        token = jwt.encode({
            'aud': 'identity_server',
            'iss': iss,
            'exp': int((datetime.now() + timedelta(hours=24)).replace(tzinfo=timezone.utc).timestamp()),
            'email': email.lower(),
            'password': password,
        }, str(scope.secret), algorithm='HS256')

        body = {
            "subject": 'Подтвердите регистрацию',
            "body": '''
                Ваш пароль (он будет действителен после активации по ссылке) %s 
                для подтверждения регистрации перейдите по ссылке
                %s%s?token=%s она действительна
                в течении суток''' % (password, scope.domain, back_url, token),
                "from_email": 'gussman7777@gmail.com',
                "to": [email],
            }

        msg = EmailMessage(
            **body
        )
        msg.send()


        return Response(status=204)
        