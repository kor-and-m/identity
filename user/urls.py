from django.urls import path
from user import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('set-token/', auth_views.SetTokenView.as_view(), name='set-token'),
    path('registration/', auth_views.RegistrationView.as_view(), name='registration'),
]