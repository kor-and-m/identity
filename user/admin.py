from django.contrib import admin

from user.models import User, Role, Profile

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Profile)
