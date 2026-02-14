from django.db import models
from django.conf import settings

class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )
    record_type = models.CharField(max_length=100)
    encrypted_file = models.FileField(upload_to="records/")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient} - {self.record_type}"
