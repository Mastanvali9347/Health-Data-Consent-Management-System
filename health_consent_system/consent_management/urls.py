from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .views import (
    GrantConsentView,
    RevokeConsentView,
    MyConsentsAPI
)


@login_required(login_url="/auth/login/")
def grant_consent_page(request):
    return render(request, "patient/grant_consent.html")


urlpatterns = [
    path("grant/", grant_consent_page, name="grant_consent_page"),
    path("api/grant/", GrantConsentView.as_view(), name="grant_consent_api"),
    path("api/revoke/<int:consent_id>/", RevokeConsentView.as_view(), name="revoke_consent_api"),
    path("api/my-consents/", MyConsentsAPI.as_view(), name="my_consents_api"),
]
