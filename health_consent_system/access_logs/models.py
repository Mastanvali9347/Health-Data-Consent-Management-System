from django.db import models
from django.contrib.auth import get_user_model
from medical_records.models import MedicalRecord

User = get_user_model()


class AccessLog(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_access_logs"
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_access_logs"
    )

    record = models.ForeignKey(
        MedicalRecord,
        on_delete=models.CASCADE
    )

    access_type = models.CharField(
        max_length=20,
        choices=[
            ('CONSENT', 'Consent'),
            ('EMERGENCY', 'Emergency')
        ]
    )

    reason = models.TextField()

    accessed_at = models.DateTimeField(auto_now_add=True)
