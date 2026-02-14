from django.urls import path
from .views import (
    patient_dashboard,
    upload_record_page,
    my_records_page,
    UploadMedicalRecordView,
    PatientRecordsAPI,
    DoctorAccessRecordView
)

urlpatterns = [
    path("dashboard/", patient_dashboard, name="patient_dashboard"),
    path("upload/", upload_record_page, name="upload_record_page"),
    path("my-records/", my_records_page, name="my_records_page"),
    path("api/upload/", UploadMedicalRecordView.as_view(), name="upload_record_api"),
    path("api/my-records/", PatientRecordsAPI.as_view(), name="patient_records_api"),
    path("doctor-access/<int:record_id>/", DoctorAccessRecordView.as_view(), name="doctor_access_record"),
]
