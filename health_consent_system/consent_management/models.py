from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Consent(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_consents"
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_consents"
    )
    record_type = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]
        unique_together = ("patient", "provider", "record_type")

    def has_expired(self):
        return timezone.now() > self.end_date

    def __str__(self):
        return f"{self.patient} -> {self.provider} ({self.record_type})"
