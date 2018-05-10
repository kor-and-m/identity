from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('out_key', 'email', 'first_name', 'last_name', 'avatar')

    @staticmethod
    def get_first_name(self):
        return self.profile.first_name

    @staticmethod
    def get_last_name(self):
        return self.profile.last_name

    @staticmethod
    def get_avatar(self):
        try:
            url = self.profile.avatar.url
        except ValueError:
            url = None
        return url
