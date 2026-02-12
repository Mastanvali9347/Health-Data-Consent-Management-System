from django.urls import path
from .views import AccessLogView

urlpatterns = [
    path('', AccessLogView.as_view()),
]
