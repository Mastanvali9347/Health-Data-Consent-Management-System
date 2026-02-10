from django.urls import path
from .views import DoctorAccessRecordView, UploadMedicalRecordView, PatientRecordsView

urlpatterns = [
    path('upload/', UploadMedicalRecordView.as_view()),
    path('my-records/', PatientRecordsView.as_view()),
    path('doctor-access/<int:record_id>/', DoctorAccessRecordView.as_view()),

]
