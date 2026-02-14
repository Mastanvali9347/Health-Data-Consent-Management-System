from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Consent
from .serializers import ConsentSerializer
from notifications.services import create_notification


@login_required(login_url="/auth/login/")
def grant_consent_page(request):
    return render(request, "patient/grant_consent.html")


@login_required(login_url="/auth/login/")
def my_consents_page(request):
    consents = Consent.objects.filter(patient=request.user)
    return render(request, "patient/consents.html", {"consents": consents})


class GrantConsentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "PATIENT":
            return Response({"error": "Only patients can grant consent"}, status=403)

        serializer = ConsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            patient=request.user,
            is_active=True
        )

        create_notification(
            user=request.user,
            message="You granted medical data consent"
        )

        return Response(
            {"message": "Consent granted successfully"},
            status=201
        )


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

        create_notification(
            user=request.user,
            message="You revoked a medical data consent"
        )

        return Response({"message": "Consent revoked successfully"})


class MyConsentsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consents = Consent.objects.filter(patient=request.user)
        serializer = ConsentSerializer(consents, many=True)
        return Response(serializer.data)
