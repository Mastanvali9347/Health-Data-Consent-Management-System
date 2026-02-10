from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    record_type = models.CharField(max_length=100)
    encrypted_file = models.FileField(upload_to='records/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.record_type}"
