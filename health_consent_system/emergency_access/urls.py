from django.urls import path
from django.shortcuts import render
from .views import StartEmergencyAccessView, EndEmergencyAccessView

urlpatterns = [
    path('', lambda request: render(request, 'doctor/emergency_access.html')),
    path('api/start/', StartEmergencyAccessView.as_view()),
    path('api/end/', EndEmergencyAccessView.as_view()),
]
