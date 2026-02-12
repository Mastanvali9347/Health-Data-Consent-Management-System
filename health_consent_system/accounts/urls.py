from django.urls import path
from django.contrib.auth import logout
from django.shortcuts import redirect

from .views import (
    login_page,
    register_page,
    LoginAPIView,
    RegisterAPIView,
    ProfileView
)

urlpatterns = [
    path('login/', login_page),
    path('register/', register_page),
    path('logout/', lambda request: (logout(request), redirect('/auth/login/'))[1]),

    path('api/login/', LoginAPIView.as_view()),
    path('api/register/', RegisterAPIView.as_view()),
    path('profile/', ProfileView.as_view()),
]
