from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Consent
from .serializers import ConsentSerializer
from access_logs.models import AccessLog
from notifications.services import create_notification


@login_required
def grant_consent_page(request):
    return render(request, 'patient/grant_consent.html')


@login_required
def my_consents_page(request):
    consents = Consent.objects.filter(patient=request.user)
    return render(request, 'patient/consents.html', {'consents': consents})

class GrantConsentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'PATIENT':
            return Response({"error": "Only patients can grant consent"}, status=403)

        doctor_id = request.data.get('provider')
        record_type = request.data.get('record_type')
        end_date = request.data.get('end_date')

        if not doctor_id or not record_type or not end_date:
            return Response({"error": "All fields required"}, status=400)

        consent = Consent.objects.create(
            patient=request.user,
            provider_id=doctor_id,
            record_type=record_type,
            end_date=end_date
        )

        AccessLog.objects.create(
            user=request.user,
            record=None,
            action='GRANT_CONSENT'
        )

        return Response({"message": "Consent granted successfully"}, status=201)


class RevokeConsentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consent_id):
        consent = get_object_or_404(
            Consent,
            id=consent_id,
            patient=request.user,
            is_active=True
        )

        consent.is_active = False
        consent.end_date = timezone.now()
        consent.save()

        AccessLog.objects.create(
            user=request.user,
            record_id=0,
            action="REVOKE_CONSENT"
        )

        create_notification(
            user=request.user,
            message="You revoked a consent"
        )

        return Response({"message": "Consent revoked successfully"})


class MyConsentsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consents = Consent.objects.filter(patient=request.user)
        serializer = ConsentSerializer(consents, many=True)
        return Response(serializer.data)
