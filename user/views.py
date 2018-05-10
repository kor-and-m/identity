from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.contrib import auth
import base64

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

        response = Response(scope.set_token(user), status=201, content_type=content_type)

        return response


class LogoutView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def post(request):
        response = Response(status=204)
        if request.user.is_authenticated:
            response.delete_cookie('AUTH_COOKIE')
        return response


# auth

# class RegistrationView(APIView): 
#     renderer_classes = (JSONRenderer,)

#     @staticmethod
#     def get(request):
#         try:
#             invite = Invite.objects.get(hash=request.GET['hash'])
#             invite.owner.is_active = True
#             invite.owner.save()
#             auth.login(request, invite.owner)
#             invite.delete()
#             return redirect('/')
#         except Invite.DoesNotExist:
#             return Response('Приглошения не существует возможно оно сгорело', status=404)

#     @staticmethod
#     def post(request):
#     	base64.b64decode(settings.SECRET_KEY)
#     	settings.SECRET_KEY
#     	email=request.JSON['email'].lower()
#     	password = request.JSON.get('password')
#         if password:
#             user = get_user_model().objects.create_user(
#                 email=email,
#                 password=password,
#             )
#         else:
#             user = get_user_model().objects.create_user(
#                 email=email,
#             )

#         return Response(UserSelfSerializer(user).data, status=200)

