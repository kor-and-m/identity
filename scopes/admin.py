from django.contrib import admin

from scopes.models import Scope, ScopeStyles

admin.site.register(Scope)
admin.site.register(ScopeStyles)