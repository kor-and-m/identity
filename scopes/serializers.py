from rest_framework import serializers
from scopes.models import Scope, ScopeStyles
from user.serializers import UserSerializer


class ScopeStylesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScopeStyles
        fields = '__all__'


class ScopeSerializer(serializers.ModelSerializer):
    styles = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Scope
        exclude = ('secret',)

    @staticmethod
    def get_styles(self):
        return None if self.styles is None else ScopeStylesSerializer(self.styles).data

    @staticmethod
    def get_author(self):
        return None if self.author is None else UserSerializer(self.author).data

