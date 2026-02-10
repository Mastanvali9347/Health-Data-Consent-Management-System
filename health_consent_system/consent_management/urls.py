from django.urls import path
from .views import GrantConsentView, RevokeConsentView, MyConsentsView

urlpatterns = [
    path('grant/', GrantConsentView.as_view()),
    path('revoke/<int:consent_id>/', RevokeConsentView.as_view()),
    path('my-consents/', MyConsentsView.as_view()),
]
