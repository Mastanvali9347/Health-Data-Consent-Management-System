from django.urls import path
from .views import (
    grant_consent_page,
    my_consents_page,
    GrantConsentView,
    RevokeConsentView,
    MyConsentsAPI
)

urlpatterns = [
    path('grant/', grant_consent_page),
    path('my/', my_consents_page),

    path('api/grant/', GrantConsentView.as_view()),
    path('api/revoke/<int:consent_id>/', RevokeConsentView.as_view()),
    path('api/my/', MyConsentsAPI.as_view()),
]
