from django.urls import path
from django.shortcuts import render
from .views import NotificationListView

urlpatterns = [
    path('', lambda request: render(request, 'patient/notifications.html')),
    path('api/', NotificationListView.as_view()),
]
