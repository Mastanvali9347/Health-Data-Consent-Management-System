from django.urls import path
from django.shortcuts import render
from .views import GrantConsentView

urlpatterns = [
    path('grant/', lambda request: render(request, 'patient/grant_consent.html')),
    path('api/grant/', GrantConsentView.as_view()),
]
