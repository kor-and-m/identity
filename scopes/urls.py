from django.urls import path
from scopes import views as scopes_views

urlpatterns = [
    path('', scopes_views.ScopesView.as_view(), name='scopes'),
]