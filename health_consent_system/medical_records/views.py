from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from consent_management.services import has_valid_consent
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from .encryption import encrypt_file

class UploadMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'PATIENT':
            return Response({"error": "Only patients can upload records"}, status=403)

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "File is required"}, status=400)

        encrypted_data = encrypt_file(uploaded_file.read())

        record = MedicalRecord.objects.create(
            patient=request.user,
            record_type=request.data.get('record_type')
        )

        record.encrypted_file.save(
            uploaded_file.name,
            ContentFile(encrypted_data)
        )

        return Response({"message": "Medical record uploaded successfully"})

class PatientRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = MedicalRecord.objects.filter(patient=request.user)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)

class DoctorAccessRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, record_id):
        if request.user.role != 'DOCTOR':
            return Response({"error": "Only doctors allowed"}, status=403)

        record = get_object_or_404(MedicalRecord, id=record_id)

        if not has_valid_consent(
            patient=record.patient,
            provider=request.user,
            record_type=record.record_type
        ):
            return Response({"error": "Consent not available"}, status=403)

        return Response({
            "message": "Consent verified. Access allowed",
            "record_type": record.record_type,
            "patient": record.patient.username
        })
