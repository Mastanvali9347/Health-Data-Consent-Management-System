from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .views import StartEmergencyAccessView, EndEmergencyAccessView


@login_required(login_url="/auth/login/")
def emergency_access_page(request):
    return render(request, "doctor/emergency_access.html")


urlpatterns = [
    path("", emergency_access_page, name="emergency_access_page"),
    path("api/start/", StartEmergencyAccessView.as_view(), name="start_emergency_access"),
    path("api/end/", EndEmergencyAccessView.as_view(), name="end_emergency_access"),
]
