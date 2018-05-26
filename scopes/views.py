from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from django.conf import settings

from django.contrib.auth import get_user_model

from scopes.serializers import ScopeSerializer
from scopes.models import Scope


class ScopesView(APIView):
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    parser_classes = (MultiPartParser, )


    @staticmethod
    def get(request):
        return Response([ScopeSerializer(scope).data for scope in Scope.objects.all()], status=200)

    @staticmethod
    def post(request):
        data = request.POST.dict()
        data['icon'] = request.FILES.get('icon')
        data['author'] = request.user
        scope = ScopeSerializer().create(data)
        return Response(ScopeSerializer(scope).data, status=200)
