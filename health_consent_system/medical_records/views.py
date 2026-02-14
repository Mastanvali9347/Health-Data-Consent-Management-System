from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.core.files.base import ContentFile

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from .encryption import encrypt_file

from consent_management.services import has_valid_consent
from emergency_access.services import has_emergency_access
from access_logs.models import AccessLog


@login_required(login_url="/auth/login/")
def patient_dashboard(request):
    return render(request, "patient/dashboard.html")


@login_required(login_url="/auth/login/")
def upload_record_page(request):
    return render(request, "patient/upload_record.html")


@login_required(login_url="/auth/login/")
def my_records_page(request):
    records = MedicalRecord.objects.filter(patient=request.user)
    return render(request, "patient/my_records.html", {"records": records})


class UploadMedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "PATIENT":
            return Response({"error": "Only patients can upload records"}, status=403)

        uploaded_file = request.FILES.get("file")
        record_type = request.data.get("record_type")

        if not uploaded_file or not record_type:
            return Response({"error": "File and record_type are required"}, status=400)

        encrypted_data = encrypt_file(uploaded_file.read())

        record = MedicalRecord.objects.create(
            patient=request.user,
            record_type=record_type
        )

        record.encrypted_file.save(
            uploaded_file.name,
            ContentFile(encrypted_data),
            save=True
        )

        AccessLog.objects.create(
            user=request.user,
            record=record,
            action="UPLOAD_RECORD"
        )

        return Response({"message": "Medical record uploaded successfully"}, status=201)


class PatientRecordsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = MedicalRecord.objects.filter(patient=request.user)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class DoctorAccessRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, record_id):
        if request.user.role != "DOCTOR":
            return Response({"error": "Only doctors allowed"}, status=403)

        record = get_object_or_404(MedicalRecord, id=record_id)

        consent_ok = has_valid_consent(
            patient=record.patient,
            provider=request.user,
            record_type=record.record_type
        )

        emergency_ok = has_emergency_access(
            doctor=request.user,
            patient=record.patient
        )

        if not consent_ok and not emergency_ok:
            return Response({"error": "Consent not available"}, status=403)

        AccessLog.objects.create(
            user=request.user,
            record=record,
            action="DOCTOR_VIEW_RECORD"
        )

        return Response({
            "message": "Access granted",
            "record_id": record.id,
            "record_type": record.record_type,
            "patient": record.patient.username
        })
