from .models import EmergencyAccess

def has_emergency_access(doctor, patient):
    return EmergencyAccess.objects.filter(
        doctor=doctor,
        patient=patient,
        is_active=True
    ).exists()
