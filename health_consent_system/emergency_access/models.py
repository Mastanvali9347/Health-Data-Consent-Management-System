from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class EmergencyAccess(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emergency_requests"
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emergency_accesses"
    )
    reason = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "Active" if self.is_active else "Ended"
        return f"Emergency Access: {self.doctor} -> {self.patient} ({status})"
