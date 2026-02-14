from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from accounts.models import User
from consent_management.models import Consent
from access_logs.models import AccessLog


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "total_users": User.objects.count(),
            "total_consents": Consent.objects.count(),
            "total_logs": AccessLog.objects.count()
        })
