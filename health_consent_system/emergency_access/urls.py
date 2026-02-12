from django.urls import path
from .views import (
    emergency_access_page,
    StartEmergencyAccessView,
    EndEmergencyAccessView
)

urlpatterns = [
    path('', emergency_access_page),
    path('api/start/', StartEmergencyAccessView.as_view()),
    path('api/end/', EndEmergencyAccessView.as_view()),
]
