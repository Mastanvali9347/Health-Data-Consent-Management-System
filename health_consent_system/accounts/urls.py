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

def logout_view(request):
    logout(request)
    return redirect("/auth/login/")

urlpatterns = [
    path("login/", login_page, name="login_page"),
    path("register/", register_page, name="register_page"),
    path("logout/", logout_view, name="logout"),

    path("api/login/", LoginAPIView.as_view(), name="api_login"),
    path("api/register/", RegisterAPIView.as_view(), name="api_register"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
