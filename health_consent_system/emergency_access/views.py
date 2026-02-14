from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EmergencyAccess
from access_logs.models import AccessLog
from notifications.services import create_notification


@login_required(login_url="/auth/login/")
def emergency_access_page(request):
    return render(request, "doctor/emergency_access.html")


class StartEmergencyAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "DOCTOR":
            return Response({"error": "Only doctors allowed"}, status=403)

        patient_id = request.data.get("patient")
        reason = request.data.get("reason")

        if not patient_id or not reason:
            return Response({"error": "All fields required"}, status=400)

        emergency = EmergencyAccess.objects.create(
            doctor=request.user,
            patient_id=patient_id,
            reason=reason,
            is_active=True
        )

        AccessLog.objects.create(
            user=request.user,
            record=None,
            action="START_EMERGENCY_ACCESS"
        )

        create_notification(
            user=emergency.patient,
            message="Emergency access was used on your medical records"
        )

        return Response({"message": "Emergency access granted"}, status=201)


class EndEmergencyAccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        access_id = request.data.get("access_id")

        emergency = get_object_or_404(
            EmergencyAccess,
            id=access_id,
            doctor=request.user,
            is_active=True
        )

        emergency.is_active = False
        emergency.ended_at = timezone.now()
        emergency.save()

        AccessLog.objects.create(
            user=request.user,
            record=None,
            action="END_EMERGENCY_ACCESS"
        )

        return Response({"message": "Emergency access ended"})
