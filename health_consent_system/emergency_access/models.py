from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class EmergencyAccess(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_patient')
    reason = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Emergency Access: {self.doctor} -> {self.patient} ({'Active' if self.is_active else 'Ended'})"
    