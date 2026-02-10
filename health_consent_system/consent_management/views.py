from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Consent
from .serializers import ConsentSerializer

class GrantConsentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'PATIENT':
            return Response({"error": "Only patients can grant consent"}, status=403)

        serializer = ConsentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(patient=request.user)
        return Response({"message": "Consent granted"})


class RevokeConsentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, consent_id):
        consent = Consent.objects.get(id=consent_id, patient=request.user)
        consent.is_active = False
        consent.end_date = timezone.now()
        consent.save()
        return Response({"message": "Consent revoked"})


class MyConsentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consents = Consent.objects.filter(patient=request.user)
        serializer = ConsentSerializer(consents, many=True)
        return Response(serializer.data)
