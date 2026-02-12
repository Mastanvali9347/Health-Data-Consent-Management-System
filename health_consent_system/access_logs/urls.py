from django.urls import path
from .views import access_logs_page, MyAccessLogsAPI

urlpatterns = [
    path('', access_logs_page),
    path('api/', MyAccessLogsAPI.as_view()),
]
