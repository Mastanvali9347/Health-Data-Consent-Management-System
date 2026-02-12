from django.urls import path
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

    path('api/login/', LoginAPIView.as_view()),
    path('api/register/', RegisterAPIView.as_view()),
    path('profile/', ProfileView.as_view()),
]
