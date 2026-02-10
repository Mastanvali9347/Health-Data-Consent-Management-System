from django.utils import timezone
from .models import Consent

def has_valid_consent(patient, provider, record_type):
    return Consent.objects.filter(
        patient=patient,
        provider=provider,
        record_type=record_type,
        is_active=True,
        end_date__gte=timezone.now()
    ).exists()
