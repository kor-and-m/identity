from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from django.contrib.auth import get_user_model

from scopes.serializers import ScopeSerializer
from scopes.models import Scope


class ScopesView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    @staticmethod
    def get(request):
        return Response([ScopeSerializer(scope).data for scope in Scope.objects.all()], status=200)

    @staticmethod
    def post(request):
        data = dict(request.JSON)
        data['author'] = request.user
        scope = ScopeSerializer().create(data)
        return Response(scope, status=200)
